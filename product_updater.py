"""
╔══════════════════════════════════════════════════════════╗
║         AMAZON PRODUCT AUTO-UPDATER                      ║
║  Amazon India bestsellers se automatically products      ║
║  fetch karo aur config.py mein update karo               ║
╚══════════════════════════════════════════════════════════╝
"""

import requests
from bs4 import BeautifulSoup
import re
import os
import json
import time
import random
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("updater")

AFFILIATE_TAG = "rahulfinds20c-21"

# ─── CATEGORIES TO SCRAPE ─────────────────────────────────
# Amazon India bestseller category URLs
CATEGORIES = [
    {
        "name": "Smartphones",
        "url": "https://www.amazon.in/gp/bestsellers/electronics/1389401031/",
        "category": "electronics",
        "emoji": "📱",
        "commission_pct": 0.04,
        "price_max": 60000   # Sanity check — phones above this are skipped
    },
    {
        "name": "Budget Phones",
        "url": "https://www.amazon.in/gp/bestsellers/electronics/1389401031/ref=zg_bs_nav_electronics_2_1389399031",
        "category": "electronics",
        "emoji": "📱",
        "commission_pct": 0.04,
        "price_max": 20000
    },
]

# ─── REALISTIC BROWSER HEADERS ────────────────────────────
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9,hi;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}


def get_bestsellers(category: dict, max_products: int = 5) -> list:
    """Amazon bestsellers page se products scrape karo"""
    try:
        log.info(f"   Fetching: {category['name']}...")
        time.sleep(random.uniform(2, 4))  # Polite delay

        session = requests.Session()
        session.headers.update(HEADERS)

        resp = session.get(category["url"], timeout=20)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        products = []

        is_search = category.get("search_mode", False)

        if is_search:
            # Amazon search results — div[data-asin] with s-result-item
            items = [d for d in soup.find_all("div", attrs={"data-asin": True})
                     if d.get("data-asin") and len(d.get("data-asin", "")) == 10]
        else:
            # Multiple CSS selectors for bestseller pages
            selectors = [
                "div.zg-grid-general-faceout",
                "li.zg-item-immersion",
                "div[class*='p13n-sc-uncoverable-faceout']",
                "div[data-asin]",
            ]
            items = []
            for sel in selectors:
                items = soup.select(sel)
                if items:
                    break
            if not items:
                items = soup.find_all("div", attrs={"data-asin": True})

        log.info(f"   Found {len(items)} items on page")

        for item in items[:max_products * 2]:  # Extra buffer for skips
            if len(products) >= max_products:
                break
            try:
                # Get ASIN
                asin = item.get("data-asin") or ""
                if not asin:
                    link_tag = item.select_one("a[href*='/dp/']")
                    if link_tag:
                        match = re.search(r'/dp/([A-Z0-9]{10})', link_tag.get('href', ''))
                        asin = match.group(1) if match else ""
                if not asin or len(asin) != 10:
                    continue

                # Get product name
                name = ""
                name_selectors = [
                    "._cDEzb_p13n-sc-css-line-clamp-3_g3dy1",
                    "._cDEzb_p13n-sc-css-line-clamp-4_2q2cc",
                    "span.a-size-small.a-link-normal",
                    "div.a-section span.a-truncate-cut",
                    "span[class*='line-clamp']",
                    "a.a-link-normal span",
                ]
                for ns in name_selectors:
                    el = item.select_one(ns)
                    if el and el.get_text(strip=True):
                        name = el.get_text(strip=True)
                        break
                if not name:
                    name = f"{category['name']} Product"

                # Clean name — keep first meaningful part
                name = name.split("|")[0].split("(")[0].strip()
                name = name[:45]

                # Get price
                price = 0
                price_selectors = [
                    "span.a-price span.a-offscreen",
                    "._cDEzb_p13n-sc-price_3mJ9Z",
                    "span.a-price-whole",
                    "span._cDEzb_p13n-sc-price_3mJ9Z",
                ]
                for ps in price_selectors:
                    el = item.select_one(ps)
                    if el:
                        price_text = el.get_text(strip=True)
                        # Strip paise/decimal part first (e.g. "15,999.00" → "15,999")
                        price_text = price_text.split('.')[0]
                        digits = re.sub(r'[^\d]', '', price_text)
                        if digits:
                            p_val = int(digits)
                            # Sanity: Indian phone prices are 3,000 to 2,00,000
                            if 1000 <= p_val <= 200000:
                                price = p_val
                                break

                if price == 0:
                    price = 10000  # Default fallback

                # Skip if price exceeds category max (wrong product)
                price_max = category.get("price_max", 200000)
                if price > price_max:
                    continue

                # Commission
                commission = max(int(price * category["commission_pct"]), 50)

                affiliate_link = f"https://www.amazon.in/dp/{asin}/?tag={AFFILIATE_TAG}"

                products.append({
                    "name": name,
                    "link": affiliate_link,
                    "category": category["category"],
                    "benefit": f"Rs {price:,} mein {category['name']} — Amazon Bestseller",
                    "commission": commission,
                    "emoji": category["emoji"],
                })

                log.info(f"      ✅ {name[:35]} — ₹{price:,}")

            except Exception as e:
                log.debug(f"Item parse error: {e}")
                continue

        return products

    except requests.RequestException as e:
        log.error(f"   ❌ Network error for {category['name']}: {e}")
        return []
    except Exception as e:
        log.error(f"   ❌ Error: {e}")
        return []


def update_config_products(new_products: list):
    """config.py ke PRODUCTS block ko update karo"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py")

    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Build new PRODUCTS block
    lines = ["PRODUCTS = ["]
    for p in new_products:
        lines.append("    {")
        lines.append(f'        "name": {json.dumps(p["name"], ensure_ascii=False)},')
        lines.append(f'        "link": {json.dumps(p["link"])},')
        lines.append(f'        "category": {json.dumps(p["category"])},')
        lines.append(f'        "benefit": {json.dumps(p["benefit"], ensure_ascii=False)},')
        lines.append(f'        "commission": {p["commission"]},')
        lines.append(f'        "emoji": {json.dumps(p["emoji"], ensure_ascii=False)},')
        lines.append("    },")
    lines.append("]")
    new_products_block = "\n".join(lines)

    # Replace old PRODUCTS block
    # Use lambda to avoid re interpreting backslashes/unicode in replacement
    new_content = re.sub(
        r'PRODUCTS\s*=\s*\[.*?\]',
        lambda m: new_products_block,
        content,
        flags=re.DOTALL
    )

    if new_content == content:
        log.warning("⚠️  PRODUCTS block replace nahi hua — manually check karo")
        return False

    # Backup original
    backup_path = config_path + ".backup"
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open(config_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    log.info(f"✅ config.py updated! (Backup: config.py.backup)")
    return True


def run_updater():
    print()
    print("=" * 58)
    print("  🔍 AMAZON PRODUCT AUTO-UPDATER")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print("=" * 58)
    print()
    print("  Amazon India bestsellers se products fetch ho raha hai...")
    print("  (2-4 seconds delay between each — anti-block)")
    print()

    all_products = []

    for cat in CATEGORIES:
        products = get_bestsellers(cat, max_products=3)  # Top 3 per category
        all_products.extend(products)
        if products:
            print(f"  {cat['emoji']} {cat['name']}: {len(products)} products mila")
        else:
            print(f"  ❌ {cat['name']}: fetch failed (Amazon ne block kiya ho sakta hai)")

    print()

    if not all_products:
        print("❌ Koi bhi product nahi mila!")
        print()
        print("Possible reason: Amazon ne scraping block kar diya.")
        print("Solution: Kuch minutes baad dobara try karo.")
        return

    # Remove duplicates by link
    seen = set()
    unique_products = []
    for p in all_products:
        if p["link"] not in seen:
            seen.add(p["link"])
            unique_products.append(p)

    print(f"  Total unique products found: {len(unique_products)}")
    print()
    print("  Products jo config mein jayenge:")
    print("  " + "-" * 50)
    for i, p in enumerate(unique_products, 1):
        print(f"  {i:2}. {p['emoji']} {p['name'][:40]}")
        print(f"       {p['benefit']}")
        print(f"       Commission: ₹{p['commission']}")
        print()

    # Update config.py
    success = update_config_products(unique_products)

    if success:
        print("=" * 58)
        print(f"  ✅ {len(unique_products)} products config.py mein update ho gaye!")
        print("  Ab autopilot inhe automatically use karega.")
        print("  Purana config backup: config.py.backup")
        print("=" * 58)
    else:
        print("❌ Config update fail hua — manually check karo")


if __name__ == "__main__":
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        import subprocess
        print("Installing beautifulsoup4...")
        subprocess.run(["pip", "install", "beautifulsoup4", "requests", "-q"])
        from bs4 import BeautifulSoup

    run_updater()
    print()
    input("Press Enter to exit...")
