import os
import json

def generate_comparison_article():
    print("【エクスカリバー】データの読み込みと比較表・記事生成を開始します...")
    
    # ベルダンディが集めたデータを読み込む
    news_data = []
    data_path = "data/news.json"
    
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            news_data = json.load(f)
        print(f"データ読み込み成功: {len(news_data)} 件の情報を取得しました。")
    else:
        print("データが見つからないため、デフォルトデータを使用します。")
        news_data = [{"title": "Default AI Tool", "url": "https://example.com"}]

    # 比較表・記事のMarkdownを組み立て
    markdown_content = "# スマートAI比較ナビ - 本日の最新AIトレンド\n\n"
    markdown_content += "海外で話題の最新AIツール・サービスを自動比較・解説します。\n\n"
    markdown_content += "## 📊 本日の注目AI比較表\n\n"
    markdown_content += "| ツール名 | 特徴・概要 | 公式リンク |\n"
    markdown_content += "| :--- | :--- | :--- |\n"
    
    for item in news_data:
        title = item.get("title", "No Title")
        url = item.get("url", "#")
        markdown_content += f"| **{title}** | 自動収集された最新のAIプロダクト | [公式サイト]({url}) |\n"
        
    markdown_content += "\n---\n*この記事は Project-Caliburn (スマートAI比較ナビ) により全自動生成されています。*\n"
    
    # postsフォルダに出力
    os.makedirs("posts", exist_ok=True)
    output_path = "posts/latest_comparison.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print(f"【エクスカリバー】記事の生成が完了しました: {output_path}")

if __name__ == "__main__":
    generate_comparison_article()
