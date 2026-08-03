"""
Telegram Bot Connection + Test Post
"""
import os
import requests
import sys

# Token config.py se aata hai (local) ya env var se (GitHub Actions)
try:
    from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
except ImportError:
    TELEGRAM_BOT_TOKEN  = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "@TechDealsIndia_channel")

TOKEN   = TELEGRAM_BOT_TOKEN
CHANNEL = TELEGRAM_CHANNEL_ID
BASE    = f"https://api.telegram.org/bot{TOKEN}"

if not TOKEN:
    print("ERROR: TELEGRAM_BOT_TOKEN nahi mila.")
    print("       config.py banao (config.example.py se copy karke)")
    print("       ya TELEGRAM_BOT_TOKEN env var set karo.")
    sys.exit(1)

print("=" * 50)
print("  Telegram Bot Test")
print("=" * 50)
print()

# Step 1: Bot check
print("Step 1: Bot connection check...")
try:
    r = requests.get(f"{BASE}/getMe", timeout=10)
    d = r.json()
    if d.get("ok"):
        bot_user = d["result"]["username"]
        print(f"  SUCCESS! Bot: @{bot_user}")
    else:
        print(f"  FAIL: {d.get('description')}")
        input("\nPress Enter to exit...")
        sys.exit(1)
except Exception as e:
    print(f"  ERROR: {e}")
    input("\nPress Enter to exit...")
    sys.exit(1)

print()

# Step 2: Test post
print("Step 2: Test post channel pe bhej raha hoon...")
msg = (
    "Redmi A7 Pro 5G check kiya maine \U0001f4f1\n\n"
    "Rs 15,999 mein 5G — yaar sach mein value for money hai!\n"
    "Fastest processor + pure day battery\n\n"
    "Amazon pe: https://www.amazon.in/dp/B0GS5Y6BD3/?tag=rahulfinds20c-21\n\n"
    "#Gadgets #Tech #AmazonIndia #TechDeals"
)

try:
    r2 = requests.post(
        f"{BASE}/sendMessage",
        json={"chat_id": CHANNEL, "text": msg},
        timeout=15
    )
    d2 = r2.json()
    if d2.get("ok"):
        mid = d2["result"]["message_id"]
        print(f"  SUCCESS! Post ID: {mid}")
        print(f"  URL: https://t.me/TechDealsIndia_channel/{mid}")
        print()
        print("  TELEGRAM BOT WORKING! System ready hai.")
        print("  Ab START.bat double-click karo full autopilot ke liye.")
    else:
        print(f"  FAIL: {d2.get('description')}")
        print(f"  Full response: {d2}")
except Exception as e:
    print(f"  ERROR: {e}")

print()
input("Press Enter to exit...")
