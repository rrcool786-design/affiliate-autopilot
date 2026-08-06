"""
GitHub Actions — ek post karo, band ho jao.

3-LAYER BULLETPROOF PRODUCT SYSTEM:
  Layer 1: Live Amazon scraping (har run pe fresh products)
  Layer 2: products.json (weekly updated, repo mein stored — max 7 din purana)
  Layer 3: Hardcoded emergency backup (kabhi band nahi hoga)

Post HAMESHA hogi — koi bhi layer fail ho.
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

# ─── CONFIG ──────────────────────────────────────────────────────────
GROQ_API_KEY        = os.environ.get("GROQ_API_KEY", "")
TELEGRAM_BOT_TOKEN  = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "@TechDealsIndia_channel")
AFFILIATE_TAG       = "rahulfinds20c-21"

# products.json — same folder mein hoga
PRODUCTS_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.json")

# posted_asins.json — kaunse products post ho chuke, ye yaad rakhta hai.
# GitHub Actions ka runner har run ke baad mit jaata hai, isliye workflow
# is file ko wapas repo mein commit karta hai — tabhi memory tikti hai.
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "posted_asins.json")

# ─── AMAZON CATEGORIES ───────────────────────────────────────────────
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
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "Accept-Language": "en-IN,en;q=0.9"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", "Accept-Language": "en-US,en;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36", "Accept-Language": "en-GB,en;q=0.7"},
]

# ─── LAYER 3: EMERGENCY HARDCODED (last resort) ──────────────────────
EMERGENCY_PRODUCTS = [
    {"name": "Redmi A7 Pro 5G",      "link": f"https://www.amazon.in/dp/B0GS5Y6BD3/?tag={AFFILIATE_TAG}",  "category": "electronics", "benefit": "Rs 15,999 mein best 5G phone",           "commission": 640, "emoji": "📱"},
    {"name": "OnePlus Buds 3r",       "link": f"https://www.amazon.in/dp/B0FMDL81GS/?tag={AFFILIATE_TAG}", "category": "electronics", "benefit": "Rs 1,999 mein 54hr battery ANC earbuds", "commission": 160, "emoji": "🎧"},
    {"name": "iQOO Z10R 5G",          "link": f"https://www.amazon.in/dp/B0FHB5V36G/?tag={AFFILIATE_TAG}", "category": "electronics", "benefit": "Rs 22,999 mein AMOLED 5G + 4K camera",   "commission": 920, "emoji": "🤳"},
    {"name": "OnePlus Nord CE6 Lite", "link": f"https://www.amazon.in/dp/B0GVYDLJJQ/?tag={AFFILIATE_TAG}", "category": "electronics", "benefit": "Rs 17,999 mein OnePlus 5G phone",        "commission": 720, "emoji": "📱"},
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


# ════════════════════════════════════════════════════════════════
#  LAYER 1: LIVE AMAZON SCRAPING
# ════════════════════════════════════════════════════════════════
def layer1_live_scrape():
    """Abhi Amazon se fresh trending products fetch karo"""
    if not BS4_AVAILABLE:
        return []

    cats = random.sample(BESTSELLER_URLS, min(3, len(BESTSELLER_URLS)))
    products = []

    for cat in cats:
        try:
            headers = dict(random.choice(HEADERS_LIST))
            headers["Accept"]          = "text/html,application/xhtml+xml,*/*;q=0.8"
            headers["Accept-Encoding"] = "gzip, deflate, br"

            resp = requests.Session().get(cat["url"], headers=headers, timeout=15)
            if resp.status_code != 200:
                continue

            soup  = BeautifulSoup(resp.text, "html.parser")
            items = []
            for sel in ["div.zg-grid-general-faceout", "li.zg-item-immersion", "div[data-asin]"]:
                items = soup.select(sel)
                if items:
                    break
            if not items:
                items = soup.find_all("div", attrs={"data-asin": True})

            count = 0
            for item in items[:15]:
                if count >= 2:
                    break
                try:
                    asin = item.get("data-asin", "")
                    if not asin:
                        a = item.select_one("a[href*='/dp/']")
                        if a:
                            m = re.search(r'/dp/([A-Z0-9]{10})', a.get('href', ''))
                            asin = m.group(1) if m else ""
                    if not asin or len(asin) != 10:
                        continue

                    name = ""
                    for ns in ["._cDEzb_p13n-sc-css-line-clamp-3_g3dy1",
                               "span.a-size-small.a-link-normal",
                               "a.a-link-normal span"]:
                        el = item.select_one(ns)
                        if el and el.get_text(strip=True):
                            name = el.get_text(strip=True).split("|")[0].strip()[:55]
                            break
                    if not name:
                        name = f"Amazon {cat['category'].title()} Deal"

                    price = 0
                    for ps in ["span.a-price span.a-offscreen", "._cDEzb_p13n-sc-price_3mJ9Z", "span.a-price-whole"]:
                        el = item.select_one(ps)
                        if el:
                            pt = el.get_text(strip=True).split('.')[0]
                            d  = re.sub(r'[^\d]', '', pt)
                            if d:
                                pv = int(d)
                                if 50 <= pv <= 500000:
                                    price = pv
                                    break
                    if not price:
                        price = 999

                    products.append({
                        "name":       name,
                        "link":       f"https://www.amazon.in/dp/{asin}/?tag={AFFILIATE_TAG}",
                        "category":   cat["category"],
                        "benefit":    f"Rs {price:,} mein Amazon bestseller trending {cat['category']} product",
                        "commission": max(int(price * cat["commission_pct"]), 40),
                        "emoji":      cat["emoji"],
                    })
                    count += 1
                except Exception:
                    continue

            if count:
                print(f"   [L1] {cat['emoji']} {cat['category']}: {count} live products")

        except Exception as e:
            print(f"   [L1] {cat['category']}: {e}")

    return products


# ════════════════════════════════════════════════════════════════
#  LAYER 2: products.json (weekly updated, repo mein stored)
# ════════════════════════════════════════════════════════════════
def layer2_json_products():
    """products.json se products load karo — max 7 din purana"""
    try:
        if not os.path.exists(PRODUCTS_JSON):
            print("   [L2] products.json nahi mila — skip")
            return []

        with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)

        products = data.get("products", [])
        updated  = data.get("updated_at", "unknown")

        if not products:
            print("   [L2] products.json empty hai — skip")
            return []

        print(f"   [L2] products.json se {len(products)} products mila (updated: {updated})")
        return products

    except Exception as e:
        print(f"   [L2] products.json read error: {e}")
        return []


# ════════════════════════════════════════════════════════════════
#  POST HISTORY — ek product sirf ek baar, catalog khatam hone tak
# ════════════════════════════════════════════════════════════════
ASIN_RE = re.compile(r'/dp/([A-Z0-9]{10})')


def extract_asin(product):
    """Product link se ASIN nikalo — yahi uska unique ID hai."""
    m = ASIN_RE.search(product.get("link", ""))
    return m.group(1) if m else ""


def load_state():
    """posted_asins.json padho. Purana format (plain list) bhi chal jayega."""
    empty = {"cycle": 1, "posted": [], "catalog": {}}

    if not os.path.exists(STATE_FILE):
        print("   [STATE] posted_asins.json nahi mila — pehla run maan raha hoon")
        return empty

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        # File corrupt ho to bhi post rukni nahi chahiye
        print(f"   [STATE] read error ({e}) — fresh state se shuru")
        return empty

    # Purana format tha sirf ASIN ki list — usse migrate kar lo
    if isinstance(data, list):
        posted = [a for a in data if isinstance(a, str)]
        print(f"   [STATE] purana list format mila ({len(posted)} ASIN) — naye format mein migrate")
        return {"cycle": 1, "posted": posted, "catalog": {}}

    if not isinstance(data, dict):
        return empty

    catalog = data.get("catalog")
    return {
        "cycle":   data.get("cycle", 1),
        "posted":  [a for a in data.get("posted", []) if isinstance(a, str)],
        "catalog": catalog if isinstance(catalog, dict) else {},
    }


def save_state(state):
    """Atomic write — aadhi likhi file kabhi nahi banegi."""
    state["updated_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE_FILE)


def merge_into_catalog(catalog, products):
    """
    Scrape kiye products ko catalog mein jodo.
    Har run mein Amazon sirf 4-6 product deta hai, par catalog jama hota
    rehta hai — isliye rotate karne ko pool bada hota jaata hai.
    """
    added = 0
    for p in products:
        asin = extract_asin(p)
        if not asin:
            continue
        if asin not in catalog:
            added += 1
        catalog[asin] = p          # naam/price hamesha taaza rakho
    return added


def pick_product(state, hot_asins):
    """
    Sirf un products mein se chuno jo is cycle mein post NAHI hue.
    Poora catalog khatam ho jaaye tabhi naya cycle shuru hota hai.
    """
    posted   = set(state["posted"])
    catalog  = state["catalog"]
    unposted = {a: p for a, p in catalog.items() if a not in posted}

    if not unposted:
        state["cycle"] += 1
        state["posted"] = []
        unposted = dict(catalog)
        print(f"   [CYCLE] poora catalog ({len(catalog)}) post ho chuka — "
              f"cycle {state['cycle']} shuru, history reset")

    # Hot product ko preference — par sirf unposted mein se (50% chance)
    if hot_asins and random.random() < 0.50:
        for asin in hot_asins:
            if asin in unposted:
                print(f"   [HOT] click data se hot product chuna: {unposted[asin]['name']}")
                return asin, unposted[asin]

    asin = random.choice(sorted(unposted.keys()))
    return asin, unposted[asin]


# ════════════════════════════════════════════════════════════════
#  AI POST GENERATION
# ════════════════════════════════════════════════════════════════
def generate_post(product, style):
    client   = openai.OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
    hashtags = HASHTAGS.get(product.get("category", "default"), HASHTAGS["default"])

    prompt = f"""Ek viral Telegram channel post likho affiliate product ke liye.

Product: {product['name']} {product['emoji']}
Benefit: {product['benefit']}
Affiliate link: {product['link']}
Writing style: {style}
Hashtags: {hashtags}

Rules:
- Hinglish mein (Hindi + English mix — natural feel)
- 2-4 lines, short aur punchy
- Salesy mat lagao — real user jaisa
- Link PLAIN TEXT mein alag line pe (NO markdown)
- Hashtags end mein
- First line mein hook — scroll ruk jaaye
- 2-3 emojis max

Sirf post text do. Koi explanation nahi."""

    try:
        r   = openai.OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1").chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.9
        )
        raw = r.choices[0].message.content.strip()
        return re.sub(r'\[.*?\]\((https?://[^\)]+)\)', r'\1', raw)
    except Exception as e:
        print(f"   AI error: {e}")
        hashtags = HASHTAGS.get(product.get("category", "default"), HASHTAGS["default"])
        return f"{product['emoji']} {product['name']} — {product['benefit']}\n\n{product['link']}\n\n{hashtags}"


# ════════════════════════════════════════════════════════════════
#  TELEGRAM POST
# ════════════════════════════════════════════════════════════════
def post_to_telegram(message):
    resp = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHANNEL_ID, "text": message,
              "parse_mode": "HTML", "disable_web_page_preview": False},
        timeout=15
    )
    d = resp.json()
    if d.get("ok"):
        print(f"   Posted: https://t.me/{TELEGRAM_CHANNEL_ID.replace('@','')}/{d['result']['message_id']}")
        return True
    print(f"   Telegram error: {d.get('description')}")
    return False


# ════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"\nAuto-post [{datetime.now().strftime('%d %b %Y %H:%M')} IST]")
    print("-" * 45)

    if not GROQ_API_KEY or not TELEGRAM_BOT_TOKEN:
        print("ERROR: API keys missing!")
        exit(1)

    # ── LAYER 1: Live Amazon scraping ──────────────────────────
    print("Layer 1: Amazon se live trending products fetch ho rahe hain...")
    products = layer1_live_scrape()
    source   = "Amazon Live"

    # ── LAYER 2: products.json fallback ────────────────────────
    if not products:
        print("Layer 2: products.json se products load ho rahe hain...")
        products = layer2_json_products()
        source   = "products.json (weekly cache)"

    # ── LAYER 3: Emergency hardcoded ───────────────────────────
    if not products:
        print("Layer 3: Emergency hardcoded products use ho rahe hain...")
        products = EMERGENCY_PRODUCTS
        source   = "Emergency Backup"

    # ── Post history load karo ─────────────────────────────────
    print("\nPost history load ho rahi hai...")
    state = load_state()
    print(f"   [STATE] cycle {state['cycle']} | catalog: {len(state['catalog'])} products "
          f"| ab tak post: {len(state['posted'])}")
    print(f"   [STATE] Previously Posted IDs: {state['posted'] if state['posted'] else '(abhi koi nahi)'}")

    # ── Naye products catalog mein jodo ────────────────────────
    added = merge_into_catalog(state["catalog"], products)
    print(f"   [STATE] is run se {added} naye product jude (source: {source}) "
          f"— catalog ab {len(state['catalog'])}")

    if not state["catalog"]:
        print("ERROR: catalog khali hai — post nahi ho sakti")
        exit(1)

    # ── Boost hot products (from click_report.py data) ────────
    hot_json  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hot_products.json")
    hot_asins = []
    if os.path.exists(hot_json):
        try:
            with open(hot_json) as f:
                hot_data = json.load(f)
            hot_asins = hot_data.get("hot_asins", [])
            print(f"   [HOT] click data se hot ASINs: {hot_asins}")
        except Exception:
            pass

    # ── Product chuno — sirf jo post nahi hua ──────────────────
    asin, product = pick_product(state, hot_asins)

    already    = set(state["posted"])
    remaining  = [a for a in sorted(state["catalog"]) if a not in already and a != asin]
    next_up    = state["catalog"][remaining[0]]["name"] if remaining else "(cycle poora — history reset hogi)"
    style      = random.choice(POST_STYLES)

    print(f"\nSource              : {source}")
    print(f"Selected Product ID : {asin}")
    print(f"Selected Product    : {product['name']} ({product.get('category','-')})")
    print(f"Next Product        : {next_up}")
    print(f"Remaining unposted  : {len(remaining)} / {len(state['catalog'])}")
    print(f"Style               : {style}")

    post_text = generate_post(product, style)
    print(f"\nPost:\n{post_text}\n")

    success = post_to_telegram(post_text)

    # ── Sirf post SAFAL hone par hi history save ───────────────
    # Fail hone par kuch save nahi hota, to agli baar wahi product
    # dobara try hoga — aur duplicate kabhi nahi banega.
    if success:
        state["posted"].append(asin)
        save_state(state)
        print(f"   [STATE] {asin} history mein save — "
              f"{len(state['posted'])}/{len(state['catalog'])} post ho chuke")
    else:
        print("   [STATE] post fail — history nahi badli")

    print("-" * 45)
    exit(0 if success else 1)
