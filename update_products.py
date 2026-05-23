update_products.py"""
Weekly Amazon India bestsellers fetch karo aur products.json mein save karo.
GitHub Actions: Sunday 05:30 IST pe automatically run hota hai.
products.json repo mein commit hota hai — post_once.py ise Layer 2 fallback ke taur pe use karta hai.
"""

import requests
import random
import re
import json
import os
import sys
import time
from datetime import datetime

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: pip install beautifulsoup4")
    sys.exit(1)

AFFILIATE_TAG = "rahulfinds20c-21"
OUTPUT_FILE   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.json")

CATEGORIES = [
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
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36", "Accept-Language": "en-GB,en;q=0.7"},
]


def scrape_category(cat, max_products=3):
    try:
        time.sleep(random.uniform(2, 4))
        headers = dict(random.choice(HEADERS_LIST))
        headers["Accept"] = "text/html,*/*;q=0.8"
        headers["Accept-Encoding"] = "gzip, deflate, br"
        resp = requests.Session().get(cat["url"], headers=headers, timeout=20)
        if resp.status_code != 200:
            print(f"   {cat['category']}: HTTP {resp.status_code}")
            return []
        soup = BeautifulSoup(resp.text, "html.parser")
        items = []
        for sel in ["div.zg-grid-general-faceout","li.zg-item-immersion","div[class*='p13n-sc-uncoverable-faceout']","div[data-asin]"]:
            items = soup.select(sel)
            if items:
                break
        if not items:
            items = soup.find_all("div", attrs={"data-asin": True})
        products = []
        for item in items[:max_products * 3]:
            if len(products) >= max_products:
                break
            try:
                asin = item.get("data-asin","")
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
                    name = f"Amazon {cat['category'].title()} Bestseller"
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
            except:
                continue
        print(f"   {cat['emoji']} {cat['category']}: {len(products)} products")
        return products
    except Exception as e:
        print(f"   {cat['category']} error: {e}")
        return []


def run_update():
    print("=" * 50)
    print(f"  WEEKLY PRODUCTS UPDATE")
    print(f"  {datetime.now().strftime('%d %B %Y %I:%M %p')}")
    print("=" * 50)

    all_products = []
    for cat in CATEGORIES:
        all_products.extend(scrape_category(cat, max_products=3))

    seen, clean = set(), []
    for p in all_products:
        asin = p["link"].split("/dp/")[1].split("/")[0]
        if asin not in seen:
            seen.add(asin)
            clean.append(p)

    print(f"\nTotal unique products: {len(clean)}")

    if not clean:
        print("ERROR: Koi product nahi mila — products.json update nahi hoga")
        sys.exit(1)

    data = {"updated_at": datetime.now().strftime("%Y-%m-%d %H:%M IST"), "total": len(clean), "products": clean}
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"products.json saved — {len(clean)} products ready!")


if __name__ == "__main__":
    run_update()
