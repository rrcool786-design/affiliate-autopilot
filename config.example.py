# =============================================================
#   CONFIG.EXAMPLE.PY — Template
#
#   Isko copy karke "config.py" banao aur apni asli keys daalo:
#       copy config.example.py config.py
#
#   config.py .gitignore mein hai — wo kabhi GitHub pe nahi jayegi.
#   ASLI KEYS KABHI IS FILE MEIN MAT DAALNA.
# =============================================================

# ─── API KEYS ───────────────────────────────────────────────────
GROQ_API_KEY       = "PASTE_YOUR_GROQ_KEY_HERE"          # console.groq.com — FREE

# Twitter / X Developer keys — NOT USED (Pay Per Use)
TWITTER_API_KEY        = ""
TWITTER_API_SECRET     = ""
TWITTER_ACCESS_TOKEN   = ""
TWITTER_ACCESS_SECRET  = ""

# Telegram Bot — @BotFather se banao, phir channel mein admin banao
TELEGRAM_BOT_TOKEN   = "PASTE_YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHANNEL_ID  = "@TechDealsIndia_channel"

# Email report ke liye (Gmail App Password use karo, asli password nahi)
EMAIL_SENDER   = "your@gmail.com"
EMAIL_PASSWORD = "PASTE_YOUR_GMAIL_APP_PASSWORD_HERE"
EMAIL_RECEIVER = "where-to-send-report@gmail.com"

# ─── SCHEDULE ───────────────────────────────────────────────────
POST_TIMES = ["07:00", "08:30", "10:00", "11:30", "13:00",
              "14:30", "16:00", "17:30", "19:00", "21:00"]
REPORT_TIME = "22:00"

# ─── AFFILIATE PRODUCTS ─────────────────────────────────────────
# product_updater.py se auto-update hota hai — Sunday 06:00 pe
PRODUCTS = [
    {
        "name": "Product Name",
        "link": "https://www.amazon.in/dp/XXXXXXXXXX/?tag=your-tag-21",
        "category": "electronics",
        "benefit": "Chhota description — kyun lena chahiye",
        "commission": 100,
        "emoji": "📱",
    },
]
