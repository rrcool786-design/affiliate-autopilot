# 🤖 Affiliate Autopilot — Setup Guide
## Ek baar karo, phir system khud chalega

---

## Step 1 — Python Install karo (agar nahi hai)
```
python.org/downloads → Windows installer download karo
Install karte waqt "Add to PATH" tick karo
```

## Step 2 — Dependencies install karo
```bash
pip install openai tweepy schedule requests
```

## Step 3 — API Keys lao (sab FREE hain)

### OpenAI Key
1. platform.openai.com pe jaao
2. Sign up → API Keys → Create new key
3. Copy karo → config.py mein `OPENAI_API_KEY` mein daalo

### Twitter / X Keys
1. developer.twitter.com pe jaao
2. Sign in with Twitter → Create Project → Create App
3. "Free" tier select karo
4. Keys & Tokens section → saari 4 keys copy karo
5. config.py mein daalo

### Gmail App Password
1. myaccount.google.com pe jaao
2. Security → 2-Step Verification ON karo
3. App Passwords → "Mail" select → Generate
4. 16-digit password copy karo → config.py mein `EMAIL_PASSWORD` mein daalo

## Step 4 — Affiliate Links add karo

### Hostinger
1. hostinger.com/affiliates pe jaao
2. Register → Dashboard → Affiliate Link copy karo
3. config.py mein `YOUR_HOSTINGER_AFFILIATE_LINK` replace karo

### SEMrush
1. semrush.com/affiliates pe jaao
2. Join program → unique link copy karo

### ConvertKit
1. convertkit.com/affiliates pe jaao
2. Apply → approval milti hai → link copy karo

### Canva
1. canva.com/affiliates pe jaao
2. Sign up → affiliate link lo

### NordVPN
1. affiliates.nordvpn.com pe jaao
2. Register → link milega dashboard mein

## Step 5 — config.py fill karo
```
config.py file kholo → Notepad/VS Code se
Saare "YOUR_..." replace karo apni real values se
Save karo
```

## Step 6 — System start karo
```bash
python autopilot.py
```
Option 1 → Demo test karo pehle
Option 2 → Full auto mode start karo

---

## System kya karta hai automatically

| Time       | Action                          |
|------------|---------------------------------|
| 08:00 AM   | AI tweet generate + post        |
| 01:00 PM   | AI tweet generate + post        |
| 07:00 PM   | AI tweet generate + post        |
| 10:00 PM   | Email report bhejta hai         |
| 24/7       | CSV mein sab log hota rehta hai |

---

## Files ka kaam

| File                    | Kaam                              |
|-------------------------|-----------------------------------|
| `config.py`             | Tumhari settings — sirf yeh edit karo |
| `autopilot.py`          | Main engine — mat chhedo          |
| `posts_log.csv`         | Saare tweets ka record            |
| `earnings_log.csv`      | Income tracking                   |
| `autopilot.log`         | System ka log                     |

---

## 24/7 Chalne ke liye (PC band na karo ya server use karo)

**Option A — PC on raho** (simple)
Bas `autopilot.py` running rakho

**Option B — Free Cloud Server** (recommended)
1. railway.app pe free account banao
2. GitHub pe apni files upload karo
3. Railway se deploy karo — 24/7 free run hoga

**Option C — Windows Task Scheduler**
1. Task Scheduler open karo
2. Basic Task → Daily → python autopilot.py path
3. PC boot pe bhi auto-start hoga

---

## Earnings track kaise karo

Jab bhi koi affiliate dashboard pe conversion dikhaye:
1. `earnings_log.csv` kholo Excel mein
2. Nayi row add karo: date, product, clicks, conversions
3. Total automatically calculate hoga

Ya autopilot ko batao:
```python
from autopilot import log_earning
log_earning("Hostinger", conversions=2)  # 2 sales = ₹3,000
```

---

## Realistic Income Projection

| Month | Posts/Day | Conversions | Estimated Income |
|-------|-----------|-------------|-----------------|
| 1     | 3         | 2-5/month   | ₹3,000–8,000   |
| 2     | 3         | 5-15/month  | ₹8,000–25,000  |
| 3     | 3         | 15-30/month | ₹25,000–50,000 |

*Followers badhenge to conversions bhi badhenge*

---

## Help chahiye?

Koi bhi step mein atak jao — Claude se poocho, woh solve karega.
