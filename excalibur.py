import os
import time
import json
import re
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else genai.Client()

# ==========================================
# 💰 あなたの紹介報酬が入るアフィリエイトURL定義
# ==========================================
AFFILIATE_URLS = {
    "Claude Code": "https://anthropic.com?ref=YOUR_AFFILIATE_ID",
    "GLM (Z.ai)": "https://z.ai?ref=YOUR_AFFILIATE_ID",
    "MiniMax": "https://minimaxi.com?ref=YOUR_AFFILIATE_ID",
    "Kimi": "https://moonshot.cn?ref=YOUR_AFFILIATE_ID",
    "Qwen (Alibaba)": "https://aliyun.com?ref=YOUR_AFFILIATE_ID"
}

def generate_json_data():
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
        "affiliate_url": "https://anthropic.com?ref=YOUR_AFFILIATE_ID",
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
        "affiliate_url": "https://z.ai?ref=YOUR_AFFILIATE_ID",
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
        "affiliate_url": "https://minimaxi.com?ref=YOUR_AFFILIATE_ID",
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
        "affiliate_url": "https://moonshot.cn?ref=YOUR_AFFILIATE_ID",
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
        "affiliate_url": "https://aliyun.com?ref=YOUR_AFFILIATE_ID",
        "description": "Alibabaが提供する強力なオープンウェイト/商用コードAI。"
      }
    ]
    """

    models_to_try = ['gemini-3.8-flash', 'gemini-flash-latest']
    
    for model_name in models_to_try:
        print(f"【カリバーン】モデル '{model_name}' でデータ構築中...")
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            if response and response.text:
                text = response.text
                match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
                json_str = match.group(1) if match else text
                data = json.loads(json_str)
                
                # アフィリエイトURLの差し替え補正
                for item in data:
                    if item['name'] in AFFILIATE_URLS:
                        item['affiliate_url'] = AFFILIATE_URLS[item['name']]
                        
                print(f"✅ 成功！モデル '{model_name}' でデータ生成完了。")
                return data
        except Exception as e:
            print(f"⚠️ モデル '{model_name}' 失敗: {e}")
            time.sleep(3)

    raise Exception("全モデルで生成に失敗しました。")

def save_site_files(data):
    os.makedirs("public", exist_ok=True)
    
    # 1. 比較Webサイト用 JSONデータ（index.htmlがこれを読み込む）
    with open("public/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("【カリバーン】public/data.json を出力しました。")
    
    # 2. AI検索(Perplexity / ChatGPT等)用 llms.txt (GEO対策)
    llms_text = "# AI Coding Plans Comparison (2026 Updated)\n\n"
    for item in data:
        llms_text += f"- **{item['name']}**: Price: {item['price']} | Link: {item['affiliate_url']}\n"
    with open("public/llms.txt", "w", encoding="utf-8") as f:
        f.write(llms_text)
    print("【カリバーン】public/llms.txt を出力しました。")

if __name__ == "__main__":
    print("🚀 [Caliburn] 比較メディア連動データ構築モード起動...")
    data = generate_json_data()
    save_site_files(data)
    print("✅ 全ての自動生成処理が正常完了しました！")
