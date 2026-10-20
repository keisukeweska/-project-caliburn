import os
import json
from google import genai

def generate_with_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY が設定されていません。")
        return None

    try:
        client = genai.Client(api_key=api_key)
        
        # 1. 現在使えるモデルの一覧を自動取得して、生成に使える（generateContent対応の）ものを探す
        available_models = []
        for m in client.models.list():
            # generateContentメソッドがサポートされているモデルを抽出
            if "generateContent" in getattr(m, "supported_generation_methods", []):
                available_models.append(m.name)
        
        print(f"利用可能なモデル一覧: {available_models}")

        # 2. 優先的に使いたいモデルの候補リスト（flash系を優先）
        preferred_models = [
            "gemini-3.8-flash",
            "gemini-2.5-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro"
        ]

        # 優先リストの中で、実際に現在利用可能なモデルがあればそれを選択
        target_model = None
        for pref in preferred_models:
            # "models/gemini-..." のような完全一致または部分一致を探す
            matched = [m for m in available_models if pref in m]
            if matched:
                target_model = matched[0]
                break
        
        # 優先リストに見つからなければ、利用可能なモデルの先頭を使う
        if not target_model and available_models:
            target_model = available_models[0]

        if not target_model:
            print("利用可能なGeminiモデルが見つかりませんでした。")
            return None

        print(f"使用するモデル: {target_model}")

        # 3. 選択されたモデルで生成を実行
        response = client.models.generate_content(
            model=target_model,
            contents=prompt,
        )
        return response.text

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

    # AIへのプロンプト作成
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
