"""
=============================================================
  AFFILIATE CONTENT AUTO-GENERATOR
  Daily social media posts generate karo — automatically

  HOW TO USE:
    pip install openai schedule requests
    python affiliate_content_generator.py
=============================================================
"""

import openai
import schedule
import time
import json
import random
from datetime import datetime

# ─── CONFIG ───────────────────────────────────────────────────────────────────
OPENAI_API_KEY = "sk-YOUR_OPENAI_KEY_HERE"   # openai.com se lo

# Apne affiliate products aur links yahan add karo
AFFILIATE_PRODUCTS = [
    {
        "name": "Hostinger",
        "link": "YOUR_HOSTINGER_AFFILIATE_LINK",
        "category": "web hosting",
        "price": "₹69/month",
        "highlight": "India ka #1 cheap hosting — SSL + domain free",
        "commission": "60% per sale"
    },
    {
        "name": "SEMrush",
        "link": "YOUR_SEMRUSH_AFFILIATE_LINK",
        "category": "SEO tool",
        "price": "$119/month",
        "highlight": "Keyword research + competitor spy tool",
        "commission": "$200/sale"
    },
    {
        "name": "ConvertKit",
        "link": "YOUR_CONVERTKIT_AFFILIATE_LINK",
        "category": "email marketing",
        "price": "Free start",
        "highlight": "Email list banao, automation se paise kamao",
        "commission": "30% recurring lifetime"
    },
    {
        "name": "Canva Pro",
        "link": "YOUR_CANVA_AFFILIATE_LINK",
        "category": "design tool",
        "price": "₹3,999/year",
        "highlight": "Pro graphics bano bina designer ke",
        "commission": "$36/referral"
    },
    {
        "name": "NordVPN",
        "link": "YOUR_NORDVPN_AFFILIATE_LINK",
        "category": "VPN",
        "price": "₹199/month",
        "highlight": "Secure browsing + Netflix unlock",
        "commission": "40% per sale"
    },
]

# Social platforms ke liye format
PLATFORMS = ["Twitter/X", "Instagram caption", "LinkedIn post", "WhatsApp status", "Facebook post"]

# ─── AI CONTENT GENERATOR ─────────────────────────────────────────────────────
def generate_post(product: dict, platform: str) -> str:
    """GPT se fresh affiliate post generate karo"""

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"""
Ek engaging {platform} post likho affiliate product ke liye.

Product: {product['name']}
Category: {product['category']}
Price: {product['price']}
Key benefit: {product['highlight']}
Affiliate link: {product['link']}

Rules:
- Hinglish mein likho (Hindi + English mix)
- Real user ki tarah likho — salesy mat lagao
- Personal experience ke style mein ("Maine try kiya...", "Mere liye kaam kiya...")
- {platform} ke liye sahi length aur tone rakho
- Relevant emojis use karo
- CTA at the end with affiliate link
- Hashtags add karo (agar Twitter/Instagram ho)

Sirf post text do — koi explanation nahi.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.85
    )

    return response.choices[0].message.content.strip()


# ─── DAILY CONTENT BATCH ──────────────────────────────────────────────────────
def generate_daily_batch():
    """Aaj ke liye saare posts generate karo"""

    print(f"\n{'='*60}")
    print(f"📅 Daily Content Batch — {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
    print(f"{'='*60}\n")

    today_content = []

    # Random 3 products + 2 platforms pick karo
    selected_products = random.sample(AFFILIATE_PRODUCTS, min(3, len(AFFILIATE_PRODUCTS)))
    selected_platforms = random.sample(PLATFORMS, 2)

    for product in selected_products:
        for platform in selected_platforms:
            print(f"🔄 Generating: {product['name']} → {platform}...")

            try:
                post = generate_post(product, platform)

                content_item = {
                    "product": product['name'],
                    "platform": platform,
                    "affiliate_link": product['link'],
                    "commission": product['commission'],
                    "post": post,
                    "generated_at": datetime.now().isoformat()
                }

                today_content.append(content_item)

                print(f"\n{'─'*50}")
                print(f"📱 {platform.upper()} | Product: {product['name']}")
                print(f"💰 Commission: {product['commission']}")
                print(f"{'─'*50}")
                print(post)
                print()

                time.sleep(1)  # API rate limit se bachne ke liye

            except Exception as e:
                print(f"❌ Error for {product['name']}: {e}")

    # Save to JSON file
    save_content(today_content)

    print(f"\n✅ {len(today_content)} posts generated aur saved!")
    print(f"📁 File: affiliate_posts_{datetime.now().strftime('%Y-%m-%d')}.json")

    return today_content


def save_content(content: list):
    """Posts ko JSON file mein save karo"""
    filename = f"affiliate_posts_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)


# ─── DEMO MODE (API key ke bina test karo) ────────────────────────────────────
def demo_mode():
    """OpenAI API key ke bina demo posts dikhao"""

    demo_posts = {
        "Hostinger": """Yaar, website banana itna easy ho gaya hai 😮

Maine khud Hostinger try kiya 6 mahine pehle — ₹69/month mein domain + SSL + WordPress sab milta hai!

Seriously, agar blog ya small business site banana hai toh yeh #1 option hai.

👇 Neeche link hai, special discount bhi hai:
[AFFILIATE_LINK]

#Hostinger #WebHosting #BloggingTips #IndianBlogger""",

        "SEMrush": """Competitor ka traffic kaise check karte ho? 🤔

Maine discover kiya SEMrush se — kisi bhi website ka traffic, keywords, backlinks sab dekh sakte ho!

Mera blog grow hua sirf iske wajah se. Free trial bhi hai, try karke dekho.

🔗 Link bio mein hai
[AFFILIATE_LINK]

#SEO #SEMrush #DigitalMarketing #BloggingIndia""",

        "ConvertKit": """Email list = Passive income ka shortcut 📧

Meri email list ne mujhe pichle mahine ₹22,000 dilaye — aur mai uss time so raha tha!

ConvertKit se automation setup karo, ek baar setup karo, lifetime kama te raho.

Free shuru karo → [AFFILIATE_LINK]

#EmailMarketing #PassiveIncome #OnlineIncome"""
    }

    print(f"\n{'='*60}")
    print(f"🎯 DEMO MODE — Sample Affiliate Posts")
    print(f"{'='*60}\n")

    for product_name, post in demo_posts.items():
        product = next(p for p in AFFILIATE_PRODUCTS if p['name'] == product_name)
        post_with_link = post.replace("[AFFILIATE_LINK]", product['link'])

        print(f"{'─'*50}")
        print(f"📱 Instagram/Twitter | {product_name}")
        print(f"💰 Commission: {product['commission']}")
        print(f"{'─'*50}")
        print(post_with_link)
        print()


# ─── SCHEDULER ────────────────────────────────────────────────────────────────
def start_scheduler():
    """Roz subah 8 baje automatically generate karo"""

    print("⏰ Scheduler start ho gaya!")
    print("📅 Daily 8:00 AM pe content auto-generate hoga")
    print("   (Ctrl+C se band karo)\n")

    schedule.every().day.at("08:00").do(generate_daily_batch)

    # Abhi bhi ek baar run karo
    generate_daily_batch()

    while True:
        schedule.run_pending()
        time.sleep(60)


# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║   AFFILIATE CONTENT AUTO-GENERATOR v1.0      ║
║   Daily passive income posts — auto pilot    ║
╚══════════════════════════════════════════════╝

Options:
  1. Demo mode   (API key ke bina — sample posts dekho)
  2. Live mode   (OpenAI API se real posts generate karo)
  3. Scheduler   (Roz subah auto-generate karo)
""")

    choice = input("Choose (1/2/3): ").strip()

    if choice == "1":
        demo_mode()

    elif choice == "2":
        if OPENAI_API_KEY == "sk-YOUR_OPENAI_KEY_HERE":
            print("\n⚠️  Pehle OPENAI_API_KEY set karo file ke top mein!")
            print("   openai.com/api-keys se free key lo")
        else:
            generate_daily_batch()

    elif choice == "3":
        if OPENAI_API_KEY == "sk-YOUR_OPENAI_KEY_HERE":
            print("\n⚠️  Pehle OPENAI_API_KEY set karo file ke top mein!")
        else:
            start_scheduler()
    else:
        print("Invalid choice. 1, 2, ya 3 enter karo.")
