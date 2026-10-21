import os
import time
import requests
import google.generativeai as genai

# APIキーの設定
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_article_with_fallback(prompt_text):
    # 混雑に強いモデルの優先順位リスト
    models_to_try = [
        'gemini-2.5-flash',
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-2.5-pro'
    ]
    
    max_retries_per_model = 3  # 各モデルでのリトライ回数
    retry_delay = 15            # リトライ時の待ち時間（秒）

    for model_name in models_to_try:
        print(f"【カリバーン】モデル '{model_name}' で執筆を試行中...")
        for attempt in range(1, max_retries_per_model + 1):
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt_text)
                
                if response and response.text:
                    print(f"【カリバーン】成功: モデル '{model_name}' で記事を生成しました！")
                    return response.text
            except Exception as e:
                print(f"【カリバーン】モデル '{model_name}' 試行 {attempt}/{max_retries_per_model} 失敗: {e}")
                if attempt < max_retries_per_model:
                    print(f"【カリバーン】{retry_delay}秒後に再試行します...")
                    time.sleep(retry_delay)
        
        print(f"【カリバーン】モデル '{model_name}' は混雑のためスキップし、次のモデルへ切り替えます。")

    raise Exception("すべてのGeminiモデルが混雑または応答不能のため、記事生成に失敗しました。")

def send_to_discord(content):
    if not DISCORD_WEBHOOK_URL:
        print("【注意】DISCORD_WEBHOOK_URL が設定されていないため、Discord送信をスキップします。")
        return
    
    # Discordの文字数制限（2000文字）対策として分割または切り詰め
    payload = {"content": content[:2000]}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204 or response.status_code == 200:
        print("【カリバーン】Discordへの送信に成功しました！")
    else:
        print(f"【注意】Discord送信失敗: {response.status_code}, {response.text}")

def main():
    print("【カリバーン】システム起動...")
    
    # テスト用のプロンプト（必要に応じてスクレイピング結果などをここに結合する）
    prompt = "AIトレンドや開発者向けの高価値なプレミアム記事を、日本語でマークダウン形式で執筆してください。"
    
    try:
        # 記事生成実行
        article_text = generate_article_with_fallback(prompt)
        
        # Discordへ通知
        send_to_discord(article_text)
        
        print("【カリバーン】全工程が正常に完了しました！")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
