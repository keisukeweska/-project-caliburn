import os
import time
import feedparser
import urllib.request
from google import genai

# リクエスト拒否を防ぐための標準的なUser-Agentヘッダー
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# 確実に取得可能な主要RSSフィード一覧
RSS_URLS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://news.ycombinator.com/rss",
    "https://www.producthunt.com/feed"
]

def fetch_latest_tech_news():
    news_items = []
    print("【カリバーン】海外AI・SaaS・開発者メディアから一括取得中...")
    
    for url in RSS_URLS:
        try:
            # User-Agentを指定してHTTPリクエストを作成し、403拒否を回避
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()
                feed = feedparser.parse(xml_data)
                
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

    prompt = (
        "あなたは月額500円の有料マガジンで数千人の有料会員を抱えるトップAI・SaaSシニアアナリスト兼プロダクトエンジニアです。\n"
        f"提供された【本日取得した海外データ一覧】（計{len(news_list)}件）から厳選し、読者が「500円どころか5,000円の価値がある」と衝撃を受けるレベルの実用・実践
