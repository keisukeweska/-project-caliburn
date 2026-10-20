import os
import json
import requests

def generate_with_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY が設定されていません。")
        return None

    # 最新の安定版 API エンドポイント
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Gemini API 呼び出しエラー: {e}")
        return None

def generate_comparison_article():
    print("【エクスカリバー】Gemini APIを活用したSEO比較記事の自動生成を開始します...")
    
    # データを読み込む
    data_path = "data/news.json"
    news_data = []
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            news_data = json.load(f)

    # AIへのプロンプト（指示書）作成
    prompt = f"""
以下の収集データをもとに、日本のユーザーに向けた『スマートAI比較ナビ』の最新記事を作成してください。

【収集データ】
{json.dumps(news_data, ensure_ascii=False, indent=2)}

【記事の要件】
1. タイトルは「【最新】注目の海外AI・SaaSツール比較解説」とする。
2. 最初に読者を惹きつける魅力的な導入文を入れる。
3. 収集データを元に、「ツール名」「特徴・概要」「公式リンク」を含んだ見やすいMarkdown形式の比較表を作成する。
4. 各ツールの詳細解説（どんな人におすすめか、何ができるか）を分かりやすく記載する。
5. 最後に記事のまとめと、末尾に「※この記事は Project-Caliburn (スマートAI比較ナビ) により全自動生成されています。」を入れる。
"""

    # Geminiで記事生成
    ai_article = generate_with_gemini(prompt)

    # APIエラー時などのフォールバック
    if not ai_article:
        ai_article = "# スマートAI比較ナビ - 最新AIトレンド\n\nAI生成に失敗したため、基本情報を出力します。\n"

    # ファイルに保存
    os.makedirs("posts", exist_ok=True)
    output_path = "posts/latest_comparison.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ai_article)
        
    print(f"【エクスカリバー】Geminiによる記事生成が完了しました: {output_path}")

if __name__ == "__main__":
    generate_comparison_article()
