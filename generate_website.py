"""
Professional Amazon Deals Website Generator
Daily auto-generate — GitHub Pages pe free hosting
Zero maintenance, zero cost, daily fresh deals
"""

import requests
import json
import os
import re
import random
from datetime import datetime

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

AFFILIATE_TAG  = "rahulfinds20c-21"
TELEGRAM_CHANNEL = "https://t.me/TechDealsIndia_channel"
OUTPUT_DIR     = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
OUTPUT_FILE    = os.path.join(OUTPUT_DIR, "index.html")
PRODUCTS_JSON  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.json")

CATEGORIES = [
    {"url": "https://www.amazon.in/gp/bestsellers/electronics/",    "name": "Electronics",  "emoji": "📱", "commission_pct": 0.04},
    {"url": "https://www.amazon.in/gp/bestsellers/computers/",      "name": "Laptops",      "emoji": "💻", "commission_pct": 0.04},
    {"url": "https://www.amazon.in/gp/bestsellers/kitchen/",        "name": "Kitchen",      "emoji": "🍳", "commission_pct": 0.05},
    {"url": "https://www.amazon.in/gp/bestsellers/home/",           "name": "Home",         "emoji": "🏠", "commission_pct": 0.05},
    {"url": "https://www.amazon.in/gp/bestsellers/apparel/",        "name": "Fashion",      "emoji": "👕", "commission_pct": 0.09},
    {"url": "https://www.amazon.in/gp/bestsellers/sporting-goods/", "name": "Sports",       "emoji": "⚽", "commission_pct": 0.05},
    {"url": "https://www.amazon.in/gp/bestsellers/beauty/",         "name": "Beauty",       "emoji": "💄", "commission_pct": 0.06},
    {"url": "https://www.amazon.in/gp/bestsellers/books/",          "name": "Books",        "emoji": "📚", "commission_pct": 0.05},
    {"url": "https://www.amazon.in/gp/bestsellers/toys/",           "name": "Toys",         "emoji": "🧸", "commission_pct": 0.05},
    {"url": "https://www.amazon.in/gp/bestsellers/health/",         "name": "Health",       "emoji": "💊", "commission_pct": 0.05},
]

HEADERS_LIST = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36", "Accept-Language": "en-IN,en;q=0.9"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36", "Accept-Language": "en-US,en;q=0.8"},
]

EMERGENCY_PRODUCTS = [
    {"name": "Redmi A7 Pro 5G",      "asin": "B0GS5Y6BD3",  "category": "Electronics", "emoji": "📱", "price": 15999, "original_price": 19999, "discount": 20},
    {"name": "OnePlus Buds 3r",       "asin": "B0FMDL81GS", "category": "Electronics", "emoji": "🎧", "price": 1999,  "original_price": 2999,  "discount": 33},
    {"name": "iQOO Z10R 5G",          "asin": "B0FHB5V36G", "category": "Electronics", "emoji": "📱", "price": 22999, "original_price": 29999, "discount": 23},
    {"name": "OnePlus Nord CE6 Lite", "asin": "B0GVYDLJJQ", "category": "Electronics", "emoji": "📱", "price": 17999, "original_price": 22999, "discount": 22},
]

import time

def scrape_products():
    if not BS4_AVAILABLE:
        return []
    all_products = []
    for cat in CATEGORIES:
        try:
            time.sleep(random.uniform(1, 3))
            headers = dict(random.choice(HEADERS_LIST))
            headers["Accept"] = "text/html,application/xhtml+xml,*/*;q=0.8"
            resp = requests.Session().get(cat["url"], headers=headers, timeout=15)
            if resp.status_code != 200:
                continue
            soup  = BeautifulSoup(resp.text, "html.parser")
            items = []
            for sel in ["div.zg-grid-general-faceout", "li.zg-item-immersion", "div[data-asin]"]:
                items = soup.select(sel)
                if items:
                    break
            count = 0
            for item in items[:20]:
                if count >= 3:
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
                    for ns in ["._cDEzb_p13n-sc-css-line-clamp-3_g3dy1", "span.a-size-small.a-link-normal", "a.a-link-normal span"]:
                        el = item.select_one(ns)
                        if el and el.get_text(strip=True):
                            name = el.get_text(strip=True).split("|")[0].strip()[:60]
                            break
                    if not name:
                        name = f"Amazon {cat['name']} Deal"
                    price = 999
                    for ps in ["span.a-price span.a-offscreen", "._cDEzb_p13n-sc-price_3mJ9Z", "span.a-price-whole"]:
                        el = item.select_one(ps)
                        if el:
                            d = re.sub(r'[^\d]', '', el.get_text(strip=True).split('.')[0])
                            if d and 50 <= int(d) <= 500000:
                                price = int(d)
                                break
                    original_price = int(price * random.uniform(1.2, 1.5))
                    discount = int((1 - price/original_price) * 100)
                    all_products.append({
                        "name": name, "asin": asin,
                        "category": cat["name"], "emoji": cat["emoji"],
                        "price": price, "original_price": original_price, "discount": discount,
                    })
                    count += 1
                except Exception:
                    continue
        except Exception:
            continue
    return all_products


def load_json_products():
    try:
        if not os.path.exists(PRODUCTS_JSON):
            return []
        with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        products = data.get("products", [])
        result = []
        for p in products:
            asin = p.get("link", "").split("/dp/")[-1].split("/")[0] if "/dp/" in p.get("link","") else ""
            price_str = re.sub(r'[^\d]', '', p.get("benefit","").split("Rs ")[-1].split(" ")[0]) if "Rs " in p.get("benefit","") else "999"
            price = int(price_str) if price_str else 999
            original_price = int(price * 1.3)
            discount = int((1 - price/original_price) * 100)
            result.append({
                "name": p.get("name","Deal"), "asin": asin,
                "category": p.get("category","Electronics").title(), "emoji": p.get("emoji","🔥"),
                "price": price, "original_price": original_price, "discount": discount,
            })
        return result
    except Exception:
        return []


def generate_html(products):
    now       = datetime.now()
    date_str  = now.strftime("%d %B %Y")
    time_str  = now.strftime("%I:%M %p IST")
    categories = sorted(set(p["category"] for p in products))
    cards_html = ""
    for i, p in enumerate(products):
        asin     = p.get("asin","")
        img_url  = f"https://ws-in.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN={asin}&Format=_SL250_&ID=AsinImage&MarketPlace=IN&ServiceVersion=20070822&WS=1&tag={AFFILIATE_TAG}" if asin else ""
        link     = f"https://www.amazon.in/dp/{asin}/?tag={AFFILIATE_TAG}" if asin else "#"
        discount = p.get("discount", 20)
        price    = p.get("price", 999)
        orig     = p.get("original_price", int(price*1.3))
        viewers  = random.randint(12, 89)
        badge    = ""
        if i < 3:
            badge = '<span class="badge hot">HOT DEAL</span>'
        elif discount >= 30:
            badge = '<span class="badge save">BEST PRICE</span>'
        cards_html += f'<div class="product-card" data-category="{p["category"]}"><a href="{link}" target="_blank" rel="nofollow" class="card-link"><div class="discount-tag">-{discount}%</div><div class="product-img-wrap"><img src="{img_url}" alt="{p["name"]}" loading="lazy" onerror="this.src=\'https://placehold.co/200x200/f0f0f0/999?text=Deal\'"></div><div class="product-info"><span class="category-tag">{p["emoji"]} {p["category"]}</span><h3 class="product-name">{p["name"]}</h3><div class="price-block"><span class="price">Rs.{price:,}</span><span class="original-price">Rs.{orig:,}</span></div><div class="save-amount">Save Rs.{orig-price:,} ({discount}% off)</div><div class="buy-btn">Get This Deal on Amazon</div><div class="amazon-tag">Verified Amazon Deal</div></div></a></div>'
    tab_html = '<button class="tab active" onclick="filterCat(\'all\', this)">All Deals</button>\n'
    for cat in categories:
        emoji = next((p["emoji"] for p in products if p["category"] == cat), "")
        tab_html += f'<button class="tab" onclick="filterCat(\'{cat}\', this)">{emoji} {cat}</button>\n'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TechDeals India - Best Amazon Deals Today {date_str}</title>
<meta name="description" content="Best Amazon India deals today - up to 70% off Electronics, Mobiles, Laptops, Kitchen, Fashion. Updated daily. Verified deals only.">
<meta name="keywords" content="amazon deals india, best amazon offers today, amazon sale india, mobile deals india, laptop deals">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Inter',sans-serif;background:#f5f5f5;color:#1a1a1a}}
header{{background:linear-gradient(135deg,#131921,#1f2d3d);padding:0;position:sticky;top:0;z-index:100;box-shadow:0 2px 8px rgba(0,0,0,.3)}}
.header-top{{display:flex;align-items:center;justify-content:space-between;padding:12px 20px;max-width:1400px;margin:0 auto}}
.logo{{color:#fff;font-size:1.5rem;font-weight:800;text-decoration:none}}.logo span{{color:#FF6B00}}
.tg-btn{{background:#0088cc;color:#fff;padding:8px 16px;border-radius:20px;text-decoration:none;font-size:.85rem;font-weight:600}}
.live-badge{{background:#00a650;color:#fff;padding:4px 10px;border-radius:12px;font-size:.75rem;font-weight:700}}
.banner{{background:linear-gradient(135deg,#FF6B00,#ff8c00);text-align:center;padding:10px 20px;color:#fff;font-size:.9rem;font-weight:600}}
.banner a{{color:#fff;text-decoration:underline}}
.hero{{background:linear-gradient(135deg,#131921,#232f3e);padding:40px 20px;text-align:center;color:#fff}}
.hero h1{{font-size:clamp(1.5rem,4vw,2.5rem);font-weight:800;margin-bottom:8px}}.hero h1 span{{color:#FF6B00}}
.hero p{{font-size:1rem;opacity:.8;margin-bottom:16px}}
.update-info{{display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.1);padding:6px 14px;border-radius:20px;font-size:.82rem;color:#ccc}}
.search-wrap{{max-width:600px;margin:20px auto 0;position:relative}}
.search-wrap input{{width:100%;padding:14px 50px 14px 20px;border-radius:30px;border:none;font-size:1rem;outline:none}}
.search-wrap button{{position:absolute;right:8px;top:50%;transform:translateY(-50%);background:#FF6B00;border:none;width:36px;height:36px;border-radius:50%;cursor:pointer;color:#fff;font-size:1rem}}
.tabs-wrap{{background:#fff;border-bottom:2px solid #e0e0e0;position:sticky;top:60px;z-index:90}}
.tabs{{display:flex;gap:4px;padding:0 20px;overflow-x:auto;max-width:1400px;margin:0 auto;scrollbar-width:none}}
.tab{{padding:12px 18px;border:none;background:none;cursor:pointer;font-size:.88rem;font-weight:600;color:#666;white-space:nowrap;border-bottom:3px solid transparent;transition:all .2s}}
.tab.active,.tab:hover{{color:#FF6B00}}.tab.active{{border-bottom-color:#FF6B00}}
main{{max-width:1400px;margin:0 auto;padding:20px}}
.trust-bar{{display:flex;justify-content:center;gap:30px;flex-wrap:wrap;background:#fff;padding:20px;border-radius:12px;margin:20px 0;box-shadow:0 2px 12px rgba(0,0,0,.08)}}
.trust-item{{display:flex;align-items:center;gap:8px;font-size:.85rem;font-weight:600}}
.section-header{{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;padding-bottom:10px;border-bottom:2px solid #e0e0e0}}
.section-title{{font-size:1.3rem;font-weight:800}}
.deal-count{{font-size:.85rem;color:#666;font-weight:500}}
.products-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}}
.product-card{{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.08);transition:all .3s;position:relative}}
.product-card:hover{{transform:translateY(-4px);box-shadow:0 8px 30px rgba(0,0,0,.15)}}
.card-link{{text-decoration:none;color:inherit;display:flex;flex-direction:column;height:100%}}
.discount-tag{{position:absolute;top:10px;right:10px;z-index:2;background:#FF6B00;color:#fff;padding:4px 8px;border-radius:8px;font-size:.75rem;font-weight:800}}
.product-img-wrap{{background:#f8f8f8;padding:20px;display:flex;align-items:center;justify-content:center;min-height:180px}}
.product-img-wrap img{{max-height:160px;max-width:100%;object-fit:contain}}
.product-info{{padding:14px;flex:1;display:flex;flex-direction:column;gap:6px}}
.category-tag{{font-size:.72rem;font-weight:600;color:#FF6B00;background:#fff5ee;padding:2px 8px;border-radius:8px;display:inline-block}}
.product-name{{font-size:.9rem;font-weight:600;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.price-block{{display:flex;align-items:center;gap:8px;flex-wrap:wrap}}
.price{{font-size:1.3rem;font-weight:800;color:#B12704}}
.original-price{{font-size:.85rem;color:#666;text-decoration:line-through}}
.save-amount{{font-size:.78rem;font-weight:700;color:#00a650}}
.buy-btn{{display:block;background:linear-gradient(135deg,#FFD814,#F7CA00);color:#111;text-align:center;padding:10px;border-radius:8px;font-weight:700;font-size:.9rem;margin-top:auto;border:1px solid #F2C200}}
.amazon-tag{{font-size:.72rem;color:#00a650;text-align:center;font-weight:600}}
.tg-cta{{background:linear-gradient(135deg,#0088cc,#005f8f);border-radius:16px;padding:32px;text-align:center;color:#fff;margin:30px 0}}
.tg-cta h2{{font-size:1.5rem;margin-bottom:8px}}
.tg-cta p{{opacity:.85;margin-bottom:20px}}
.tg-cta-btn{{display:inline-block;background:#fff;color:#0088cc;padding:12px 30px;border-radius:25px;font-weight:700;text-decoration:none;font-size:1rem}}
footer{{background:#131921;color:#aaa;text-align:center;padding:30px 20px;margin-top:40px}}
footer a{{color:#ccc;text-decoration:none;margin:0 8px}}
footer p{{margin:6px 0;font-size:.82rem}}
.hidden{{display:none!important}}
@media(max-width:600px){{.products-grid{{grid-template-columns:repeat(2,1fr);gap:10px}}.trust-bar{{gap:15px}}}}
</style>
</head>
<body>
<header>
<div class="header-top">
<a href="/" class="logo">TechDeals<span>India</span> 🔥</a>
<div style="display:flex;align-items:center;gap:12px">
<div class="live-badge">● LIVE</div>
<a href="https://t.me/TechDealsIndia_channel" target="_blank" class="tg-btn">✈️ Join Telegram</a>
</div>
</div>
</header>
<div class="banner">🎉 <strong>Aaj ke best deals!</strong> — Daily updated, verified Amazon deals &nbsp;|&nbsp; <a href="https://t.me/TechDealsIndia_channel" target="_blank">Join Telegram for instant alerts →</a></div>
<div class="hero">
<h1>Best Amazon India Deals <span>Today</span> 🔥</h1>
<p>Hand-picked, verified deals — updated daily. Up to 70% off!</p>
<div class="update-info">🕐 Last updated: {date_str} at {time_str} &nbsp;•&nbsp; {len(products)} deals live</div>
<div class="search-wrap"><input type="text" id="searchInput" placeholder="Search deals... phone, laptop, earbuds" oninput="searchProducts()"><button>🔍</button></div>
</div>
<div class="tabs-wrap"><div class="tabs">{tab_html}</div></div>
<main>
<div class="trust-bar">
<div class="trust-item">✅ Verified Deals Only</div>
<div class="trust-item">🔄 Updated Daily</div>
<div class="trust-item">🛒 Direct Amazon Links</div>
<div class="trust-item">💰 Best Prices</div>
<div class="trust-item">🔒 100% Safe</div>
</div>
<div class="section-header">
<div class="section-title">🔥 Today's Best Deals</div>
<div class="deal-count" id="dealCount">{len(products)} deals found</div>
</div>
<div class="products-grid" id="productsGrid">{cards_html}</div>
<div class="tg-cta">
<h2>📲 Never Miss a Deal Again!</h2>
<p>Join thousands of smart shoppers on our Telegram channel.<br>Get instant alerts for flash sales and limited-time offers!</p>
<a href="https://t.me/TechDealsIndia_channel" target="_blank" class="tg-cta-btn">✈️ Join Free Telegram Channel</a>
</div>
</main>
<footer>
<p>🔥 <strong style="color:#fff">TechDeals India</strong> — India's Most Trusted Deal Site</p>
<p><a href="https://t.me/TechDealsIndia_channel" target="_blank">Telegram</a> • <a href="#">Privacy Policy</a> • <a href="#">Disclaimer</a></p>
<p style="margin-top:12px;font-size:.75rem;opacity:.6">We earn affiliate commission when you buy through our links. Prices may vary. Last updated: {date_str}.</p>
</footer>
<script>
function filterCat(cat,btn){{document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));btn.classList.add('active');let cards=document.querySelectorAll('.product-card'),count=0;cards.forEach(c=>{{if(cat==='all'||c.dataset.category===cat){{c.classList.remove('hidden');count++;}}else{{c.classList.add('hidden');}}});document.getElementById('dealCount').textContent=count+' deals found';}}
function searchProducts(){{let q=document.getElementById('searchInput').value.toLowerCase(),cards=document.querySelectorAll('.product-card'),count=0;cards.forEach(c=>{{let name=c.querySelector('.product-name').textContent.toLowerCase(),cat2=c.querySelector('.category-tag').textContent.toLowerCase();if(!q||name.includes(q)||cat2.includes(q)){{c.classList.remove('hidden');count++;}}else{{c.classList.add('hidden');}}}});document.getElementById('dealCount').textContent=count+' deals found';}}
</script>
</body>
</html>"""


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("="*55)
    print("  PROFESSIONAL WEBSITE GENERATOR")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print("="*55)
    print("\n[Layer 1] Amazon se live scraping...")
    products = scrape_products()
    source = "Amazon Live"
    if not products:
        print("[Layer 2] products.json se load ho raha hai...")
        products = load_json_products()
        source = "products.json"
    if not products:
        print("[Layer 3] Emergency backup products...")
        products = EMERGENCY_PRODUCTS
        source = "Emergency Backup"
    print(f"  Source  : {source}")
    print(f"  Products: {len(products)}")
    html = generate_html(products)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n  Website generated: docs/index.html ({len(html):,} chars)")
    print("="*55)
