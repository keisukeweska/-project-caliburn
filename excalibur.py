import os
import time
import feedparser
from google import genai
from google.genai.errors import APIError

# 1. 取得する海外AIニュースのRSSフィード一覧
RSS_URLS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
]

def fetch_latest_ai_news():
    """海外メディアから最新のAIニュース記事タイトルと概要を取得する"""
    news_items = []
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                title = entry.get("title", "")
                summary = entry.get("summary", entry.get("description", ""))
                link = entry.get("link", "")
                if title:
                    news_items.append(f"- タイトル: {title}\n  URL: {link}\n  概要: {summary[:200]}...")
        except Exception as e:
            print(f"RSS取得エラー ({url}): {e}")
    return news_items

def generate_article():
    news_list = fetch_latest_ai_news()
    
    if not news_list:
        print("Error: 海外ニュースの取得に失敗したか、記事が見つかりませんでした。")
        return

    news_text = "\n".join(news_list)
    client = genai.Client()

    prompt = f"""
以下は本日取得した海外の最新AIツール・AI関連のニュースデータです。
この実在するニュース情報のみをベースにして、日本のビジネスパーソン向けに分かりやすいAI解説・比較記事を作成してください。

【取得した海外AIニュースデータ】
{news_text}

【記事作成ルール】
1. 架空のツール名（「New AI Tool」など）は絶対に使用しないでください。取得データにある実在のツール・企業・ニュースのみを扱ってください。
2. 記事のタイトル、概要、具体的な活用シーンや注目ポイントを日本語でわかりやすく解説してください。
3. 記事の最後に、元となったニュースへのリンク（公式URL）を記載してください。
4. Markdown形式で出力してください。
"""

    candidate_models = [
        "gemini-3.8-flash",
        "gemini-flash-latest"
    ]

    response = None
    # 混雑時の503エラー対策として、モデル全体への試行を数回リトライする
    for attempt in range(1, 4):
        print(f"【カリバーン】記事生成トライアル #{attempt}...")
        for model_name in candidate_models:
            try:
                print(f"【カリバーン】モデル '{model_name}' で生成を試行中...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                print(f"【カリバーン】成功: モデル '{model_name}' を使用して記事を生成しました。")
                break
            except Exception as e:
                print(f"【カリバーン】モデル '{model_name}' 失敗: {e}")
        
        if response:
            break
        
        print(f"【カリバーン】サーバーが混雑しているため、5秒後に再試行します...")
        time.sleep(5)

    if not response:
        print("Error: サーバー混雑により、利用可能なGeminiモデルで生成できませんでした。時間をおいて再実行してください。")
        return

    os.makedirs("posts", exist_ok=True)
    with open("posts/latest_comparison.md", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("【カリバーン】本物のニュースに基づいた記事生成が完了しました！")

if __name__ == "__main__":
    generate_article()
