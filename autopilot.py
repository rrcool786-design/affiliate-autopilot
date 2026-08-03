"""
╔══════════════════════════════════════════════════════════════╗
║          AFFILIATE AUTOPILOT ENGINE v3.0 — TELEGRAM          ║
║  Fully automatic: Generate → Post → Track → Report           ║
║                                                              ║
║  SETUP (ek baar karo):                                       ║
║    pip install openai schedule requests                      ║
║    config.py mein apni keys daalo                            ║
║    python autopilot.py                                       ║
╚══════════════════════════════════════════════════════════════╝
"""

import openai
import requests
import schedule
import time
import csv
import smtplib
import random
import logging
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import *

# ─── LOGGING SETUP ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("autopilot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("autopilot")


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 1: AI CONTENT GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def generate_post(product: dict, style: str) -> str:
    """Groq (FREE) se Telegram post generate karo"""
    client = openai.OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )
    hashtags = HASHTAGS.get(product["category"], "#OnlineIncome #PassiveIncome")

    prompt = f"""
Ek viral Telegram channel post likho affiliate product ke liye.

Product: {product['name']} {product['emoji']}
Benefit: {product['benefit']}
Affiliate link: {product['link']}
Writing style: {style}
Hashtags: {hashtags}

Strict rules:
- Hinglish mein likho (Hindi + English mix — natural, real feel)
- 2-4 lines ka post (short, punchy)
- Salesy mat lagao — real user jaisi baat karo
- Link ZAROOR include karo — PLAIN TEXT mein, exactly as given — NO markdown, NO [text](url) format
- Hashtags end mein daalo
- Hook first line mein — scroll-stop karna hai
- Emojis use karo (2-3 max)
- URL ko alag line pe rakho

Example format:
Yaar yeh phone try kiya — sach mein zabardast hai! 📱
Rs 15,999 mein 5G + best battery!

https://amazon.in/...link...

#Gadgets #Tech #AmazonIndia

Sirf post text do. Koi explanation nahi.
"""
    try:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=180,
            temperature=0.9
        )
        raw = resp.choices[0].message.content.strip()
        # Safety fix: convert any markdown [text](url) → plain url
        import re
        raw = re.sub(r'\[.*?\]\((https?://[^\)]+)\)', r'\1', raw)
        return raw
    except Exception as e:
        log.error(f"❌ AI generation failed: {e}")
        # Fallback post if AI fails
        return f"{product['emoji']} {product['name']} — {product['benefit']}\n\n{product['link']}\n\n{hashtags}"


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 2: TELEGRAM AUTO-POSTER (FREE — Unlimited posts)
# ══════════════════════════════════════════════════════════════════════════════

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def post_to_telegram(message: str) -> dict:
    """Telegram channel mein post karo — completely FREE"""
    try:
        url = f"{TELEGRAM_API_URL}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHANNEL_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": False  # Link preview ON — engagement badhta hai
        }
        resp = requests.post(url, json=payload, timeout=15)
        data = resp.json()

        if data.get("ok"):
            msg_id = data["result"]["message_id"]
            channel_username = TELEGRAM_CHANNEL_ID.replace("@", "")
            post_url = f"https://t.me/{channel_username}/{msg_id}"
            log.info(f"✅ Telegram post published: {post_url}")
            return {"success": True, "message_id": msg_id, "url": post_url}
        else:
            error = data.get("description", "Unknown error")
            log.error(f"❌ Telegram API error: {error}")
            return {"success": False, "error": error}

    except requests.RequestException as e:
        log.error(f"❌ Network error: {e}")
        return {"success": False, "error": str(e)}


def test_telegram_connection() -> bool:
    """Bot aur channel connection check karo"""
    try:
        url = f"{TELEGRAM_API_URL}/getMe"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get("ok"):
            bot_name = data["result"]["username"]
            log.info(f"✅ Telegram bot connected: @{bot_name}")
            return True
        else:
            log.error(f"❌ Bot token invalid: {data.get('description')}")
            return False
    except Exception as e:
        log.error(f"❌ Telegram connection failed: {e}")
        return False


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 3: TRACKER — CSV mein sab log karo
# ══════════════════════════════════════════════════════════════════════════════

def init_csv_files():
    """CSV files create karo agar exist nahi karti"""
    if not os.path.exists(POSTS_LOG_FILE):
        with open(POSTS_LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "product", "platform", "post_text",
                             "post_url", "status", "error"])

    if not os.path.exists(EARNINGS_LOG_FILE):
        with open(EARNINGS_LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "product", "estimated_clicks",
                             "conversions", "commission_per_sale",
                             "total_earned_inr", "notes"])


def log_post(product: dict, post_text: str, result: dict):
    """Post ko CSV mein log karo"""
    with open(POSTS_LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            product["name"],
            "Telegram",
            post_text[:120] + "...",
            result.get("url", ""),
            "success" if result["success"] else "failed",
            result.get("error", "")
        ])


def log_earning(product: str, conversions: int = 0, notes: str = "auto-posted"):
    """Earning track karo"""
    product_data = next((p for p in PRODUCTS if p["name"] == product), None)
    if not product_data:
        return
    total = conversions * product_data["commission"]
    with open(EARNINGS_LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d"),
            product,
            0,
            conversions,
            product_data["commission"],
            total,
            notes
        ])


def get_today_stats() -> dict:
    """Aaj ke stats CSV se nikalo"""
    today = datetime.now().strftime("%Y-%m-%d")
    posts_today = 0
    earnings_today = 0.0
    failed_today = 0

    try:
        with open(POSTS_LOG_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["timestamp"].startswith(today):
                    posts_today += 1
                    if row["status"] == "failed":
                        failed_today += 1
    except FileNotFoundError:
        pass

    try:
        with open(EARNINGS_LOG_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["date"] == today:
                    earnings_today += float(row["total_earned_inr"] or 0)
    except FileNotFoundError:
        pass

    return {
        "posts": posts_today,
        "failed": failed_today,
        "earnings": earnings_today
    }


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 4: EMAIL DAILY REPORT
# ══════════════════════════════════════════════════════════════════════════════

def send_daily_report():
    """Raat ko email mein report bhejo"""
    stats = get_today_stats()
    today = datetime.now().strftime("%d %B %Y")
    channel_link = f"https://t.me/{TELEGRAM_CHANNEL_ID.replace('@', '')}"

    html = f"""
    <html><body style="font-family:Arial,sans-serif;max-width:600px;margin:auto;padding:20px;">
      <h2 style="color:#2563eb;">📊 Autopilot Daily Report — {today}</h2>
      <p>Channel: <a href="{channel_link}">{TELEGRAM_CHANNEL_ID}</a></p>

      <table style="width:100%;border-collapse:collapse;margin:20px 0;">
        <tr style="background:#eff6ff;">
          <td style="padding:12px;border:1px solid #ddd;font-weight:bold;">📱 Posts Published</td>
          <td style="padding:12px;border:1px solid #ddd;font-size:22px;font-weight:bold;color:#2563eb;">{stats['posts']}</td>
        </tr>
        <tr>
          <td style="padding:12px;border:1px solid #ddd;font-weight:bold;">❌ Failed Posts</td>
          <td style="padding:12px;border:1px solid #ddd;font-size:22px;color:#dc2626;">{stats['failed']}</td>
        </tr>
        <tr style="background:#f0fdf4;">
          <td style="padding:12px;border:1px solid #ddd;font-weight:bold;">💰 Estimated Earnings</td>
          <td style="padding:12px;border:1px solid #ddd;font-size:22px;font-weight:bold;color:#16a34a;">₹{stats['earnings']:.0f}</td>
        </tr>
      </table>

      <h3>📁 Log Files</h3>
      <ul>
        <li><code>posts_log.csv</code> — saare Telegram posts</li>
        <li><code>earnings_log.csv</code> — income tracking</li>
        <li><code>autopilot.log</code> — system log</li>
      </ul>

      <p style="color:#6b6b6b;font-size:13px;margin-top:30px;">
        🤖 Yeh report automatically bheja gaya hai.<br>
        Earnings manually update karo jab Amazon Associates dashboard pe conversions dikhein.
      </p>
    </body></html>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🤖 Autopilot Report {today} — {stats['posts']} posts, ₹{stats['earnings']:.0f} earned"
        msg["From"]    = EMAIL_SENDER
        msg["To"]      = EMAIL_RECEIVER
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        log.info(f"📧 Daily report bheja gaya: {EMAIL_RECEIVER}")
    except Exception as e:
        log.error(f"❌ Email error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 5: MASTER AUTO-POST JOB
# ══════════════════════════════════════════════════════════════════════════════

def auto_post_job():
    """Ek scheduled posting job — random product + style"""
    log.info("🔄 Auto-post job start hua...")

    # Amazon products only (placeholder links wale skip karo)
    valid_products = [p for p in PRODUCTS if "YOUR_" not in p["link"]]
    if not valid_products:
        valid_products = PRODUCTS  # fallback

    product = random.choice(valid_products)
    style   = random.choice(POST_STYLES)

    log.info(f"   Product: {product['name']} | Style: {style}")

    # Step 1: AI se content generate karo
    post_text = generate_post(product, style)
    log.info(f"   Generated: {post_text[:80]}...")

    # Step 2: Telegram pe post karo
    result = post_to_telegram(post_text)

    # Step 3: CSV mein log karo
    log_post(product, post_text, result)

    if result["success"]:
        log.info(f"✅ Auto-post complete: {product['name']} → {result['url']}")
    else:
        log.warning(f"⚠️  Post failed: {result.get('error')} — logged")


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 6: SCHEDULER
# ══════════════════════════════════════════════════════════════════════════════

def auto_update_products():
    """Weekly Amazon bestsellers se products auto-update karo"""
    log.info("🔄 Weekly product update start hua...")
    try:
        import importlib
        import sys
        updater_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "product_updater.py")
        if os.path.exists(updater_path):
            spec = importlib.util.spec_from_file_location("product_updater", updater_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.run_updater()
            log.info("✅ Products update complete — next posts mein naye products use honge")
        else:
            log.warning("⚠️  product_updater.py nahi mila — skip")
    except Exception as e:
        log.error(f"❌ Product update failed: {e}")


def setup_scheduler():
    """Saari schedules set karo"""
    for post_time in POST_TIMES:
        schedule.every().day.at(post_time).do(auto_post_job)
        log.info(f"   ⏰ Post scheduled: {post_time}")

    schedule.every().day.at(REPORT_TIME).do(send_daily_report)
    log.info(f"   📧 Report scheduled: {REPORT_TIME}")

    # Weekly product update — har Sunday subah 06:00 pe
    schedule.every().sunday.at("06:00").do(auto_update_products)
    log.info(f"   🔍 Product auto-update: Every Sunday 06:00")


def run_autopilot():
    """Main loop — hamesha chalta rahega"""
    log.info("=" * 60)
    log.info("  🤖 AFFILIATE AUTOPILOT ENGINE v3.0 — TELEGRAM")
    log.info("=" * 60)

    # Connection test
    if not test_telegram_connection():
        log.error("❌ Telegram connection fail — config.py mein TELEGRAM_BOT_TOKEN check karo")
        return

    init_csv_files()
    setup_scheduler()

    log.info(f"\n  Platform  : Telegram (@TechDealsIndia_channel)")
    log.info(f"  Products  : {len(PRODUCTS)} loaded")
    log.info(f"  Post times: {', '.join(POST_TIMES)}")
    log.info(f"  Report    : {REPORT_TIME}")
    log.info(f"\n  System chalu hai — Ctrl+C se band karo\n")

    # Pehla test post abhi karo
    log.info("🚀 First post kar raha hoon abhi...")
    auto_post_job()

    while True:
        schedule.run_pending()
        time.sleep(30)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════╗
║    🤖 AFFILIATE AUTOPILOT ENGINE v3.0            ║
║    Platform: Telegram (FREE — Unlimited posts)   ║
║    Generate → Post → Track → Report              ║
╚══════════════════════════════════════════════════╝

Kya karna hai?

  1. Test post     — Abhi ek post Telegram pe bhejo
  2. Full Auto     — 3x/day automatic posting start karo
  3. Email report  — Aaj ka report email karo
  4. Stats         — Terminal mein stats dekho
""")

    choice = input("Choose (1/2/3/4): ").strip()

    if choice == "1":
        print("\n🔄 Telegram connection test kar raha hoon...")
        if test_telegram_connection():
            init_csv_files()
            print("✅ Connected! Post bhej raha hoon...\n")
            auto_post_job()
            print("\n✅ Done! Telegram channel check karo:")
            print(f"   https://t.me/{TELEGRAM_CHANNEL_ID.replace('@', '')}")
        else:
            print("❌ Connection fail. config.py mein TELEGRAM_BOT_TOKEN check karo.")

    elif choice == "2":
        run_autopilot()

    elif choice == "3":
        print("\n📧 Report bhej raha hoon...")
        send_daily_report()
        print("✅ Done! Email check karo.")

    elif choice == "4":
        stats = get_today_stats()
        print(f"\n📊 Aaj ke stats ({datetime.now().strftime('%d %B %Y')}):")
        print(f"   Posts    : {stats['posts']}")
        print(f"   Failed   : {stats['failed']}")
        print(f"   Earnings : ₹{stats['earnings']:.0f}")

    else:
        print("1, 2, 3 ya 4 enter karo.")
