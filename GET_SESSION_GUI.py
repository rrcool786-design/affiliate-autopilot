"""
Telethon Session Generator — saves to file automatically
Run via RUN_SESSION_GUI.bat
"""
import asyncio, os, sys

API_ID   = 38785528
API_HASH = "11bd09c14887231674535ca85bbd725d"
OUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TELETHON_SESSION.txt")

async def main():
    try:
        from telethon import TelegramClient
        from telethon.sessions import StringSession
    except ImportError:
        os.system('pip install telethon')
        from telethon import TelegramClient
        from telethon.sessions import StringSession

    # async with handles login automatically (prompts phone + OTP in terminal)
    async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        session_str = client.session.save()

        # Save to file
        with open(OUT_FILE, "w") as f:
            f.write(session_str)

        print("\n" + "="*60)
        print("SUCCESS! Session string saved to:")
        print(OUT_FILE)
        print("="*60)
        input("\nPress Enter to close...")

asyncio.run(main())
