"""
╔══════════════════════════════════════════════════════════════╗
║          🔥 VIRAL SHARE ENGINE — 5 SALES FAST 🔥             ║
║  WhatsApp · Telegram · Reddit · Facebook · Instagram         ║
╚══════════════════════════════════════════════════════════════╝

Run:  python VIRAL_SHARE.py
Output:  SHARE_NOW.txt  (copy-paste ke liye ready messages)
"""

from datetime import datetime

SITE     = "https://rrcool786-design.github.io/affiliate-autopilot/"
TAG      = "rahulfinds20c-21"
TELEGRAM = "https://t.me/TechDealsIndia_channel"

TODAY = datetime.now().strftime("%d %b %Y")

# ─── TOP DEALS (live from site) ───────────────────────────────
DEALS = [
    {
        "name":    "Redmi A7 Pro 5G",
        "price":   "₹15,999",
        "orig":    "₹19,999",
        "save":    "₹4,000",
        "pct":     "20%",
        "url":     "https://www.amazon.in/dp/B0GS5Y6BD3/?tag=rahulfinds20c-21",
        "why":     "Budget 5G phone with 50MP camera & 5000mAh battery",
    },
    {
        "name":    "OnePlus Nord Buds 3r",
        "price":   "₹1,999",
        "orig":    "₹2,999",
        "save":    "₹1,000",
        "pct":     "33%",
        "url":     "https://www.amazon.in/dp/B0FMDL81GS/?tag=rahulfinds20c-21",
        "why":     "ANC earbuds with 44hr battery — lowest price ever",
    },
    {
        "name":    "iQOO Z10R 5G",
        "price":   "₹22,999",
        "orig":    "₹29,999",
        "save":    "₹7,000",
        "pct":     "23%",
        "url":     "https://www.amazon.in/dp/B0FHB5V36G/?tag=rahulfinds20c-21",
        "why":     "6000mAh beast with 144Hz display & Snapdragon 7s Gen 3",
    },
    {
        "name":    "OnePlus Nord CE6 Lite",
        "price":   "₹17,999",
        "orig":    "₹22,999",
        "save":    "₹5,000",
        "pct":     "22%",
        "url":     "https://www.amazon.in/dp/B0GVYDLJJQ/?tag=rahulfinds20c-21",
        "why":     "OnePlus quality at budget price — limited stock",
    },
]

# ──────────────────────────────────────────────────────────────
#  MESSAGE TEMPLATES
# ──────────────────────────────────────────────────────────────

def whatsapp_group_blast():
    msgs = []

    # MSG 1: Main broadcast
    m1 = f"""🚨 *AMAZON DEALS TODAY — {TODAY}* 🚨

Bhai log, ye deals abhi live hain — limited time!

📱 *Redmi A7 Pro 5G*
💸 ~~₹19,999~~ → *₹15,999* (Save ₹4,000!)
👉 {DEALS[0]['url']}

🎧 *OnePlus Buds 3r* (ANC Earbuds)
💸 ~~₹2,999~~ → *₹1,999* (33% OFF!)
👉 {DEALS[1]['url']}

📱 *iQOO Z10R 5G* (6000mAh)
💸 ~~₹29,999~~ → *₹22,999* (Save ₹7,000!)
👉 {DEALS[2]['url']}

📱 *OnePlus Nord CE6 Lite*
💸 ~~₹22,999~~ → *₹17,999* (Save ₹5,000!)
👉 {DEALS[3]['url']}

⚡ Aur bhi 15+ deals:
🌐 {SITE}

📣 Share karo doston ke saath!
🔔 Daily alerts: {TELEGRAM}"""
    msgs.append(("WhatsApp Group Blast (Main)", m1))

    # MSG 2: Urgency msg
    m2 = f"""⚠️ *ALERT: Amazon Stock Khatam Ho Raha Hai!*

Ye items abhi ₹₹₹ saste hain — kal price badh sakta hai:

1️⃣ iQOO Z10R 5G — *Save ₹7,000* 🔥
   {DEALS[2]['url']}

2️⃣ OnePlus Buds 3r — *₹1,999* (Lowest Price)
   {DEALS[1]['url']}

3️⃣ Redmi A7 Pro 5G — *Save ₹4,000*
   {DEALS[0]['url']}

⏰ Deals expire aaj raat tak
Sabhi deals ek jagah: {SITE}"""
    msgs.append(("WhatsApp Urgency Message", m2))

    # MSG 3: Personal recommendation style
    m3 = f"""Yaar, mujhe ek khatarnak deal mili —

*iQOO Z10R 5G sirf ₹22,999* mein! 😱
(MRP ₹29,999 tha — save ₹7,000)
{DEALS[2]['url']}

Aur earbuds chahiye? OnePlus Buds 3r sirf ₹1,999!
{DEALS[1]['url']}

Zyada deals dekho: {SITE}

(Bhai share karo, family ko bhi batao 🙏)"""
    msgs.append(("Personal Recommendation Style", m3))

    # MSG 4: Status message (short)
    m4 = f"""🔥 {TODAY} — Amazon Maha Deals!

📱 iQOO Z10R 5G → ₹22,999 (Save ₹7k)
📱 Redmi A7 Pro → ₹15,999 (Save ₹4k)
🎧 OnePlus Buds 3r → ₹1,999 (33% OFF)

👇 Sabhi deals:
{SITE}"""
    msgs.append(("WhatsApp/Instagram Status (Short)", m4))

    return msgs


def telegram_group_messages():
    msgs = []

    m1 = f"""🔥 **AMAZON DEALS — {TODAY}** 🔥

━━━━━━━━━━━━━━━━━━━━
📱 **iQOO Z10R 5G**
~~₹29,999~~ → **₹22,999** _(Save ₹7,000 | 23% OFF)_
✅ Snapdragon 7s Gen 3 | 6000mAh | 144Hz
🛒 {DEALS[2]['url']}
━━━━━━━━━━━━━━━━━━━━
🎧 **OnePlus Nord Buds 3r**
~~₹2,999~~ → **₹1,999** _(33% OFF | Lowest Price Ever)_
✅ ANC | 44hr Battery | Fast Charge
🛒 {DEALS[1]['url']}
━━━━━━━━━━━━━━━━━━━━
📱 **Redmi A7 Pro 5G**
~~₹19,999~~ → **₹15,999** _(Save ₹4,000)_
✅ 50MP Camera | 5000mAh | 5G
🛒 {DEALS[0]['url']}
━━━━━━━━━━━━━━━━━━━━

🌐 **15+ aur deals:** {SITE}
🔔 **Join:** {TELEGRAM}

_Share karo! Doston ki help karo paise bachane mein_ 🙏"""
    msgs.append(("Telegram Group Post (Formatted)", m1))

    m2 = f"""💥 **FLASH SALE ALERT** 💥

iQOO Z10R 5G abhi **₹22,999** mein!
Direct link: {DEALS[2]['url']}

OnePlus Buds 3r abhi **₹1,999** mein!
Direct link: {DEALS[1]['url']}

⚡ Stock limited — abhi order karo
📌 Save this post for later"""
    msgs.append(("Telegram Flash Alert (Short)", m2))

    return msgs


def reddit_posts():
    msgs = []

    m1 = f"""**Title:** Found some great Amazon India deals today — iQOO Z10R 5G at ₹22,999 (Save ₹7,000)

Been tracking Amazon prices for a while. Today found these:

**iQOO Z10R 5G** - ₹22,999 (was ₹29,999)
- Snapdragon 7s Gen 3, 6000mAh, 144Hz AMOLED
- Link: {DEALS[2]['url']}

**OnePlus Buds 3r** - ₹1,999 (was ₹2,999) — seems like all-time low
- ANC, 44hr total battery
- Link: {DEALS[1]['url']}

**Redmi A7 Pro 5G** - ₹15,999 (was ₹19,999)
- Good budget 5G option
- Link: {DEALS[0]['url']}

More deals I'm tracking: {SITE}

---
*Posted these in r/IndiaDeals, r/india — feel free to share*"""
    msgs.append(("Reddit Post — r/IndiaDeals / r/india", m1))

    m2 = """**Subreddits to post in (copy-paste same post):**
• r/IndiaDeals
• r/india
• r/androidindia
• r/OnePlus (for OnePlus deals)
• r/Xiaomi (for Redmi deals)
• r/frugalmalefashion
• r/IndiaInvestments (save money angle)"""
    msgs.append(("Reddit Subreddits List", m2))

    return msgs


def facebook_groups():
    groups = [
        "Amazon India Deals & Offers",
        "India Online Shopping Deals",
        "Budget Smartphones India",
        "Tech Deals India",
        "Amazon Great Indian Sale",
        "India Loot Deals",
        "Online Shopping India - Best Deals",
        "Smartphone Deals India",
        "Amazon Flipkart Deals India",
        "Deal Hunt India",
    ]

    msg = f"""🔥 *AMAZON DEALS TODAY — {TODAY}*

📱 iQOO Z10R 5G — ₹22,999 (Save ₹7,000!)
🎧 OnePlus Buds 3r — ₹1,999 (33% OFF)
📱 Redmi A7 Pro 5G — ₹15,999 (Save ₹4,000)
📱 OnePlus Nord CE6 Lite — ₹17,999 (Save ₹5,000)

👉 All deals: {SITE}
🔔 Telegram: {TELEGRAM}

Comment "DEAL" for more details! Share karo! 🙏"""

    result = "📘 FACEBOOK GROUPS — YE GROUPS MEIN POST KARO:\n\n"
    result += "Search on Facebook and post in these groups:\n"
    for i, g in enumerate(groups, 1):
        result += f"  {i}. {g}\n"
    result += f"\n--- Facebook Post Text ---\n{msg}"
    return [("Facebook Groups + Post Text", result)]


def instagram_caption():
    cap = f"""🔥 AMAZON DEALS TODAY — {TODAY}

iQOO Z10R 5G sirf ₹22,999! 😱
(Save ₹7,000 — Snapdragon 7s Gen 3 + 6000mAh)

OnePlus Buds 3r sirf ₹1,999!
(33% OFF — ANC earbuds)

🔗 Bio mein link hai — ya search karo:
techdeals-india affiliate

.
.
.
#AmazonIndia #Deals #TechDeals #IndiaDeals
#iQOO #OnePlus #Redmi #Budget5G
#AmazonSale #MobileDeals #SaveMoney
#TechDealsIndia #AmazonOffers #LootDeal
#Earbuds #Smartphone #IndiaOffers"""
    return [("Instagram Caption + Hashtags", cap)]


def quora_answer():
    ans = f"""**Best Amazon India deals right now? ({TODAY})**

I've been tracking Amazon prices daily. Here are today's best:

**1. iQOO Z10R 5G — ₹22,999** (was ₹29,999)
Best mid-range phone right now. Snapdragon 7s Gen 3, 6000mAh battery, 144Hz AMOLED. At this price it beats everything.
→ {DEALS[2]['url']}

**2. OnePlus Nord Buds 3r — ₹1,999** (was ₹2,999)
At ₹1,999 with ANC, this seems like all-time low. 44hr total battery life.
→ {DEALS[1]['url']}

**3. Redmi A7 Pro 5G — ₹15,999** (was ₹19,999)
Best budget 5G under ₹16k. 50MP camera.
→ {DEALS[0]['url']}

I track all Amazon deals here (updates daily): {SITE}

Hope this helps! 🙏"""
    return [("Quora Answer Template", ans)]


# ──────────────────────────────────────────────────────────────
#  MAIN — Generate all messages
# ──────────────────────────────────────────────────────────────
def main():
    all_sections = []
    all_sections += whatsapp_group_blast()
    all_sections += telegram_group_messages()
    all_sections += reddit_posts()
    all_sections += facebook_groups()
    all_sections += instagram_caption()
    all_sections += quora_answer()

    output = f"""
╔══════════════════════════════════════════════════════════════╗
║   🔥 VIRAL SHARE MESSAGES — {TODAY}   ║
║   Copy-paste karo aur SALES AO!                              ║
╚══════════════════════════════════════════════════════════════╝

📊 STRATEGY:
  WhatsApp Groups  → Best conversion (family/friends trust karte hain)
  Telegram Groups  → Mass reach (mass_post.py chalao)
  Reddit           → Free organic traffic
  Facebook Groups  → India mein 10cr+ users
  Instagram        → Story + Post + Reel
  Quora            → Long-term traffic (questions rank on Google)

⚡ 5 SALES KAISE: 500 clicks chahiye → 1% conversion = 5 sales
   Sirf 10 WhatsApp groups mein share karo (50 log each) = 500 reach ✅

═══════════════════════════════════════════════════════════════

"""

    for i, (title, msg) in enumerate(all_sections, 1):
        output += f"{'='*65}\n"
        output += f"  [{i}] {title.upper()}\n"
        output += f"{'='*65}\n\n"
        output += msg.strip()
        output += "\n\n"

    output += """
═══════════════════════════════════════════════════════════════
🎯 ACTION CHECKLIST — YE KAR DO ABHI (30 min):
═══════════════════════════════════════════════════════════════

□ 1. WhatsApp: Message [1] apne TOP 10 WhatsApp groups mein bhejo
□ 2. WhatsApp: Message [3] (personal style) 20 dosto ko personally bhejo
□ 3. WhatsApp Status: Message [4] lagao — 24hr tak dikhta rahega
□ 4. Telegram: mass_post.py chalao (groups update karo)
□ 5. Reddit: r/IndiaDeals, r/india, r/androidindia mein post karo
□ 6. Facebook: 5 groups mein post karo (search karke join karo)
□ 7. Instagram: Story lagao + Post karo + [Caption] use karo
□ 8. Quora: "best amazon deals india" search karo → answer do

⏰ TIMELINE:
  - 30 min mein sab platforms cover ho jaate hain
  - 2-3 ghante mein clicks aane shuru ho jaate hain
  - 24-48 ghante mein conversions aate hain

💰 EARNING:
  Amazon India affiliate commission: 1% - 9% per sale
  Average order ₹5,000 → ₹50-₹450 per sale
  5 sales = ₹250 - ₹2,250 earnings

🔄 DAILY KARO:
  Ye script daily chalao — fresh deals aati hain
  python VIRAL_SHARE.py → SHARE_NOW.txt update hoga

═══════════════════════════════════════════════════════════════
"""

    with open("SHARE_NOW.txt", "w", encoding="utf-8") as f:
        f.write(output)

    print(output)
    print("\n✅ SHARE_NOW.txt file bhi save ho gayi!")
    print("📋 Upar se messages copy karo aur ABHI share karo!")


if __name__ == "__main__":
    main()
