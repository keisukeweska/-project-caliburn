import os
import json
import requests

def fetch_ai_news():
    print("【ベルダンディ】海外AI最新情報の自動収集を開始します...")
    
    # サンプルデータ（将来的にAPIやスクレイピングで取得するデータ）
    sample_data = [
        {"title": "New AI Tool Released", "url": "https://example.com"}
    ]
    
    print(f"収集完了: {len(sample_data)} 件の情報を取得しました。")
    
    # データをJSONファイルとして保存（エクスカリバーに渡すため）
    os.makedirs("data", exist_ok=True)
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=4)
        
    print("【ベルダンディ】データを data/news.json に保存しました。")

if __name__ == "__main__":
    fetch_ai_news()
