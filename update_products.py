"""
Weekly Amazon India bestsellers fetch karo aur products.json mein save karo.
GitHub Actions se Sunday 06:00 IST pe automatically run hota hai.
products.json repo mein commit hota hai — post_once.py ise Layer 2 fallback ke taur pe use karta hai.
"""

import requests
import random
import re
import json
import os
import sys
from datetime import datetime

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

AFFILIATE_TAG = "rahulfinds20c-21"
OUTPUT_FILE   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.json")

# ─── SAB CATEGORIES ──────────────────────────────────────────────────
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
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "Accept-Language": "en-IN,en;q=0.9"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", "Accept-Language": "en-US,en;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36", "Accept-Language": "en-GB,en;q=0.7"},
]

import time


def scrape_category(cat, max_products=5):
    """Ek category ke top products fetch karo"""
    try:
        time.sleep(random.uniform(2, 4))  # Polite delay — anti-block
        headers = dict(random.choice(HEADERS_LIST))
        headers["Accept"]          = "text/html,application/xhtml+xml,*/*;q=0.8"
        headers["Accept-Encoding"] = "gzip, deflate, br"
        headers["Connection"]      = "keep-alive"

        resp = requests.Session().get(cat["url"], headers=headers, timeout=20)
        if resp.status_code != 200:
            print(f"   {cat['category']}: HTTP {resp.status_code} — skip")
            return []

        soup  = BeautifulSoup(resp.text, "html.parser")
        items = []
        for sel in ["div.zg-grid-general-faceout", "li.zg-item-immersion",
                    "div[class*='p13n-sc-uncoverable-faceout']", "div[data-asin]"]:
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
                # ASIN
                asin = item.get("data-asin", "")
                if not asin:
                    a = item.select_one("a[href*='/dp/']")
                    if a:
                        m = re.search(r'/dp/([A-Z0-9]{10})', a.get('href', ''))
                        asin = m.group(1) if m else ""
                if not asin or len(asin) != 10:
                    continue

                # Name
                name = ""
                for ns in ["._cDEzb_p13n-sc-css-line-clamp-3_g3dy1",
                           "._cDEzb_p13n-sc-css-line-clamp-4_2q2cc",
                           "span.a-size-small.a-link-normal",
                           "span[class*='line-clamp']",
                           "a.a-link-normal span"]:
                    el = item.select_one(ns)
                    if el and el.get_text(strip=True):
                        name = el.get_text(strip=True).split("|")[0].split("(")[0].strip()[:55]
                        break
                if not name:
                    name = f"Amazon {cat['category'].title()} Bestseller"

                # Price
                price = 0
                for ps in ["span.a-price span.a-offscreen",
                           "._cDEzb_p13n-sc-price_3mJ9Z",
                           "span.a-price-whole"]:
                    el = item.select_one(ps)
                    if el:
                        pt     = el.get_text(strip=True).split('.')[0]
                        digits = re.sub(r'[^\d]', '', pt)
                        if digits:
                            pv = int(digits)
                            if 50 <= pv <= 500000:
                                price = pv
                                break
                if not price:
                    price = 999

                products.append({
                    "name":       name,
                    "link":       f"https://www.amazon.in/dp/{asin}/?tag={AFFILIATE_TAG}",
                    "category":   cat["category"],
                    "benefit":    f"Rs {price:,} mein Amazon bestseller — trending {cat['category']} product",
                    "commission": max(int(price * cat["commission_pct"]), 40),
                    "emoji":      cat["emoji"],
                })
            except Exception:
                continue

        print(f"   {cat['emoji']} {cat['category']}: {len(products)} products")
        return products

    except Exception as e:
        print(f"   {cat['category']} error: {e}")
        return []


def run_update():
    if not BS4_AVAILABLE:
        print("ERROR: beautifulsoup4 not installed! Run: pip install beautifulsoup4")
        sys.exit(1)

    print("=" * 55)
    print(f"  AMAZON PRODUCTS WEEKLY UPDATE")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p IST')}")
    print("=" * 55)
    print()

    all_products = []
    for cat in CATEGORIES:
        products = scrape_category(cat, max_products=3)
        all_products.extend(products)

    # Duplicates hataao (same ASIN)
    seen  = set()
    clean = []
    for p in all_products:
        asin = p["link"].split("/dp/")[1].split("/")[0]
        if asin not in seen:
            seen.add(asin)
            clean.append(p)

    print()
    print(f"  Total unique products: {len(clean)}")

    if len(clean) == 0:
        print("  ERROR: Koi product nahi mila — products.json update nahi hoga")
        print("  Reason: Amazon ne iss run mein block kiya hoga.")
        print("  Previous products.json safe hai.")
        sys.exit(1)

    # Save to products.json
    data = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M IST"),
        "total":      len(clean),
        "products":   clean,
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  products.json saved — {len(clean)} products")
    print()
    print("  Products:")
    print("  " + "-" * 45)
    for i, p in enumerate(clean, 1):
        print(f"  {i:2}. {p['emoji']} {p['name'][:40]}")
        print(f"       {p['benefit']}")
        print(f"       Commission: Rs {p['commission']}")
    print()
    print("=" * 55)
    print("  Done! GitHub Actions ab ise commit karega.")
    print("=" * 55)


if __name__ == "__main__":
    run_update()
