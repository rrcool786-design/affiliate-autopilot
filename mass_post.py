"""
Telethon Mass Group Poster — Affiliate Autopilot
Posts today's top Amazon deals to multiple Telegram groups.

LOCAL RUN:
  pip install telethon
  python get_session_string.py   ← run ONCE to generate session string
  python mass_post.py

GITHUB ACTIONS (fully automated):
  Add these 4 secrets in repo → Settings → Secrets → Actions:
    TELEGRAM_API_ID       = your API_ID (number)
    TELEGRAM_API_HASH     = your API_HASH
    TELETHON_SESSION      = output of get_session_string.py
    TELEGRAM_GROUPS       = comma-separated: @group1,@group2,https://t.me/joinchat/xxx
"""

import asyncio, json, os, random
from datetime import datetime
from telethon import TelegramClient, errors
from telethon.sessions import StringSession

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
API_ID   = int(os.environ.get("TELEGRAM_API_ID",   "0"))
API_HASH = os.environ.get("TELEGRAM_API_HASH",  "")
SESSION  = os.environ.get("TELETHON_SESSION",   "")   # StringSession string
SESSION_FILE = "mass_post"                             # fallback local session file

AFFILIATE_TAG = os.environ.get("AMAZON_AFFILIATE_TAG", "rrcool786-21")
# Tag badalna ho to yahan ya AMAZON_AFFILIATE_TAG env var / GitHub Secret se
WEBSITE_URL      = "https://rrcool786-design.github.io/affiliate-autopilot/"
TELEGRAM_CHANNEL = "https://t.me/TechDealsIndia_channel"

# Groups: env var (GitHub Actions) OR hardcode below for local
_groups_env = os.environ.get("TELEGRAM_GROUPS", "")
TARGET_GROUPS = [g.strip() for g in _groups_env.split(",") if g.strip()] or [
    # ── INDIA DEALS & OFFERS GROUPS ──────────────────────────
    "@IndiaDealz",
    "@amazonindiaoffers",
    "@AmazonIndiaDeals",
    "@dealsforindia",
    "@IndiaLootDeals",
    "@indiadeals",
    "@DealHuntIndia",
    "@BestDealsIndia",
    "@TechDealsIndia",
    "@cheap_deals_india",
    # ── TECH / MOBILE GROUPS ─────────────────────────────────
    "@TechNinja_India",
    "@IndiaSmartphones",
    "@budget_phones_india",
    "@OnePlusIndia",
    "@RedmiIndia_Fans",
    "@iQOO_India",
    # ── AMAZON SPECIFIC ───────────────────────────────────────
    "@AmazonSaleIndia",
    "@Amazon_India_Loot",
    "@AmazonGreatIndia",
    "@AmazonFlipkartDeals",
    # ── SHOPPING / SAVINGS ───────────────────────────────────
    "@OnlineShoppingIndia",
    "@SaveMoneyIndia",
    "@coupons_india",
    "@IndiaOffers",
    "@ShoppingDealsIndia",
    # ── YOUR OWN CHANNEL (always post here first) ────────────
    "https://t.me/TechDealsIndia_channel",
]

PRODUCTS_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.json")
MAX_PRODUCTS  = 5
MIN_DELAY     = 10   # seconds between posts
MAX_DELAY     = 25
# ─────────────────────────────────────────────


def load_products():
    """
    products.json se products lo.

    NOTE: pehle ye code p["discount_pct"] se sort karta tha aur
    p["url"] / p["price"] padhta tha — par products.json mein wo keys
    hain hi nahi (usmein name/link/category/benefit/commission/emoji
    hain). Isliye channel pe khali price wale (💰 **) post ja rahe the
    aur link bhi website pe fallback ho jaata tha.
    """
    if not os.path.exists(PRODUCTS_JSON):
        print("❌ products.json not found.")
        return []
    with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    products = data if isinstance(data, list) else data.get("products", [])

    # Sirf wahi products jinke paas kaam ka naam aur asli Amazon link ho
    products = [p for p in products
                if p.get("name") and "amazon.in" in (p.get("link") or p.get("url") or "")]

    # commission zyada wale pehle — yahi ek asli number hai jo maujood hai
    products.sort(key=lambda p: p.get("commission", 0), reverse=True)
    return products[:MAX_PRODUCTS]


def build_message(product, index, total):
    name     = product.get("name", "").strip() or "Amazon pick"
    category = product.get("category", "")
    benefit  = product.get("benefit", "")
    rating   = product.get("rating", 0)
    reviews  = product.get("reviews", 0)
    price    = product.get("price", 0)
    url      = product.get("link") or product.get("url") or WEBSITE_URL

    if "amazon.in" in url and AFFILIATE_TAG not in url:
        url += ("&" if "?" in url else "?") + f"tag={AFFILIATE_TAG}"

    # Har line sirf tab jab uske peeche asli data ho — warna line hi mat
    # dikhao. Pehle khali price pe "💰 **" chhap jaata tha.
    lines = [f"🛒 *{name}*", ""]
    if category:
        lines.append(f"📂 _{category}_")
    if price:
        lines.append(f"💰 Rs {price:,}")
    if rating and reviews:
        lines.append(f"⭐ {rating}/5 · {reviews:,} reviews")
    elif benefit:
        lines.append(benefit)

    lines += ["", f"👉 [Amazon pe dekho]({url})", "",
              f"📢 Aur picks: {WEBSITE_URL}",
              f"🔔 Channel: {TELEGRAM_CHANNEL}"]
    return "\n".join(lines)


async def run():
    print("=" * 55)
    print(f"🚀 Mass Poster  |  {datetime.now().strftime('%d %b %Y  %H:%M')}")
    print("=" * 55)

    if API_ID == 0 or not API_HASH:
        print("❌ Set TELEGRAM_API_ID and TELEGRAM_API_HASH (env vars or GitHub Secrets)")
        return

    if not TARGET_GROUPS:
        print("❌ No groups set. Add to TARGET_GROUPS list or TELEGRAM_GROUPS env var.")
        return

    products = load_products()
    if not products:
        return

    total = len(TARGET_GROUPS)
    print(f"📦 {len(products)} products  →  {total} groups\n")

    # Use StringSession if available (GitHub Actions), else file session
    session = StringSession(SESSION) if SESSION else SESSION_FILE

    async with TelegramClient(session, API_ID, API_HASH) as client:
        ok, fail = 0, 0
        for i, group in enumerate(TARGET_GROUPS, 1):
            product = products[(i - 1) % len(products)]
            msg = build_message(product, i, total)
            try:
                await client.send_message(group, msg, parse_mode="md", link_preview=False)
                print(f"  ✅ [{i}/{total}] {group}")
                ok += 1
            except errors.FloodWaitError as e:
                print(f"  ⏳ Flood wait {e.seconds}s — skipping {group}")
                await asyncio.sleep(min(e.seconds, 60))
                fail += 1
            except (errors.ChatWriteForbiddenError, errors.UserBannedInChannelError):
                print(f"  🚫 No access: {group}")
                fail += 1
            except Exception as e:
                print(f"  ⚠️  {group}: {e}")
                fail += 1

            if i < total:
                delay = random.randint(MIN_DELAY, MAX_DELAY)
                print(f"     ⏱  {delay}s...")
                await asyncio.sleep(delay)

    print(f"\n{'='*55}")
    print(f"✅ Done — {ok} posted, {fail} failed")
    print(f"{'='*55}")


if __name__ == "__main__":
    asyncio.run(run())
