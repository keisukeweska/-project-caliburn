import os
import time
import feedparser
from google import genai

# ハイブリッド情報源（AIニュース ＋ 海外個人開発・SaaS・開発者コミュニティ）
RSS_URLS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
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

    prompt = f"""
あなたは月額500円の有料マガジンで数千人の有料会員を抱えるトップAI・SaaSシニアアナリスト兼プロダクトエンジニアです。
提供された【本日取得した海外データ一覧】から厳選し、読者が「500円どころか5,000円の価値がある」と衝撃を受けるレベルの実用・実践型プレミアムレポートを執筆してください。

【本日取得した海外データ一覧】
{news_text}

---

【執筆およびnote最適化ルール】

1. **トーン＆マナー**:
   - 定型的なAI文体（「〜を解説します」「いかがでしたか」等）は完全排除。
   - 業界の裏まで知り尽くしたプロの切れ味ある文体（「〜だ」「〜と言える」「正直ここは〜だ」）で執筆すること。

2. **構成テンプレ（note有料ライン対応）**:

# 🚀 【日刊AI＆海外SaaS動向】（鋭い見出し・ビジネス視点）

> 💡 **今朝のインサイト（アナリストの眼）**
> （海外の動向から見えてきたAI業界・SaaSビジネスの「潮目・狙い目」を2〜3行で鋭く指摘）

## ⚡ 1分で掴む！今朝の3行要約（TL;DR）
- **AIトピック1**: （1行要約）
- **AIトピック2**: （1行要約）
- **注目SaaS/開発事例**: （1行要約）

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
* **【マネタイズ・グロースのポイント】**
* **【日本で真似・応用するヒント】**

---

## 🛠️ 【即実践】本日の実利アセット（500円以上の価値を即回収）

### 1. 💻 コピペで即デプロイできる自動化コード（Python / TypeScript）
（本日のトピックやSaaS事例に関連し、読者の開発時間を大幅削減する実用的な自動化スクリプト・API連携コードをそのまま貼る）

```python
# ここに実用的なコードを出力
