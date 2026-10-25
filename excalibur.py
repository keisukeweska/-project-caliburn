import os
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else genai.Client()

# ==========================================
# 💰 あなたの紹介報酬が入るアフィリエイトリンク定義
# ==========================================
AFFILIATE_LINKS = {
    "Claude Code": "https://anthropic.com?ref=YOUR_AFFILIATE_ID", # 自分のIDに書き換えOK
    "GLM": "https://z.ai?ref=YOUR_AFFILIATE_ID",
    "MiniMax": "https://minimaxi.com?ref=YOUR_AFFILIATE_ID",
    "Kimi": "https://moonshot.cn?ref=YOUR_AFFILIATE_ID",
    "Qwen": "https://aliyun.com?ref=YOUR_AFFILIATE_ID"
}

def generate_comparison_page():
    prompt = f"""
    You are a professional conversion-focused SaaS affiliate marketer and tech analyst.
    Write a high-converting, comprehensive comparison guide in Markdown format focusing on the best AI coding tools and agents for developers in 2026.

    Target Tools to Compare:
    1. Claude Code (Anthropic) - Price: $20/mo
    2. GLM (Z.ai) - Price: $3/mo
    3. MiniMax - Price: $10/mo
    4. Kimi - Price: ~$7/wk
    5. Qwen (Alibaba) - Price: $10/mo

    Requirements:
    1. Create a clear comparison table (Tool, Price, Speed/TPS, Best For).
    2. Write an in-depth review of each tool, highlighting why developers should use them.
    3. **Crucial**: Naturally and aggressively embed these exact affiliate CTA links into the markdown where each tool is recommended:
       - Claude Code: {AFFILIATE_LINKS['Claude Code']}
       - GLM: {AFFILIATE_LINKS['GLM']}
       - MiniMax: {AFFILIATE_LINKS['MiniMax']}
       - Kimi: {AFFILIATE_LINKS['Kimi']}
       - Qwen: {AFFILIATE_LINKS['Qwen']}
    4. Output ONLY the raw Markdown content for a high-ranking affiliate landing page.
    """

    print("【カリバーン】高単価アフィリエイト比較LPを生成中...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

if __name__ == "__main__":
    print("🚀 [Caliburn] アフィリエイト直結型・比較LP生成モード起動...")
    
    os.makedirs("public", exist_ok=True)
    
    # GitHub Pagesのトップページとして公開されるよう public/index.md に保存
    markdown_content = generate_comparison_page()
    with open("public/index.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print("✅ 成功！ public/index.md にアフィリエイトリンク付き比較LPを出力しました。")
