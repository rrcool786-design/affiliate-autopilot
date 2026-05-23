"""GitHub Actions autopilot post script"""
import openai, requests, random, re, os
from datetime import datetime

GROQ_API_KEY        = os.environ.get("GROQ_API_KEY", "")
TELEGRAM_BOT_TOKEN  = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "@TechDealsIndia_channel")

PRODUCTS = [
    {"name": "Redmi A7 Pro 5G", "link": "https://www.amazon.in/dp/B0GS5Y6BD3/?tag=rahulfinds20c-21", "category": "electronics", "benefit": "Rs 15,999 mein 5G phone - fastest processor + all day battery", "commission": 640, "emoji": "📱"},
    {"name": "OnePlus Buds 3r", "link": "https://www.amazon.in/dp/B0FMDL81GS/?tag=rahulfinds20c-21", "category": "electronics", "benefit": "Rs 1,999 mein 54 hour battery earbuds - ANC + noise cancellation", "commission": 160, "emoji": "🎧"},
    {"name": "iQOO Z10R 5G", "link": "https://www.amazon.in/dp/B0FHB5V36G/?tag=rahulfinds20c-21", "category": "electronics", "benefit": "Rs 22,999 mein AMOLED 5G phone - 4K camera + curved display", "commission": 920, "emoji": "🤳"},
    {"name": "OnePlus Nord CE6 Lite", "link": "https://www.amazon.in/dp/B0GVYDLJJQ/?tag=rahulfinds20c-21", "category": "electronics", "benefit": "Rs 17,999 mein 5G phone - OnePlus quality, budget price", "commission": 720, "emoji": "📱"},
]
POST_STYLES = ["personal story", "problem solution", "before/after", "quick tip", "question hook"]
HASHTAGS = {"electronics": "#Gadgets #Tech #Smartphone #Electronics #AmazonIndia"}

def generate_post(p, style):
    client = openai.OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
    h = HASHTAGS.get(p["category"], "#AmazonIndia")
    prompt = f"Ek viral Telegram post likho. Product: {p['name']} {p['emoji']}. Benefit: {p['benefit']}. Link: {p['link']}. Style: {style}. Hashtags: {h}. Rules: Hinglish, 2-4 lines, link plain text alag line, hashtags end mein. Sirf post do."
    try:
        r = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":prompt}], max_tokens=180, temperature=0.9)
        raw = r.choices[0].message.content.strip()
        return re.sub(r'\[.*?\]\((https?://[^)]+)\)', r'\1', raw)
    except:
        return f"{p['emoji']} {p['name']}\n\n{p['link']}\n\n{h}"

def post_to_telegram(msg):
    r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHANNEL_ID, "text": msg, "disable_web_page_preview": False}, timeout=15).json()
    if r.get("ok"):
        print(f"Posted: https://t.me/{TELEGRAM_CHANNEL_ID.replace('@','')}/{r['result']['message_id']}")
        return True
    print(f"Error: {r.get('description')}"); return False

if __name__ == "__main__":
    print(f"[{datetime.now().strftime('%d %b %Y %H:%M')} IST]")
    if not GROQ_API_KEY or not TELEGRAM_BOT_TOKEN: exit(1)
    p = random.choice(PRODUCTS)
    exit(0 if post_to_telegram(generate_post(p, random.choice(POST_STYLES))) else 1)
