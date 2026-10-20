import os
import json
from google import genai

def generate_with_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY が設定されていません。")
        return None

    client = genai.Client(api_key=api_key)

    # 今後モデルが更新されても上から順に試して動くものを自動選出する候補リスト
    candidate_models = [
        "gemini-flash-latest",
        "gemini-1.5-flash",
        "gemini-2.5-flash",
        "gemini-3.8-flash",
        "gemini-pro"
    ]

    for model_name in candidate_models:
        try:
            print(f"モデル '{model_name}' での生成を試行中...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            if response and response.text:
                print(f"成功: モデル '{model_name}' を使用して記事を生成しました。")
                return response.text
        except Exception as e:
            print(f"モデル '{model_name}' 試行失敗: {e}")
            continue

    print("すべてのモデル候補での生成に失敗しました。")
    return None

def generate_comparison_article():
    print("【エクスカリバー】Gemini APIを活用したSEO比較記事の自動生成を開始します...")
    
    data_path = "data/news.json"
    news_data = []
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            news_data = json.load(f)

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

    ai_article = generate_with_gemini(prompt)

    if not ai_article:
        ai_article = "# スマートAI比較ナビ - 最新AIトレンド\n\nAI生成に失敗したため、基本情報を出力します。\n"

    os.makedirs("posts", exist_ok=True)
    output_path = "posts/latest_comparison.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ai_article)
        
    print(f"【エクスカリバー】Geminiによる記事生成が完了しました: {output_path}")

if __name__ == "__main__":
    generate_comparison_article()
