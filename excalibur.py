import os
import time
import json
import re
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_available_models():
    """現在利用可能なモデルリストを動的に取得"""
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_name = m.name.replace("models/", "")
                available_models.append(model_name)
        
        available_models.sort(key=lambda x: (
            0 if '3.8' in x else
            1 if '3.1' in x else
            2 if 'flash' in x else 3
        ))
        return available_models
    except Exception:
        return ['gemini-3.8-flash', 'gemini-3.1-pro-preview', 'gemini-flash-latest']

def generate_json_data():
    models_to_try = get_available_models()
    max_retries = 2
    retry_delay = 10

    prompt = """
    海外の最新AIコーディング・開発支援ツールの比較データをJSON形式で作成してください。
    以下のフォーマットのみを出力し、マークダウンのコードブロック(```json ... ```)を含めてください。

    [
      {
        "id": "claude-code",
        "name": "Claude Code",
        "price": "$20/mo",
        "models": ["Opus 4.6", "Sonnet 4.6"],
        "usage": "Usage limits apply",
        "tiers": 3,
        "highlight": "Gold Standard",
        "affiliate_url": "https://anthropic.com",
        "description": "Anthropicの次世代ターミナル型AIコーディングエージェント。"
      },
      {
        "id": "glm-zai",
        "name": "GLM (Z.ai)",
        "price": "$3/mo",
        "models": ["GLM-5", "GLM-4.7"],
        "usage": "~80 prompts",
        "tiers": 3,
        "highlight": "Free MCP Tools",
        "affiliate_url": "https://z.ai",
        "description": "圧倒的コスパを誇る軽量コード生成モデル。"
      },
      {
        "id": "minimax",
        "name": "MiniMax",
        "price": "$10/mo",
        "models": ["M2.5", "M2.5-highspeed"],
        "usage": "100 prompts",
        "tiers": 6,
        "highlight": "100+ TPS",
        "affiliate_url": "https://minimaxi.com",
        "description": "超高速トークン生成を特長とする爆速モデル。"
      },
      {
        "id": "kimi",
        "name": "Kimi",
        "price": "~$7/wk",
        "models": ["Kimi K2.5"],
        "usage": "300-1,200 calls",
        "tiers": 1,
        "highlight": "100 TPS",
        "affiliate_url": "https://moonshot.cn",
        "description": "長文コンテキストと高速推論に特化した開発支援AI。"
      },
      {
        "id": "qwen",
        "name": "Qwen (Alibaba)",
        "price": "$10/mo",
        "models": ["Qwen3.5-Plus", "Qwen3-Coder"],
        "usage": "1,200 requests",
        "tiers": 2,
        "highlight": "Multi-model",
        "affiliate_url": "https://aliyun.com",
        "description": "Alibabaが提供する強力なオープンウェイト/商用コードAI。"
      }
    ]
    """

    for model_name in models_to_try:
        print(f"【カリバーン】モデル '{model_name}' でAIデータ生成中...")
        for attempt in range(1, max_retries + 1):
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                
                if response and response.text:
                    # JSON部分だけを抽出
                    text = response.text
                    match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
                    if match:
                        json_str = match.group(1)
                    else:
                        json_str = text
                    
                    # 正当なJSONかチェック
                    data = json.loads(json_str)
                    print(f"【カリバーン】成功！モデル '{model_name}' でデータ抽出完了。")
                    return data
            except Exception as e:
                print(f"【カリバーン】モデル '{model_name}' 試行 {attempt}/{max_retries} 失敗: {e}")
                if attempt < max_retries:
                    time.sleep(retry_delay)

    raise Exception("全モデルでデータ生成に失敗しました。")

def save_site_files(data):
    """Webサイト用データとAI検索(GEO)用ファイルを保存"""
    os.makedirs("public", exist_ok=True)
    
    # 1. 比較Webサイト用 JSONデータ
    with open("public/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("【カリバーン】public/data.json を出力しました。")
    
    # 2. AI検索(Perplexity / ChatGPT等)用 llms.txt
    llms_text = f"# AI Coding Plans Comparison (2026 Updated)\n\n"
    llms_text += "Updated regularly via Automated AI Pipeline.\n\n"
    llms_text += "## Live Comparison Summary\n"
    for item in data:
        llms_text += f"- **{item['name']}**: Starting Price: {item['price']} | Core Models: {', '.join(item['models'])} | Highlight: {item['highlight']}\n"
    
    with open("public/llms.txt", "w", encoding="utf-8") as f:
        f.write(llms_text)
    print("【カリバーン】public/llms.txt (AI検索対策) を出力しました。")

    # 3. クローラー用 robots.txt
    robots_txt = "User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n"
    with open("public/robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_txt)

def main():
    print("【カリバーン】比較メディア連動データ構築モード起動...")
    try:
        data = generate_json_data()
        save_site_files(data)
        print("【カリバーン】全てのデータ生成・保存処理が正常完了しました！")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
