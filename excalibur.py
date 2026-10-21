import time
import google.generativeai as genai

def generate_article_with_fallback(prompt_text):
    # 試行するモデルの優先順位リスト（混雑に強いモデルを網羅）
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
