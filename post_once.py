"""
GitHub Actions ke liye — ek baar chalega, ek post karega, band ho jayega.
Ab LIVE market research karta hai — Amazon India se trending products fetch karta hai (sab categories).
Fallback: hardcoded products (agar Amazon block kare).
"""

import openai
import requests
import random
import re
import os
from datetime import datetime

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

GROQ_API_KEY        = os.environ.get("GROQ_API_KEY", "")
TELEGRAM_BOT_TOKEN  = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "@TechDealsIndia_channel")
AFFILIATE_TAG       = "rahulfinds20c-21"

BESTSELLER_URLS = [
    {"url": "https://www.amazon.in/gp/bestsellers/electronics/",    "category": "electronics", "emoji": "📱", "commission_pct": 0.04},
    {"url": "https://www.amazon.in/gp/bestsellers/computers/",      "category": "computers",   "emoji": "💻", "commission_pct": 0.04},
    {"url": "https://www.amazon.in/gp/bestsellers/kitchen/",        "category": "kitchen",     "emoji": "🍳", "commission_pct": 0.05},
    {"url": "https://www.amazon.in/gp/bestsellers/home/",           "category": "home",        "emoji": "🏠", "commission_pct": 0.05},
    {"url": "https://www.amazon.in/gp/bestsellers/apparel/",        "category": "fashion",     "emoji": "👕", "commission_pct": 0.09},
    {"url": "https://www.amazon.in/gp/bestsellers/sporting-goods/", "category": "sports",      "emoji": "⚽", "commission_pct": 0.05},
    {"url": "https://www.amazon.in/gp/bestsellers/beauty/",         "category": "beauty",      "emoji": "💄", "commission_pct": 0.06},
    {"url": "https://www.amazon.in/gp/bestsellers/books/",          "category": "books",       "emoji": "📚", "commission_pct": 0.05},
    {"url": "https://www.amazon.in/gp/bestsellers/toys/",           "category": "toys",        "emoji": "🧸", "commission_pct": 0.05},
    {"url": "https://www.amazon.in/gp/bestsellers/health/",         "category": "health",      "emoji": "💊", "commission_pct": 0.05},
]

HEADERS_LIST = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36", "Accept-Language": "en-IN,en;q=0.9"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36", "Accept-Language": "en-US,en;q=0.8"},
]

FALLBACK_PRODUCTS = [
    {"name": "Redmi A7 Pro 5G",      "link": "https://www.amazon.in/dp/B0GS5Y6BD3/?tag=rahulfinds20c-21",  "category": "electronics", "benefit": "Rs 15,999 mein best 5G phone",            "commission": 640, "emoji": "📱"},
    {"name": "OnePlus Buds 3r",       "link": "https://www.amazon.in/dp/B0FMDL81GS/?tag=rahulfinds20c-21", "category": "electronics", "benefit": "Rs 1,999 mein 54hr battery ANC earbuds",  "commission": 160, "emoji": "🎧"},
    {"name": "iQOO Z10R 5G",          "link": "https://www.amazon.in/dp/B0FHB5V36G/?tag=rahulfinds20c-21", "category": "electronics", "benefit": "Rs 22,999 mein AMOLED 5G + 4K camera",    "commission": 920, "emoji": "🤳"},
    {"name": "OnePlus Nord CE6 Lite", "link": "https://www.amazon.in/dp/B0GVYDLJJQ/?tag=rahulfinds20c-21", "category": "electronics", "benefit": "Rs 17,999 mein OnePlus 5G phone",         "commission": 720, "emoji": "📱"},
]

POST_STYLES = [
    "personal story — meri apni experience share karo",
    "problem solution format — user ka pain point pehle",
    "before/after — pehle vs ab comparison",
    "quick tip format — ek useful tip with product mention",
    "question se start karo — curiosity hook",
    "deal alert — LIMITED TIME feel, urgency create karo",
    "comparison — yeh product vs expensive alternatives",
]

HASHTAGS = {
    "electronics": "#Gadgets #Tech #Smartphone #Electronics #AmazonIndia #BestDeals",
    "computers":   "#Laptop #Tech #Computer #AmazonIndia #BestDeals",
    "kitchen":     "#Kitchen #HomeAppliances #Cooking #AmazonIndia #BestDeals",
    "home":        "#HomeDecor #HomeAppliances #AmazonIndia #BestDeals",
    "fashion":     "#Fashion #Style #Clothing #AmazonIndia #BestDeals",
    "sports":      "#Sports #Fitness #Workout #AmazonIndia #BestDeals",
    "beauty":      "#Beauty #Skincare #Makeup #AmazonIndia #BestDeals",
    "books":       "#Books #Reading #SelfImprovement #AmazonIndia #BestDeals",
    "toys":        "#Toys #Kids #ParentingIndia #AmazonIndia #BestDeals",
    "health":      "#Health #Wellness #Fitness #AmazonIndia #BestDeals",
    "default":     "#AmazonIndia #BestDeals #OnlineShopping #IndianShopper",
}


def fetch_trending_products():
    if not BS4_AVAILABLE:
        return []
    cats = random.sample(BESTSELLER_URLS, min(3, len(BESTSELLER_URLS)))
    products = []
    for cat in cats:
        try:
            headers = dict(random.choice(HEADERS_LIST))
            headers["Accept"] = "text/html,application/xhtml+xml,*/*;q=0.8"
            headers["Accept-Encoding"] = "gzip, deflate, br"
            resp = requests.Session().get(cat["url"], headers=headers, timeout=15)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            items = []
            for sel in ["div.zg-grid-general-faceout", "li.zg-item-immersion", "div[data-asin]"]:
                items = soup.select(sel)
                if items:
                    break
            count = 0
            for item in items[:15]:
                if count >= 2:
                    break
                try:
                    asin = item.get("data-asin", "")
                    if not asin or len(asin) != 10:
                        a = item.select_one("a[href*='/dp/']")
                        if a:
                            m = re.search(r'/dp/([A-Z0-9]{10})', a.get('href',''))
                            asin = m.group(1) if m else ""
                    if not asin or len(asin) != 10:
                        continue
                    name = ""
                    for ns in ["._cDEzb_p13n-sc-css-line-clamp-3_g3dy1","span.a-size-small.a-link-normal","a.a-link-normal span"]:
                        el = item.select_one(ns)
                        if el and el.get_text(strip=True):
                            name = el.get_text(strip=True).split("|")[0].strip()[:50]
                            break
                    if not name:
                        name = f"Amazon {cat['category'].title()} Deal"
                    price = 0
                    for ps in ["span.a-price span.a-offscreen","._cDEzb_p13n-sc-price_3mJ9Z","span.a-price-whole"]:
                        el = item.select_one(ps)
                        if el:
                            pt = el.get_text(strip=True).split('.')[0]
                            d = re.sub(r'[^\d]','',pt)
                            if d:
                                pv = int(d)
                                if 50 <= pv <= 500000:
                                    price = pv
                                    break
                    if not price:
                        price = 999
                    products.append({
                        "name": name,
                        "link": f"https://www.amazon.in/dp/{asin}/?tag={AFFILIATE_TAG}",
                        "category": cat["category"],
                        "benefit": f"Rs {price:,} mein Amazon trending {cat['category']}",
                        "commission": max(int(price * cat["commission_pct"]), 40),
                        "emoji": cat["emoji"],
                    })
                    count += 1
                except:
                    continue
            if count:
                print(f"   {cat['emoji']} {cat['category']}: {count} products mila")
        except Exception as e:
            print(f"   {cat['category']}: {e}")
    return products


def generate_post(product, style):
    client = openai.OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
    hashtags = HASHTAGS.get(product.get("category","default"), HASHTAGS["default"])
    prompt = f"""Ek viral Telegram post likho affiliate product ke liye.
Product: {product['name']} {product['emoji']}
Benefit: {product['benefit']}
Link: {product['link']}
Style: {style}
Hashtags: {hashtags}
Rules: Hinglish, 2-4 lines, real user jaisi baat, link PLAIN TEXT alag line pe, hashtags end mein, hook first line, 2-3 emojis.
Sirf post text do."""
    try:
        r = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":prompt}], max_tokens=200, temperature=0.9)
        raw = r.choices[0].message.content.strip()
        return re.sub(r'\[.*?\]\((https?://[^)]+)\)', r'\1', raw)
    except Exception as e:
        print(f"AI error: {e}")
        return f"{product['emoji']} {product['name']} — {product['benefit']}\n\n{product['link']}\n\n{hashtags}"


def post_to_telegram(msg):
    r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHANNEL_ID, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": False}, timeout=15)
    d = r.json()
    if d.get("ok"):
        print(f"Posted: https://t.me/{TELEGRAM_CHANNEL_ID.replace('@','')}/{d['result']['message_id']}")
        return True
    print(f"Error: {d.get('description')}")
    return False


if __name__ == "__main__":
    print(f"Auto-post [{datetime.now().strftime('%d %b %Y %H:%M')} IST]")
    if not GROQ_API_KEY or not TELEGRAM_BOT_TOKEN:
        print("API keys missing!")
        exit(1)
    print("\nAmazon India trending products fetch ho rahe hain (10 categories)...")
    trending = fetch_trending_products()
    if trending:
        product = random.choice(trending)
        print(f"Trending: {product['name']} ({product['category']})")
    else:
        product = random.choice(FALLBACK_PRODUCTS)
        print(f"Fallback: {product['name']}")
    style = random.choice(POST_STYLES)
    post_text = generate_post(product, style)
    print(f"\nPost:\n{post_text}\n")
    success = post_to_telegram(post_text)
    exit(0 if success else 1)
