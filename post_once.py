"""
GitHub Actions - ek post karo, band ho jao.

3-LAYER BULLETPROOF PRODUCT SYSTEM:
  Layer 1: Live Amazon scraping (har run pe fresh)
  Layer 2: products.json (weekly updated, repo mein stored)
  Layer 3: Emergency hardcoded backup (kabhi fail nahi hoga)
"""

import openai
import requests
import random
import re
import os
import json
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
PRODUCTS_JSON       = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.json")

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
EMERGENCY_PRODUCTS = [
    {"name": "Redmi A7 Pro 5G",      "link": "https://www.amazon.in/dp/B0GS5Y6BD3/?tag=rahulfinds20c-21",  "category": "electronics", "benefit": "Rs 15,999 mein best 5G phone",           "commission": 640, "emoji": "📱"},
    {"name": "OnePlus Buds 3r",       "link": "https://www.amazon.in/dp/B0FMDL81GS/?tag=rahulfinds20c-21", "category": "electronics", "benefit": "Rs 1,999 mein 54hr battery ANC earbuds", "commission": 160, "emoji": "🎧"},
    {"name": "iQOO Z10R 5G",          "link": "https://www.amazon.in/dp/B0FHB5V36G/?tag=rahulfinds20c-21", "category": "electronics", "benefit": "Rs 22,999 mein AMOLED 5G + 4K camera",   "commission": 920, "emoji": "🤳"},
    {"name": "OnePlus Nord CE6 Lite", "link": "https://www.amazon.in/dp/B0GVYDLJJQ/?tag=rahulfinds20c-21", "category": "electronics", "benefit": "Rs 17,999 mein OnePlus 5G phone",        "commission": 720, "emoji": "📱"},
]
POST_STYLES = ["personal story", "problem solution format", "before/after comparison", "quick tip with product", "question hook", "deal alert urgency", "vs expensive comparison"]
HASHTAGS = {
    "electronics": "#Gadgets #Tech #Smartphone #AmazonIndia #BestDeals",
    "computers": "#Laptop #Tech #Computer #AmazonIndia #BestDeals",
    "kitchen": "#Kitchen #HomeAppliances #AmazonIndia #BestDeals",
    "home": "#HomeDecor #HomeAppliances #AmazonIndia #BestDeals",
    "fashion": "#Fashion #Style #AmazonIndia #BestDeals",
    "sports": "#Sports #Fitness #AmazonIndia #BestDeals",
    "beauty": "#Beauty #Skincare #AmazonIndia #BestDeals",
    "books": "#Books #Reading #AmazonIndia #BestDeals",
    "toys": "#Toys #Kids #AmazonIndia #BestDeals",
    "health": "#Health #Wellness #AmazonIndia #BestDeals",
    "default": "#AmazonIndia #BestDeals #OnlineShopping",
}

def layer1_live_scrape():
    if not BS4_AVAILABLE:
        return []
    cats = random.sample(BESTSELLER_URLS, min(3, len(BESTSELLER_URLS)))
    products = []
    for cat in cats:
        try:
            headers = dict(random.choice(HEADERS_LIST))
            headers["Accept"] = "text/html,*/*;q=0.8"
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
                    if not asin:
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
                            name = el.get_text(strip=True).split("|")[0].strip()[:55]
                            break
                    if not name:
                        name = f"Amazon {cat['category'].title()} Deal"
                    price = 0
                    for ps in ["span.a-price span.a-offscreen","._cDEzb_p13n-sc-price_3mJ9Z","span.a-price-whole"]:
                        el = item.select_one(ps)
                        if el:
                            d = re.sub(r'[^\d]','',el.get_text(strip=True).split('.')[0])
                            if d:
                                pv = int(d)
                                if 50 <= pv <= 500000:
                                    price = pv
                                    break
                    if not price:
                        price = 999
                    products.append({"name": name, "link": f"https://www.amazon.in/dp/{asin}/?tag={AFFILIATE_TAG}", "category": cat["category"], "benefit": f"Rs {price:,} mein Amazon bestseller trending {cat['category']}", "commission": max(int(price*cat["commission_pct"]),40), "emoji": cat["emoji"]})
                    count += 1
                except:
                    continue
            if count:
                print(f"   [L1] {cat['emoji']} {cat['category']}: {count} live products")
        except Exception as e:
            print(f"   [L1] {cat['category']}: {e}")
    return products

def layer2_json_products():
    try:
        if not os.path.exists(PRODUCTS_JSON):
            print("   [L2] products.json nahi mila")
            return []
        with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        products = data.get("products", [])
        if not products:
            return []
        print(f"   [L2] products.json: {len(products)} products (updated: {data.get('updated_at','?')})")
        return products
    except Exception as e:
        print(f"   [L2] Error: {e}")
        return []

def generate_post(product, style):
    hashtags = HASHTAGS.get(product.get("category","default"), HASHTAGS["default"])
    prompt = f"""Ek viral Telegram post likho.
Product: {product['name']} {product['emoji']}
Benefit: {product['benefit']}
Link: {product['link']}
Style: {style} — Hinglish, 2-4 lines, real user jaisa, link PLAIN TEXT alag line pe, hashtags end mein, hook first line, 2-3 emojis.
Hashtags: {hashtags}
Sirf post text do."""
    try:
        r = openai.OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1").chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":prompt}], max_tokens=200, temperature=0.9)
        raw = r.choices[0].message.content.strip()
        return re.sub(r'\[.*?\]\((https?://[^)]+)\)', r'\1', raw)
    except Exception as e:
        print(f"   AI error: {e}")
        return f"{product['emoji']} {product['name']} - {product['benefit']}\n\n{product['link']}\n\n{hashtags}"

def post_to_telegram(msg):
    d = requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={"chat_id": TELEGRAM_CHANNEL_ID, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": False}, timeout=15).json()
    if d.get("ok"):
        print(f"   Posted: https://t.me/{TELEGRAM_CHANNEL_ID.replace('@','')}/{d['result']['message_id']}")
        return True
    print(f"   Error: {d.get('description')}")
    return False

if __name__ == "__main__":
    print(f"\nAuto-post [{datetime.now().strftime('%d %b %Y %H:%M')} IST]")
    if not GROQ_API_KEY or not TELEGRAM_BOT_TOKEN:
        print("ERROR: API keys missing!")
        exit(1)

    print("Layer 1: Amazon live scraping...")
    products = layer1_live_scrape()
    source = "Amazon Live"

    if not products:
        print("Layer 2: products.json cache...")
        products = layer2_json_products()
        source = "products.json cache"

    if not products:
        print("Layer 3: Emergency hardcoded backup...")
        products = EMERGENCY_PRODUCTS
        source = "Emergency Backup"

    product = random.choice(products)
    style = random.choice(POST_STYLES)
    print(f"\nSource: {source} | Product: {product['name']} | Style: {style}")
    post_text = generate_post(product, style)
    print(f"\nPost:\n{post_text}\n")
    success = post_to_telegram(post_text)
    exit(0 if success else 1)
