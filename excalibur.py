import os
import time
import feedparser
import urllib.request
from google import genai

# リクエスト拒否を防ぐための標準的なUser-Agentヘッダー
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# ハイブリッド情報源（AIニュース ＋ 海外個人開発・SaaS・開発者コミュニティ）
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

    # 読者が「絶対払う」レベルの圧倒的実利アセットを毎朝自動生成するプロンプト
    prompt = (
        "あなたは月額500円の有料マガジンで数千人の有料会員を抱えるトップAI・SaaSシニアアナリスト兼プロダクトエンジニアです。\n"
        f"提供された【本日取得した海外データ一覧】（計{len(news_list)}件）から厳選し、読者が「500円どころか5,000円の価値がある」と衝撃を受けるレベルの実用・実践型プレミアムレポートを執筆してください。\n\n"
        "【本日取得した海外データ一覧】\n"
        f"{news_text}\n\n"
        "---\n\n"
        "【執筆およびnote最適化ルール】\n\n"
        "1. **トーン＆マナー**:\n"
        "   - 定型的なAI文体（「〜を解説します」「いかがでしたか」等）は完全排除。\n"
        "   - 業界の裏まで知り尽くしたプロの切れ味ある文体（「〜だ」「〜と言える」「正直ここは〜だ」）で執筆すること。\n\n"
        "2. **構成テンプレ（note有料ライン対応）**:\n\n"
        "# 🚀 【日刊AI＆海外SaaS動向】（鋭い見出し・ビジネス視点）\n\n"
        "> 💡 **今朝のインサイト（アナリストの眼）**\n"
        "> （海外の動向から見えてきたAI業界・SaaSビジネスの「潮目・狙い目」を2〜3行で鋭く指摘）\n\n"
        "## ⚡ 1分で掴む！今朝の3行要約（TL;DR）\n"
        "- **AIトピック1**: （1行要約）\n"
        "- **AIトピック2**: （1行要約）\n"
        "- **注目SaaS/開発事例**: （1行要約）\n\n"
        "---\n"
        "<!-- note有料ライン -->\n"
        "---\n\n"
        "## 🔍 今朝の厳選解説（AIトレンド ✕ 海外SaaSマネタイズ）\n\n"
        "### 1. [AIトピック1のタイトル]\n"
        "> 📌 **ここだけ抑えればOK**: \n"
        "> 🌐 **一次ソース**: [公式記事リンク](URL)\n\n"
        "* **【何が起きたのか】**\n"
        "* **【裏の構造・競合比較】**\n"
        "* **【日本企業・現場へのインパクト】**\n\n"
        "### 2. [AIトピック2のタイトル]\n"
        "> 📌 **ここだけ抑えればOK**: \n"
        "> 🌐 **一次ソース**: [公式記事リンク](URL)\n\n"
        "* **【何が起きたのか】**\n"
        "* **【裏の構造・競合比較】**\n"
        "* **【日本企業・現場へのインパクト】**\n\n"
        "### 3. 🔥【注目の海外SaaS・個人開発分析】[3つ目のタイトル]\n"
        "> 📌 **ここだけ抑えればOK**: \n"
        "> 🌐 **一次ソース**: [公式記事リンク](URL)\n\n"
        "* **【どんなプロダクト・事例か】**\n"
        "* **【マネタイズ・グロースのポイント】**\n"
        "* **【日本で真似・応用するヒント】**\n\n"
        "---\n\n"
        "## 🛠️ 【即実践】本日の実利アセット（500円以上の価値を即回収）\n\n"
        "### 1. 💻 コピペで即デプロイできる自動化コード\n"
        "（本日のトピックやSaaS事例に関連し、読者の開発時間を大幅削減する実用的な自動化スクリプト・API連携コードをここに実コードとして出力する）\n\n"
        "### 2. 🤖 実務特化型・超精密システムプロンプト\n"
        "（業務や自社プロダクトの検証でそのままChatGPT/ClaudeのSystem Promptにコピペして使える、制約条件・出力形式がカチカチに組み込まれた実用プロンプトをここに出力する）\n\n"
        "### 3. 📊 購読者限定スプレッドシート（海外SaaSデータベース）\n"
        "> 💡 本マガジン購読者限定で、本日紹介したプロダクトを含む「海外未上陸SaaS・月商データ・技術スタック一覧データベース」を更新中。\n"
        "> 👉 [限定スプレッドシートを開く](https://docs.google.com/spreadsheets/d/1R877xVvo3KWSciMV3GtxIji091-l_trk99FZZc2LcHI/edit?usp=sharing)\n\n"
        "---\n"
        "※実在するデータのみ扱い、架空のツール名は絶対に使用しないでください。"
    )

    candidate_models = [
        "gemini-3.8-flash",
        "gemini-flash-latest"
    ]

    response = None
    for attempt in range(1, 4):
        print(f"【カリバーン】圧倒的価値プレミアム記事生成トライアル #{attempt}...")
        for model_name in candidate_models:
            try:
                print(f"【カリバーン】モデル '{model_name}' で執筆中...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                print(f"【カリバーン】成功: 500円以上の実利価値を持つ記事を生成しました。")
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
    
    print("【カリバーン】『月額500円・圧倒的実利仕様』の記事生成が完了しました！")

if __name__ == "__main__":
    generate_article()
