import os
import time
import feedparser
from google import genai

# 1. AIニュース ＋ 海外個人開発・SaaS・エンジニアコミュニティのハイブリッド情報源
RSS_URLS = [
    # --- 海外主要AI・テックメディア ---
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
    # --- 個人開発・SaaS・プロダクト・開発者コミュニティ ---
    "https://www.producthunt.com/feed",
    "https://hnrss.org/frontpage"
]

def fetch_latest_tech_news():
    news_items = []
    print("【カリバーン】海外AI・SaaS・開発者メディアから一括取得中...")
    
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
            
    print(f"【カリバーン】合計 {len(news_items)} 件のハイブリッドデータを取得完了。")
    return news_items

def generate_article():
    news_list = fetch_latest_tech_news()
    
    if not news_list:
        print("Error: ニュースの取得に失敗しました。")
        return

    news_text = "\n\n".join(news_list)
    client = genai.Client()

    # AIトレンド＋海外SaaS・マネタイズ特化の合体型プロンプト
    prompt = f"""
あなたは月額500円の有料マガジンで高い支持を得ている、海外テック・SaaS分析のプロアナリストです。
以下に提供する【本日取得した海外データ一覧】（計{len(news_list)}件）を深く精読し、
日本のビジネスパーソン、エンジニア、副業・個人開発志向層に向けて、
「最新AIトレンド」と「海外でバズっているSaaS・マネタイズ事例」を融合させた超有料級レポートを作成してください。

【本日取得した海外データ一覧】
{news_text}

---

【執筆およびnote最適化ルール】

1. **トーン＆マナー**:
   - 定型的なAI文体（「〜を解説します」「いかがでしたか」等）は厳禁。
   - 海外市場を知り尽くしたプロのアナリストとして、人間味と切れ味のある文体（「〜だ」「〜と言える」「ここがビジネスの肝になる」）で執筆すること。

2. **選定構成（計3トピック）**:
   - **トピック1 & 2**: 今朝の海外AI重要ニュース（技術・巨大テック動向・規制など）
   - **トピック3**: 海外で注目の新ツール・SaaS・個人開発事例（Product HuntやHacker News等から「稼げるヒント」「作れるアイデア」になるものを厳選）

3. **構成テンプレート（note有料ライン対応）**:

# 🚀 【日刊AI＆海外SaaS動向】（ビジネス視点のキャッチコピー）

> 💡 **今朝のインサイト（アナリストの眼）**
> （海外の動向から見えてきたAI業界・SaaSビジネスの「潮目・狙い目」を2〜3行で鋭く指摘）

## ⚡ 1分で掴む！今朝の3行要約（TL;DR）
- **AIトピック1**: （1行で要約）
- **AIトピック2**: （1行で要約）
- **注目SaaS/開発事例**: （1行で要約）

---
<!-- note有料ライン -->
---

## 🔍 今朝の厳選解説（AIトレンド ✕ 海外SaaSマネタイズ）

### 1. [AIトピック1のタイトル]
> 📌 **ここだけ抑えればOK**: 
> 🌐 **一次ソース**: [公式記事リンク](URL)

* **【何が起きたのか】**
* **【裏の構造・競合比較】**
* **【日本企業・現場へのインパクト】**

### 2. [AIトピック2のタイトル]
> 📌 **ここだけ抑えればOK**: 
> 🌐 **一次ソース**: [公式記事リンク](URL)

* **【何が起きたのか】**
* **【裏の構造・競合比較】**
* **【日本企業・現場へのインパクト】**

### 3. 🔥【注目の海外SaaS・個人開発分析】[3つ目のタイトル]
> 📌 **ここだけ抑えればOK**: 
> 🌐 **一次ソース**: [公式記事リンク](URL)

* **【どんなプロダクト・事例か】**
  （概要や海外でウケている理由）
* **【マネタイズ・グロースのポイント】**
  （どうやって収益化・ユーザー獲得しているか）
* **【日本で真似・応用するヒント】**
  （日本市場で個人開発者や副業層が応用できる具体的なアイデア）

---

## 🎯 今日のアクションプラン
- **ビジネス・マネジメント層**: （明日判断・検討すべきこと）
- **エンジニア・個人開発層**: （明日試すべき技術・プロダクトアイデア）

---

## 🎁 【マガジン限定特典】明日から使える即戦力アセット
（今日のトピックに関連して、業務や開発でコピペで使えるプロンプト例、またはSaaS構想チェックリストを1つ提供）

---
※実在するデータのみ扱い、架空のツール名は絶対に使用しないでください。
"""

    candidate_models = [
        "gemini-3.8-flash",
        "gemini-flash-latest"
    ]

    response = None
    for attempt in range(1, 4):
        print(f"【カリバーン】合体版プレミアム記事生成トライアル #{attempt}...")
        for model_name in candidate_models:
            try:
                print(f"【カリバーン】モデル '{model_name}' で執筆中...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                print(f"【カリバーン】成功: 『AI ✕ 海外SaaS』合体版記事を生成しました。")
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
    
    print("【カリバーン】『AI ✕ 海外SaaS合体版』の記事生成が完了しました！")

if __name__ == "__main__":
    generate_article()
