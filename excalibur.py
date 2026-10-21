import os
import time
import requests
import google.generativeai as genai

# APIキーとDiscord Webhookの設定
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_available_models():
    """現在APIで利用可能な generateContent 対応モデルを動的に取得する"""
    try:
        available_models = []
        for m in genai.list_models():
            # generateContent（テキスト生成）に対応しているモデルを抽出
            if 'generateContent' in m.supported_generation_methods:
                # 'models/gemini-xxx' からモデルID部分を取り出す
                model_name = m.name.replace("models/", "")
                available_models.append(model_name)
        
        # 優先度の高いモデル（3.8 / 3.1 / flash系）が先頭に来るようにソート
        available_models.sort(key=lambda x: (
            0 if '3.8' in x else
            1 if '3.1' in x else
            2 if 'flash' in x else 3
        ))
        
        print(f"【カリバーン】現在利用可能なモデルリストを動的に取得完了: {available_models}")
        return available_models
    except Exception as e:
        print(f"【注意】モデル一覧の動的取得に失敗。バックアップリストを使用します: {e}")
        # 万が一動的取得が失敗した際の予備リスト
        return ['gemini-3.8-flash', 'gemini-3.1-pro-preview', 'gemini-flash-latest']

def generate_article_with_fallback(prompt_text):
    """動的モデル取得 ＋ リトライ ＋ 全自動切り替えロジック"""
    models_to_try = get_available_models()
    
    max_retries_per_model = 2  # 各モデルでのリトライ回数
    retry_delay = 10            # 混雑（503）時の待機時間（秒）

    for model_name in models_to_try:
        print(f"【カリバーン】モデル '{model_name}' で執筆を試行中...")
        for attempt in range(1, max_retries_per_model + 1):
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt_text)
                
                if response and response.text:
                    print(f"【カリバーン】成功！モデル '{model_name}' で記事を生成しました。")
                    return response.text
            except Exception as e:
                print(f"【カリバーン】モデル '{model_name}' 試行 {attempt}/{max_retries_per_model} 失敗: {e}")
                if attempt < max_retries_per_model:
                    print(f"【カリバーン】{retry_delay}秒待機して再試行します...")
                    time.sleep(retry_delay)
        
        print(f"【カリバーン】モデル '{model_name}' は利用不可または混雑のためスキップ。次のモデルへ...")

    raise Exception("すべての利用可能Geminiモデルでの記事生成に失敗しました。")

def send_to_discord(content):
    if not DISCORD_WEBHOOK_URL:
        print("【注意】DISCORD_WEBHOOK_URL が設定されていないため、Discord送信をスキップします。")
        return
    
    payload = {"content": content[:2000]}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code in [200, 204]:
        print("【カリバーン】Discordへの送信に成功しました！")
    else:
        print(f"【注意】Discord送信失敗: {response.status_code}, {response.text}")

def main():
    print("【カリバーン】全自動堅牢モードで起動...")
    
    prompt = """
    海外の最新AIツール・SaaSに関する情報をまとめ、開発者やテック層に向けた高価値な記事を作成してください。
    記事には以下の要素を含めてください：
    1. 【3行要約】
    2. ツールの概要と革新的な点
    3. 主な機能と活用例
    4. 今後の展望・まとめ
    """
    
    try:
        article_text = generate_article_with_fallback(prompt)
        send_to_discord(article_text)
        print("【カリバーン】全工程が正常に完了しました！")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
