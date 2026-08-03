"""
╔══════════════════════════════════════════════════════════════╗
║   CLICK REPORT — Top Converting Products → Telegram         ║
║   Runs daily via GitHub Actions                             ║
║   Fetches /today from Cloudflare Worker → posts to channel  ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import requests
from datetime import datetime

# ── Config ───────────────────────────────────────────────────
TRACKER_URL       = os.environ.get("TRACKER_URL", "")       # Cloudflare Worker URL
BOT_TOKEN         = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHANNEL_ID        = os.environ.get("TELEGRAM_CHANNEL_ID", "@TechDealsIndia_channel")
AFFILIATE_TAG     = "rahulfinds20c-21"
MIN_CLICKS        = 1  # minimum clicks to show in report

def get_today_stats():
    """Fetch today's click stats from Cloudflare Worker."""
    if not TRACKER_URL:
        print("⚠️  TRACKER_URL not set — skipping click report")
        return None
    try:
        r = requests.get(f"{TRACKER_URL}/today", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"❌ Error fetching stats: {e}")
        return None

def get_top_alltime(n=5):
    """Fetch all-time top products."""
    if not TRACKER_URL:
        return []
    try:
        r = requests.get(f"{TRACKER_URL}/top?n={n}", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"❌ Error fetching top: {e}")
        return []

def format_report(stats, top_alltime):
    """Format click data into Telegram message."""
    today = datetime.now().strftime("%d %b %Y")
    total = stats.get("total_clicks", 0)
    top_today = [p for p in stats.get("top_products", []) if p["clicks_today"] >= MIN_CLICKS]

    lines = [f"📊 *DEAL BAZAAR — Daily Report*", f"_{today}_", ""]

    if total == 0:
        lines.append("🔄 Aaj koi click nahi hua abhi tak.")
        lines.append("Kal subah report aayegi!")
    else:
        lines.append(f"✅ *Aaj {total} clicks* hamare deals pe!")
        lines.append("")
        lines.append("🔥 *Aaj ke Top Products:*")
        lines.append("")

        for i, p in enumerate(top_today[:5], 1):
            name     = p.get("name", "Unknown")
            clicks   = p["clicks_today"]
            price    = p.get("price", 0)
            discount = p.get("discount", 0)
            asin     = p["asin"]
            aff_url  = f"https://www.amazon.in/dp/{asin}?tag={AFFILIATE_TAG}"

            medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i - 1]
            lines.append(f"{medal} *{name}*")
            lines.append(f"   👆 {clicks} clicks aaj | {discount}% OFF | ₹{price:,}")
            lines.append(f"   🛒 {aff_url}")
            lines.append("")

    # All-time top section
    if top_alltime:
        lines.append("━━━━━━━━━━━━━━")
        lines.append("🏆 *All-Time Top Sellers:*")
        for p in top_alltime[:3]:
            name   = p.get("name", "Unknown")
            clicks = p.get("clicks", 0)
            asin   = p["asin"]
            aff_url = f"https://www.amazon.in/dp/{asin}?tag={AFFILIATE_TAG}"
            lines.append(f"• {name} — {clicks} total clicks")
            lines.append(f"  {aff_url}")
        lines.append("")

    lines.append("━━━━━━━━━━━━━━")
    lines.append(f"🌐 [Browse all deals](https://rrcool786-design.github.io/affiliate-autopilot/)")
    lines.append(f"📢 [Join channel](https://t.me/TechDealsIndia_channel)")

    return "\n".join(lines)

def post_to_telegram(text):
    """Post message to Telegram channel."""
    if not BOT_TOKEN:
        print("⚠️  BOT_TOKEN not set")
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        r.raise_for_status()
        result = r.json()
        msg_url = f"https://t.me/{CHANNEL_ID.lstrip('@')}/{result['result']['message_id']}"
        print(f"✅ Report posted: {msg_url}")
        return True
    except Exception as e:
        print(f"❌ Telegram error: {e}")
        return False

def update_post_once_with_top_products(top_products):
    """
    Update products list in config so tomorrow's posts feature today's
    top clicking products more prominently.
    """
    if not top_products:
        return
    top_asins = [p["asin"] for p in top_products[:3]]
    print(f"\n📈 Top ASINs today: {top_asins}")
    print("   (Use these in tomorrow's Telegram posts for max conversions)")

    # Write to a file that post_once.py can read
    with open("hot_products.json", "w") as f:
        json.dump({
            "updated": datetime.now().isoformat(),
            "hot_asins": top_asins,
            "products": top_products[:5]
        }, f, indent=2, ensure_ascii=False)
    print("   ✅ hot_products.json updated")

if __name__ == "__main__":
    print("=" * 55)
    print("  CLICK REPORT — Daily Analytics")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print("=" * 55)

    if not TRACKER_URL:
        print("\n⚠️  TRACKER_URL environment variable not set!")
        print("   Set it in GitHub Secrets as TRACKER_URL")
        print("   Value: your Cloudflare Worker URL")
        print("   Example: https://deal-tracker.USERNAME.workers.dev")
        sys.exit(0)  # Don't fail the Action, just skip

    # Get stats
    print("\n[1] Fetching today's click stats...")
    stats = get_today_stats()
    if not stats:
        print("   No stats available — Worker might not be set up yet")
        sys.exit(0)

    total = stats.get("total_clicks", 0)
    top_today = stats.get("top_products", [])
    print(f"   Total clicks today: {total}")
    print(f"   Products clicked: {len(top_today)}")

    print("\n[2] Fetching all-time top products...")
    top_alltime = get_top_alltime(5)
    print(f"   All-time top products: {len(top_alltime)}")

    print("\n[3] Formatting report...")
    message = format_report(stats, top_alltime)
    print(message[:300] + "...")

    print("\n[4] Posting to Telegram...")
    post_to_telegram(message)

    print("\n[5] Updating hot products list...")
    update_post_once_with_top_products(top_today)

    print("\n" + "=" * 55)
    print("  ✅ Click report complete!")
    print("=" * 55)
