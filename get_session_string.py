"""
Run this ONCE on your local PC to generate a Telethon session string.
Then copy the output and add it as GitHub Secret: TELETHON_SESSION

Usage:
  pip install telethon
  python get_session_string.py
"""

import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID   = 0    # ← paste your API_ID  (number from my.telegram.org)
API_HASH = ""   # ← paste your API_HASH (string from my.telegram.org)

async def main():
    if API_ID == 0 or not API_HASH:
        print("❌ Fill in API_ID and API_HASH first!")
        return

    async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        session_str = client.session.save()
        print("\n" + "="*60)
        print("✅ YOUR SESSION STRING (copy everything between the lines):")
        print("="*60)
        print(session_str)
        print("="*60)
        print("\n→ Add this as GitHub Secret: TELETHON_SESSION")
        print("→ Also add: TELEGRAM_API_ID and TELEGRAM_API_HASH")

asyncio.run(main())
