import os
import time
import feedparser
from google import genai

# 1. 情報収集ソースを主要7大海外メディアに拡大
RSS_URLS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://hnrss.org/frontpage",
    "https://feeds.feedburner.com/nvidiablog"
]

def fetch_latest_ai_news():
    """海外メディアから最新ニュースタイトルと概要を一括取得"""
    news_items = []
    print("【カリバーン】海外主要7大ソースからニュースデータを一括取得中...")
    
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]: # 各メディアから最新3件を取得
                title = entry.get("title", "")
                summary = entry.get("summary", entry.get("description", ""))
                link = entry.get("link", "")
                source_name = feed.feed.get("title", "海外テックメディア")
                if title:
                    news_items.append(f"【出所: {source_name}】\n- タイトル: {title}\n  URL: {link}\n  概要: {summary[:250]}...")
        except Exception as e:
            print(f"RSS取得スキップ ({url}): {e}")
            
    print(f"【カリバーン】合計 {len(news_items)} 件の海外ニュースを取得完了。")
    return news_items

def generate_article():
    news_list = fetch_latest_ai_news()
    
    if not news_list:
        print("Error: ニュースの取得に失敗したか、記事が見つかりませんでした。")
        return

    news_text = "\n\n".join(news_list)
    client = genai.Client()

    # スマホ読者・有料マガジン向けの視覚強化プロンプト
    prompt = f"""
あなたは有料マガジンで高い支持を得ているトップテックアナリストです。
以下に提供する【本日取得した海外AIニュース一覧】（計{len(news_list)}件）から、
日本のビジネスパーソンやIT担当者が絶対に知るべき「超重要ニュース TOP3」を厳選し、
スマホで非常に読みやすく、視覚的インパクトの強いプレミアムレポートを作成してください。

【本日取得した海外AIニュース一覧】
{news_text}

---

【レイアウト・見やすさ徹底強化ルール】

1. **構成フォーマット**:
   - **キャッチーなタイトル**（例: 【日刊AI海外動向】🔥 ○○が業界刷新 / ⚠️ ○○の規制激化 など）
   - **⚡ 1分でわかる！今日の3行まとめ（TL;DR）**: 引用ブロック（`>`）を使って冒頭に目立つ形で配置。
   - **ニュース詳細（3件）**: 以下の装飾テンプレに従って記述。

---

【各ニュースの記述テンプレート】

## 1. [ニュースタイトル]
> 📌 **ニュースの一言要約**:（1文でズバッと）  
> 🌐 **一次ソース**: [記事リンク](URL)

### 概要・背景
（スマホで読みやすいよう2〜3行ごとに改行を入れること）

### 💡 注目ポイント & 競合比較
* **ここがスゴい**: （メリットや革新性）
* **従来との違い**: （既存ツールとの比較）

### 🎯 日本ビジネスへのインパクト & 明日からのアクション
* **現場への影響**: （日本企業への波及効果）
* **推奨アクション**: （明日からやるべき具体的な一手）

---

2. **視覚デザイン（装飾）**:
   - 絵文字（🔥 💡 🎯 📌 ⚠️ ⚡ 🌐）を効果的に使って視線誘導を行うこと。
   - 重要な数値・ツール名・会社名は**太字**で強調すること。
   - 1つの段落が長くなりすぎないよう、短文でリズム良く書くこと。
   - 架空のツール名は絶対禁止。実在の取得データのみ扱うこと。
"""

    candidate_models = [
        "gemini-3.8-flash",
        "gemini-flash-latest"
    ]

    response = None
    for attempt in range(1, 4):
        print(f"【カリバーン】デザイン最適化記事生成トライアル #{attempt}...")
        for model_name in candidate_models:
            try:
                print(f"【カリバーン】モデル '{model_name}' でAI解析・レイアウト装飾中...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                print(f"【カリバーン】成功: モデル '{model_name}' を使用して超・見やすい記事を生成しました。")
                break
            except Exception as e:
                print(f"【カリバーン】モデル '{model_name}' 失敗: {e}")
        
        if response:
            break
        
        print(f"【カリバーン】サーバー混雑のため、5秒後に再試行します...")
        time.sleep(5)

    if not response:
        print("Error: サーバー混雑のため記事生成に失敗しました。")
        return

    # 生成結果の保存
    os.makedirs("posts", exist_ok=True)
    with open("posts/latest_comparison.md", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("【カリバーン】超・見やすいプレミアム記事の全自動生成が完了しました！")

if __name__ == "__main__":
    generate_article()
