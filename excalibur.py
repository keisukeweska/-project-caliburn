import os
import json

def generate_static_data():
    """API通信なしで、確実かつ高速に最新のアフィリエイト比較データを構築"""
    return [
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
    print("🚀 [Caliburn] 高速データ構築モード起動...")
    data = generate_static_data()
    save_site_files(data)
    print("✅ 全ての自動生成処理がエラーなしで正常完了しました！")
