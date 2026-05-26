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
                    # Extract real product image URL
                    img_url = ""
                    for img in item.find_all("img"):
                        # 1. data-a-dynamic-image = JSON {url: [w,h], ...} — most reliable
                        dyn = img.get("data-a-dynamic-image", "")
                        if dyn:
                            try:
                                urls = list(json.loads(dyn).keys())
                                if urls:
                                    img_url = re.sub(r'\._[A-Z]{2,3}\d+_\.', '._AC_SL300_.', urls[0])
                                    break
                            except Exception:
                                pass
                        # 2. src / data-src
                        src = img.get("src", "") or img.get("data-src", "")
                        if src and ("media-amazon" in src or "ssl-images-amazon" in src) and ".gif" not in src:
                            img_url = re.sub(r'\._[A-Z]{2,3}\d+_\.', '._AC_SL300_.', src)
                            break
                    all_products.append({
                        "name": name, "asin": asin,
                        "category": cat["name"], "emoji": cat["emoji"],
                        "price": price, "original_price": original_price, "discount": discount,
                        "image": img_url,
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

    # ── Benefit bullets per category ──────────────────────────
    CATEGORY_BENEFITS = {
        "Electronics": ["✓ Free Delivery", "✓ 1 Year Warranty", "✓ Easy Returns"],
        "Laptops":     ["✓ Free Delivery", "✓ 1 Year Warranty", "✓ EMI Available"],
        "Kitchen":     ["✓ Food Grade", "✓ Easy Clean", "✓ Durable Build"],
        "Home":        ["✓ Free Install", "✓ Premium Quality", "✓ Easy Returns"],
        "Fashion":     ["✓ Genuine Product", "✓ Easy Returns", "✓ Multiple Sizes"],
        "Sports":      ["✓ ISI Certified", "✓ Pro Grade", "✓ Free Delivery"],
        "Beauty":      ["✓ 100% Authentic", "✓ Derma Tested", "✓ Free Delivery"],
        "Books":       ["✓ Original Copy", "✓ Fast Delivery", "✓ Easy Returns"],
        "Toys":        ["✓ Safety Tested", "✓ Age Appropriate", "✓ Free Delivery"],
        "Health":      ["✓ Clinically Tested", "✓ Genuine Product", "✓ Free Delivery"],
    }

    # ── Product Cards ──────────────────────────────────────────
    cards_html = ""
    for i, p in enumerate(products):
        asin     = p.get("asin","")
        # Use scraped image URL only — ASIN ≠ Image ID so CDN fallback is removed
        img_url  = p.get("image", "")
        link     = f"https://www.amazon.in/dp/{asin}/?tag={AFFILIATE_TAG}" if asin else "#"
        discount = p.get("discount", 20)
        price    = p.get("price", 999)
        orig     = p.get("original_price", int(price*1.3))
        saved    = orig - price
        viewers  = random.randint(12, 89)
        bought   = random.randint(47, 312)
        stars    = round(random.uniform(4.1, 4.9), 1)
        star_full = int(stars)
        star_half = 1 if (stars - star_full) >= 0.5 else 0
        star_html = "★" * star_full + ("½" if star_half else "") + "☆" * (5 - star_full - star_half)
        reviews  = random.randint(1200, 18400)
        # Countdown: random 1-8 hrs remaining
        hrs = random.randint(1, 8)
        mins = random.randint(5, 59)
        countdown_id = f"cd_{asin or i}"
        benefits = CATEGORY_BENEFITS.get(p.get("category",""), ["✓ Free Delivery", "✓ Easy Returns", "✓ Genuine Product"])
        benefits_html = " &nbsp;·&nbsp; ".join(benefits)

        badge    = ""
        if i < 3:
            badge = '<span class="badge hot">🔥 HOT DEAL</span>'
        elif discount >= 30:
            badge = '<span class="badge save">💰 BEST PRICE</span>'
        elif i % 4 == 0:
            badge = '<span class="badge trending">📈 TRENDING</span>'

        cards_html += f"""
        <div class="product-card" data-category="{p['category']}">
            {badge}
            <div class="discount-tag">-{discount}%</div>
            <div class="product-img-wrap">
                <img src="{img_url}" alt="{p['name']}" loading="lazy" onerror="this.style.display='none';this.parentNode.querySelector('.img-fallback').style.display='flex'"><div class="img-fallback" style="display:none;align-items:center;justify-content:center;height:160px;font-size:60px;background:#f8f8f8;border-radius:8px">{p.get('emoji','🛒')}</div>
            </div>
            <div class="product-info">
                <span class="category-tag">{p['emoji']} {p['category']}</span>
                <h3 class="product-name">{p['name']}</h3>
                <div class="rating-row">
                    <span class="stars">{star_html}</span>
                    <span class="rating-num">{stars}</span>
                    <span class="rating-count">({reviews:,})</span>
                    <span class="bought-today">🔥 {bought} bought today</span>
                </div>
                <div class="savings-box">
                    <span class="savings-label">You Save</span>
                    <span class="savings-amount">₹{saved:,}</span>
                    <span class="savings-pct">({discount}% OFF)</span>
                </div>
                <div class="price-block">
                    <span class="price">₹{price:,}</span>
                    <span class="original-price">₹{orig:,}</span>
                </div>
                <div class="benefits-row">{benefits_html}</div>
                <div class="urgency-row">
                    <span class="viewers-dot">👁️ {viewers} viewing</span>
                    <span class="countdown-wrap">⏰ Ends in <span class="countdown" id="{countdown_id}" data-hrs="{hrs}" data-mins="{mins}"></span></span>
                </div>
                <a href="{link}" target="_blank" rel="nofollow" class="buy-btn" onclick="trackClick('{asin}')">
                    🛒 Grab This Deal Now
                </a>
                <div class="amazon-tag">✅ Verified Amazon Deal · Free Delivery</div>
            </div>
        </div>"""

    # ── Category Tabs ──────────────────────────────────────────
    tab_html = '<button class="tab active" onclick="filterCat(\'all\', this)">🔥 All Deals</button>\n'
    for cat in categories:
        emoji = next((p["emoji"] for p in products if p["category"] == cat), "🏷️")
        tab_html += f'<button class="tab" onclick="filterCat(\'{cat}\', this)">{emoji} {cat}</button>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TechDeals India 🔥 — Best Amazon Deals Today | {date_str}</title>
<meta name="description" content="Today's best Amazon India deals — up to 70% off on Electronics, Mobiles, Laptops, Kitchen, Fashion & more. Updated daily. Verified deals only.">
<meta name="keywords" content="amazon deals india, best amazon offers today, amazon sale india, mobile deals india, laptop deals, amazon discount">
<meta property="og:title" content="TechDeals India — Best Amazon Deals {date_str}">
<meta property="og:description" content="Har roz ke best Amazon deals — verified aur hand-picked!">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {{
    --primary: #FF6B00;
    --primary-dark: #e05e00;
    --bg: #f5f5f5;
    --card: #ffffff;
    --text: #1a1a1a;
    --text-light: #666;
    --border: #e0e0e0;
    --success: #00a650;
    --shadow: 0 2px 12px rgba(0,0,0,0.08);
    --shadow-hover: 0 8px 30px rgba(0,0,0,0.15);
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Inter',sans-serif; background:var(--bg); color:var(--text); }}

  /* ── HEADER ── */
  header {{
    background: linear-gradient(135deg, #131921 0%, #1f2d3d 100%);
    padding: 0;
    position: sticky; top:0; z-index:100;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  }}
  .header-top {{
    display:flex; align-items:center; justify-content:space-between;
    padding: 12px 20px; max-width:1400px; margin:0 auto;
  }}
  .logo {{ color:#fff; font-size:1.5rem; font-weight:800; text-decoration:none; }}
  .logo span {{ color:var(--primary); }}
  .header-right {{ display:flex; align-items:center; gap:12px; }}
  .tg-btn {{
    background: #0088cc; color:#fff; padding:8px 16px; border-radius:20px;
    text-decoration:none; font-size:0.85rem; font-weight:600;
    display:flex; align-items:center; gap:6px; transition:all 0.2s;
  }}
  .tg-btn:hover {{ background:#006fa6; transform:translateY(-1px); }}
  .live-badge {{
    background:#00a650; color:#fff; padding:4px 10px; border-radius:12px;
    font-size:0.75rem; font-weight:700; display:flex; align-items:center; gap:4px;
  }}
  .live-dot {{ width:7px; height:7px; background:#fff; border-radius:50%; animation:pulse 1.5s infinite; }}
  @keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.3}} }}

  /* ── BANNER ── */
  .banner {{
    background: linear-gradient(135deg, var(--primary) 0%, #ff8c00 100%);
    text-align:center; padding:10px 20px; color:#fff; font-size:0.9rem; font-weight:600;
  }}
  .banner a {{ color:#fff; text-decoration:underline; }}

  /* ── HERO ── */
  .hero {{
    background: linear-gradient(135deg, #131921 0%, #232f3e 100%);
    padding: 40px 20px; text-align:center; color:#fff;
  }}
  .hero h1 {{ font-size:clamp(1.5rem,4vw,2.5rem); font-weight:800; margin-bottom:8px; }}
  .hero h1 span {{ color:var(--primary); }}
  .hero p {{ font-size:1rem; opacity:0.8; margin-bottom:16px; }}
  .update-info {{
    display:inline-flex; align-items:center; gap:8px;
    background:rgba(255,255,255,0.1); padding:6px 14px; border-radius:20px;
    font-size:0.82rem; color:#ccc;
  }}

  /* ── SEARCH ── */
  .search-wrap {{ max-width:600px; margin:20px auto 0; position:relative; }}
  .search-wrap input {{
    width:100%; padding:14px 50px 14px 20px; border-radius:30px; border:none;
    font-size:1rem; outline:none; box-shadow: 0 4px 20px rgba(0,0,0,0.2);
  }}
  .search-wrap button {{
    position:absolute; right:8px; top:50%; transform:translateY(-50%);
    background:var(--primary); border:none; width:36px; height:36px;
    border-radius:50%; cursor:pointer; font-size:1rem;
  }}

  /* ── TABS ── */
  .tabs-wrap {{ background:#fff; border-bottom:2px solid var(--border); position:sticky; top:60px; z-index:90; }}
  .tabs {{ display:flex; gap:4px; padding:0 20px; overflow-x:auto; max-width:1400px; margin:0 auto; scrollbar-width:none; }}
  .tabs::-webkit-scrollbar {{ display:none; }}
  .tab {{
    padding:12px 18px; border:none; background:none; cursor:pointer;
    font-size:0.88rem; font-weight:600; color:var(--text-light); white-space:nowrap;
    border-bottom:3px solid transparent; transition:all 0.2s;
  }}
  .tab:hover {{ color:var(--primary); }}
  .tab.active {{ color:var(--primary); border-bottom-color:var(--primary); }}

  /* ── MAIN ── */
  main {{ max-width:1400px; margin:0 auto; padding:20px; }}

  .section-header {{
    display:flex; align-items:center; justify-content:space-between;
    margin-bottom:16px; padding-bottom:10px; border-bottom:2px solid var(--border);
  }}
  .section-title {{ font-size:1.3rem; font-weight:800; display:flex; align-items:center; gap:8px; }}
  .deal-count {{ font-size:0.85rem; color:var(--text-light); font-weight:500; }}

  /* ── GRID ── */
  .products-grid {{
    display:grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap:16px;
  }}

  /* ── CARD ── */
  .product-card {{
    background:var(--card); border-radius:12px; overflow:hidden;
    box-shadow:var(--shadow); transition:all 0.3s; position:relative;
    display:flex; flex-direction:column;
  }}
  .product-card:hover {{
    transform:translateY(-4px); box-shadow:var(--shadow-hover);
  }}
  .badge {{
    position:absolute; top:10px; left:10px; z-index:2;
    padding:4px 10px; border-radius:12px; font-size:0.72rem; font-weight:700;
  }}
  .badge.hot {{ background:#ff4444; color:#fff; }}
  .badge.save {{ background:#00a650; color:#fff; }}
  .badge.trending {{ background:#6c5ce7; color:#fff; }}
  .discount-tag {{
    position:absolute; top:10px; right:10px; z-index:2;
    background:var(--primary); color:#fff; padding:4px 8px;
    border-radius:8px; font-size:0.75rem; font-weight:800;
  }}
  .product-img-wrap {{
    background:#f8f8f8; padding:20px; display:flex;
    align-items:center; justify-content:center; min-height:180px;
  }}
  .product-img-wrap img {{ max-height:160px; max-width:100%; object-fit:contain; }}
  .product-info {{ padding:14px; flex:1; display:flex; flex-direction:column; gap:6px; }}
  .category-tag {{
    font-size:0.72rem; font-weight:600; color:var(--primary);
    background:#fff5ee; padding:2px 8px; border-radius:8px; display:inline-block;
  }}
  .product-name {{
    font-size:0.9rem; font-weight:600; line-height:1.4;
    display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;
  }}
  .price-block {{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; }}
  .price {{ font-size:1.3rem; font-weight:800; color:#B12704; }}
  .original-price {{ font-size:0.85rem; color:var(--text-light); text-decoration:line-through; }}
  .save-amount {{ font-size:0.78rem; font-weight:700; color:var(--success); }}

  /* ── RATINGS ── */
  .rating-row {{ display:flex; align-items:center; gap:5px; flex-wrap:wrap; margin:2px 0; }}
  .stars {{ color:#FF9900; font-size:0.85rem; letter-spacing:1px; }}
  .rating-num {{ font-weight:700; font-size:0.82rem; color:#FF9900; }}
  .rating-count {{ font-size:0.75rem; color:var(--text-light); }}
  .bought-today {{ font-size:0.72rem; font-weight:700; color:#C7511F; background:#fff3e0; padding:2px 7px; border-radius:10px; }}

  /* ── SAVINGS BOX ── */
  .savings-box {{
    background:linear-gradient(135deg,#e8f5e9,#c8e6c9);
    border:1px solid #a5d6a7; border-radius:8px;
    padding:6px 10px; display:flex; align-items:center; gap:6px; margin:4px 0;
  }}
  .savings-label {{ font-size:0.72rem; color:#2e7d32; font-weight:600; }}
  .savings-amount {{ font-size:1.05rem; font-weight:800; color:#1b5e20; }}
  .savings-pct {{ font-size:0.72rem; color:#2e7d32; font-weight:700; }}

  /* ── BENEFITS ── */
  .benefits-row {{ font-size:0.72rem; color:#00695c; font-weight:600; margin:3px 0; }}

  /* ── URGENCY ── */
  .urgency-row {{ display:flex; align-items:center; justify-content:space-between; font-size:0.72rem; margin:4px 0; }}
  .viewers-dot {{ color:var(--text-light); }}
  .countdown-wrap {{ color:#c62828; font-weight:700; background:#fff3f3; padding:2px 7px; border-radius:8px; }}
  .countdown {{ font-variant-numeric:tabular-nums; }}

  .viewers {{ font-size:0.75rem; color:var(--text-light); }}
  .buy-btn {{
    display:block; background:linear-gradient(135deg, #FFD814 0%, #F7CA00 100%);
    color:#111; text-align:center; padding:11px; border-radius:8px;
    font-weight:800; font-size:0.95rem; text-decoration:none;
    transition:all 0.2s; margin-top:auto;
    border:1px solid #F2C200; letter-spacing:0.3px;
  }}
  .buy-btn:hover {{ background:linear-gradient(135deg, #F7CA00 0%, #e6b800 100%); transform:scale(1.02); box-shadow:0 4px 15px rgba(255,160,0,0.4); }}
  .amazon-tag {{ font-size:0.72rem; color:var(--success); text-align:center; font-weight:600; }}

  /* ── TELEGRAM CTA ── */
  .tg-cta {{
    background: linear-gradient(135deg, #0088cc 0%, #005f8f 100%);
    border-radius:16px; padding:32px; text-align:center; color:#fff; margin:30px 0;
  }}
  .tg-cta h2 {{ font-size:1.5rem; margin-bottom:8px; }}
  .tg-cta p {{ opacity:0.85; margin-bottom:20px; }}
  .tg-cta-btn {{
    display:inline-block; background:#fff; color:#0088cc;
    padding:12px 30px; border-radius:25px; font-weight:700;
    text-decoration:none; font-size:1rem; transition:all 0.2s;
  }}
  .tg-cta-btn:hover {{ transform:scale(1.05); box-shadow:0 4px 20px rgba(0,0,0,0.2); }}

  /* ── TRUST BAR ── */
  .trust-bar {{
    display:flex; justify-content:center; gap:30px; flex-wrap:wrap;
    background:#fff; padding:20px; border-radius:12px; margin:20px 0;
    box-shadow:var(--shadow);
  }}
  .trust-item {{ display:flex; align-items:center; gap:8px; font-size:0.85rem; font-weight:600; color:#333; }}

  /* ── FOOTER ── */
  footer {{
    background:#131921; color:#aaa; text-align:center; padding:30px 20px; margin-top:40px;
  }}
  footer a {{ color:#ccc; text-decoration:none; margin:0 8px; }}
  footer p {{ margin:6px 0; font-size:0.82rem; }}

  /* ── RESPONSIVE ── */
  @media(max-width:600px) {{
    .products-grid {{ grid-template-columns: repeat(2, 1fr); gap:10px; }}
    .hero h1 {{ font-size:1.4rem; }}
    .trust-bar {{ gap:15px; }}
  }}

  /* ── HIDDEN ── */
  .hidden {{ display:none !important; }}

  /* ── TOAST ── */
  .toast {{
    position:fixed; bottom:20px; right:20px; background:#131921; color:#fff;
    padding:12px 20px; border-radius:10px; font-size:0.85rem; font-weight:600;
    transform:translateY(100px); transition:transform 0.3s; z-index:999;
  }}
  .toast.show {{ transform:translateY(0); }}
</style>
</head>
<body>

<!-- HEADER -->
<header>
  <div class="header-top">
    <a href="/" class="logo">TechDeals<span>India</span> 🔥</a>
    <div class="header-right">
      <div class="live-badge"><div class="live-dot"></div> LIVE</div>
      <a href="{TELEGRAM_CHANNEL}" target="_blank" class="tg-btn">
        ✈️ Join Telegram
      </a>
    </div>
  </div>
</header>

<!-- BANNER -->
<div class="banner">
  🎉 <strong>Aaj ke best deals!</strong> — Daily updated, verified Amazon deals &nbsp;|&nbsp;
  <a href="{TELEGRAM_CHANNEL}" target="_blank">Join Telegram for instant alerts →</a>
</div>

<!-- HERO -->
<div class="hero">
  <h1>Best Amazon India Deals <span>Today</span> 🔥</h1>
  <p>Hand-picked, verified deals — updated daily. Up to 70% off!</p>
  <div class="update-info">
    🕐 Last updated: {date_str} at {time_str} &nbsp;•&nbsp; {len(products)} deals live
  </div>
  <div class="search-wrap">
    <input type="text" id="searchInput" placeholder="Search deals... (e.g. phone, laptop, earbuds)" oninput="searchProducts()">
    <button>🔍</button>
  </div>
</div>

<!-- TABS -->
<div class="tabs-wrap">
  <div class="tabs">
    {tab_html}
  </div>
</div>

<!-- MAIN -->
<main>

  <!-- TRUST BAR -->
  <div class="trust-bar">
    <div class="trust-item">✅ Verified Deals Only</div>
    <div class="trust-item">🔄 Updated Daily</div>
    <div class="trust-item">🛒 Direct Amazon Links</div>
    <div class="trust-item">💰 Best Prices Guaranteed</div>
    <div class="trust-item">🔒 100% Safe & Secure</div>
  </div>

  <!-- PRODUCTS -->
  <div class="section-header">
    <div class="section-title">🔥 Today's Best Deals</div>
    <div class="deal-count" id="dealCount">{len(products)} deals found</div>
  </div>

  <div class="products-grid" id="productsGrid">
    {cards_html}
  </div>

  <!-- TELEGRAM CTA -->
  <div class="tg-cta">
    <h2>📲 Never Miss a Deal Again!</h2>
    <p>Join 10,000+ smart shoppers on our Telegram channel.<br>Get instant alerts for flash sales & limited-time offers!</p>
    <a href="{TELEGRAM_CHANNEL}" target="_blank" class="tg-cta-btn">
      ✈️ Join Free Telegram Channel
    </a>
  </div>

</main>

<!-- FOOTER -->
<footer>
  <p>🔥 <strong style="color:#fff">TechDeals India</strong> — India's Most Trusted Deal Site</p>
  <p>
    <a href="{TELEGRAM_CHANNEL}" target="_blank">Telegram</a> •
    <a href="#">Privacy Policy</a> •
    <a href="#">Disclaimer</a>
  </p>
  <p style="margin-top:12px; font-size:0.75rem; opacity:0.6">
    We earn affiliate commission when you buy through our links. Prices may vary. Last updated: {date_str}.
  </p>
</footer>

<div class="toast" id="toast">🛒 Opening Amazon deal...</div>

<script>
function filterCat(cat, btn) {{
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  let cards = document.querySelectorAll('.product-card');
  let count = 0;
  cards.forEach(c => {{
    if (cat === 'all' || c.dataset.category === cat) {{
      c.classList.remove('hidden'); count++;
    }} else {{
      c.classList.add('hidden');
    }}
  }});
  document.getElementById('dealCount').textContent = count + ' deals found';
}}

function searchProducts() {{
  let q = document.getElementById('searchInput').value.toLowerCase();
  let cards = document.querySelectorAll('.product-card');
  let count = 0;
  cards.forEach(c => {{
    let name = c.querySelector('.product-name').textContent.toLowerCase();
    let cat  = c.querySelector('.category-tag').textContent.toLowerCase();
    if (!q || name.includes(q) || cat.includes(q)) {{
      c.classList.remove('hidden'); count++;
    }} else {{
      c.classList.add('hidden');
    }}
  }});
  document.getElementById('dealCount').textContent = count + ' deals found';
}}

function trackClick(asin) {{
  let toast = document.getElementById('toast');
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2500);
}}

// Random viewers update (live feel)
setInterval(() => {{
  document.querySelectorAll('.viewers-dot').forEach(el => {{
    let n = Math.floor(Math.random() * 60) + 10;
    el.textContent = '👁️ ' + n + ' viewing';
  }});
}}, 8000);

// Countdown timers
function startCountdowns() {{
  document.querySelectorAll('.countdown').forEach(el => {{
    let h = parseInt(el.dataset.hrs) || 2;
    let m = parseInt(el.dataset.mins) || 30;
    let s = 0;
    el.textContent = h + 'h ' + String(m).padStart(2,'0') + 'm';
    setInterval(() => {{
      s--;
      if(s < 0) {{ s = 59; m--; }}
      if(m < 0) {{ m = 59; h--; }}
      if(h < 0) {{ h = 0; m = 0; s = 0; }}
      el.textContent = h + 'h ' + String(m).padStart(2,'0') + 'm ' + String(s).padStart(2,'0') + 's';
    }}, 1000);
  }});
}}
startCountdowns();

// Bought today random update
setInterval(() => {{
  document.querySelectorAll('.bought-today').forEach(el => {{
    let n = Math.floor(Math.random() * 30) + parseInt(el.textContent) || 50;
    el.textContent = '🔥 ' + n + ' bought today';
  }});
}}, 30000);
</script>
</body>
</html>"""


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 55)
    print("  PROFESSIONAL WEBSITE GENERATOR")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print("=" * 55)

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

    print(f"\n  ✅ Website generated: docs/index.html")
    print(f"  Size: {len(html):,} characters")
    print("=" * 55)
