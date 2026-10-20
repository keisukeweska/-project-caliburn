import os
import time
import feedparser
from google import genai

# 情報収集ソース（海外主要7大テックメディア）
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
    news_items = []
    print("【カリバーン】海外主要7大ソースからニュースデータを一括取得中...")
    
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                title = entry.get("title", "")
                summary = entry.get("summary", entry.get("description", ""))
                link = entry.get("link", "")
                source_name = feed.feed.get("title", "海外テックメディア")
                if title:
                    news_items.append(f"【出所: {source_name}】\n- タイトル: {title}\n  URL: {link}\n  概要: {summary[:250]}...")
        except Exception as e:
            print(f"RSS取得スキップ ({url}): {e}")
            
    print(f"【カリバーン】合計 {len(news_items)} 件のニュースを取得完了。")
    return news_items

def generate_article():
    news_list = fetch_latest_ai_news()
    
    if not news_list:
        print("Error: ニュースの取得に失敗しました。")
        return

    news_text = "\n\n".join(news_list)
    client = genai.Client()

    prompt = f"""
あなたは海外テック業界に10年以上身を置き、現地情報と一次ソースを毎日追い続けている「独立系テックアナリスト」です。
月額500円を払っている熱心なビジネスパーソン・エンジニア読者に向けて、今朝の海外AIニュースの中から「絶対に知っておくべき3大トピック」を厳選し、本気の個人レポートを執筆してください。

【今朝収集した海外一次情報】
{news_text}

---

【執筆ルール（「AI感」を完全に消すための約束）】

1. **トーン＆マナー（重要）**
   - 「AIが生成した文章」と思わせる丁寧すぎる定型文（「〜について解説します」「いかがでしたでしょうか」「〜が期待されます」等）は一切禁止。
   - 人間のアナリストが自分の言葉で語っているような、言い切り型で切れ味のあるプロの文体（「〜だ」「〜と言える」「正直ここが肝になる」）にすること。
   - 「AIがまとめました」「取得したデータによると」といった機械的な表現は厳禁。「今朝の米テックメディアの動向を見る限り」「現場の感覚からすると」等の人間味のある表現を使うこと。

2. **構成テンプレ**

# 🚀 【日刊AI海外動向】（鋭い見出し・分析サブタイトル）

> 💡 **今朝の業界インサイト（アナリストの眼）**
> （海外の動きから見えてきた、今日のAI業界全体の潮目や裏の背景を、プロの視点から2〜3行で鋭く言い切る）

---

## ⚡ 1分で掴む！本日の要点（TL;DR）
- **トピック1**: （1行で要約）
- **トピック2**: （1行で要約）
- **トピック3**: （1行で要約）

---

## 🔍 今朝の厳選トピック & 独自分析

### 1. [1つ目のニュースタイトル]
> 📌 **ここだけ抑えればOK**: 
> 🌐 **一次ソース**: [公式記事リンク](URL)

* **【何が起きたのか】**
  （事実に絞って短文で解説）
* **【裏にある構造・競合比較】**
  （なぜこれが話題なのか、既存の枠組みと何が違うのか）
* **【日本の現場はどう動くべきか】**
  （明日から取れる具体策や判断基準）

### 2. [2つ目のニュースタイトル]
> 📌 **ここだけ抑えればOK**: 
> 🌐 **一次ソース**: [公式記事リンク](URL)

* **【何が起きたのか】**
* **【裏にある構造・競合比較】**
* **【日本の現場はどう動くべきか】**

### 3. [3つ目のニュースタイトル]
> 📌 **ここだけ抑えればOK**: 
> 🌐 **一次ソース**: [公式記事リンク](URL)

* **【何が起きたのか】**
* **【裏にある構造・競合比較】**
* **【日本の現場はどう動くべきか】**

---

## 🎁 明日から使える実践インサイト
（今日のトピックを自社の業務や個人の開発に即座に落とし込むための、具体的なプロンプト例やチェックリストを1つ提示する）

---
※架空のツール名・情報は絶対禁止。実在データのみ扱ってください。
"""

    candidate_models = [
        "gemini-3.8-flash",
        "gemini-flash-latest"
    ]

    response = None
    for attempt in range(1, 4):
        print(f"【カリバーン】プロアナリスト記事生成トライアル #{attempt}...")
        for model_name in candidate_models:
            try:
                print(f"【カリバーン】モデル '{model_name}' で執筆中...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                print(f"【カリバーン】成功: 人間味と深みのあるプロ記事を生成しました。")
                break
            except Exception as e:
                print(f"【カリバーン】モデル '{model_name}' 失敗: {e}")
        
        if response:
            break
        
        print(f"【カリバーン】5秒後に再試行します...")
        time.sleep(5)

    if not response:
        print("Error: 記事生成に失敗しました。")
        return

    os.makedirs("posts", exist_ok=True)
    with open("posts/latest_comparison.md", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("【カリバーン】『脱AI・プロアナリスト仕様』の記事生成が完了しました！")

if __name__ == "__main__":
    generate_article()
