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

AFFILIATE_TAG    = "rahulfinds20c-21"
WEBSITE_URL      = "https://rrcool786-design.github.io/affiliate-autopilot/"
TELEGRAM_CHANNEL = "https://t.me/TechDealsIndia_channel"

# Groups: env var (GitHub Actions) OR hardcode below for local
_groups_env = os.environ.get("TELEGRAM_GROUPS", "")
TARGET_GROUPS = [g.strip() for g in _groups_env.split(",") if g.strip()] or [
    # ← add groups here for local testing
    # "@my_deals_group",
    # "https://t.me/joinchat/XXXX",
]

PRODUCTS_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.json")
MAX_PRODUCTS  = 5
MIN_DELAY     = 10   # seconds between posts
MAX_DELAY     = 25
# ─────────────────────────────────────────────


def load_products():
    if not os.path.exists(PRODUCTS_JSON):
        print("❌ products.json not found.")
        return []
    with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    products = data if isinstance(data, list) else data.get("products", [])
    products.sort(
        key=lambda p: float(str(p.get("discount_pct", 0)).replace("%", "").strip() or 0),
        reverse=True,
    )
    return products[:MAX_PRODUCTS]


def build_message(product, index, total):
    name     = product.get("name", "Amazing Deal")
    price    = product.get("price", "")
    original = product.get("original_price", "")
    discount = product.get("discount_pct", "")
    category = product.get("category", "")
    url      = product.get("url", WEBSITE_URL)

    if "amazon.in" in url and AFFILIATE_TAG not in url:
        url += ("&" if "?" in url else "?") + f"tag={AFFILIATE_TAG}"

    header   = f"🔥 *Deal {index}/{total}* — {datetime.now().strftime('%d %b %Y')}\n\n"
    disc_ln  = f"🏷️ *{discount} OFF*\n" if discount else ""
    cat_ln   = f"📂 _{category}_\n" if category else ""
    orig_ln  = f"~~{original}~~ → " if original else ""

    return (
        f"{header}"
        f"🛒 *{name}*\n\n"
        f"{disc_ln}{cat_ln}"
        f"💰 {orig_ln}*{price}*\n\n"
        f"👉 [Buy on Amazon]({url})\n\n"
        f"📢 All deals: {WEBSITE_URL}\n"
        f"🔔 Join channel: {TELEGRAM_CHANNEL}"
    )


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
