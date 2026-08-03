# 📊 Click Tracker Setup — 15 Minutes, Free Forever

Yeh system track karega kaunse products pe sabse zyada clicks aa rahe hain,
aur automatically top performers ko Telegram pe promote karega.

---

## Architecture

```
Website (GitHub Pages)
  │
  │ navigator.sendBeacon (on every "Buy" click)
  ▼
Cloudflare Worker  ← FREE (100k req/day)
  │
  ├── KV Store (click counts per ASIN)
  │
  └── /today endpoint
        │
        ▼
  GitHub Action (10pm IST daily)
        │
        ├── click_report.py
        │     → Posts top 5 products to Telegram
        │     → Saves hot_products.json
        │
        └── post_once.py (next morning)
              → 50% chance: promotes hot product
```

---

## Step 1 — Cloudflare Account (2 min)

1. **workers.cloudflare.com** pe jaao
2. **Sign up** — email se, no credit card needed
3. Free tier: **100,000 requests/day** (bahut zyada hai)

---

## Step 2 — KV Namespace banao (1 min)

1. Cloudflare Dashboard → **Workers & Pages** → **KV**
2. **Create namespace** → Name: `CLICKS` → Create

---

## Step 3 — Worker deploy karo (5 min)

1. Workers & Pages → **Create Application** → **Create Worker**
2. Worker ka naam: `deal-tracker`
3. **Edit code** → saara `cloudflare_tracker.js` ka code paste karo
4. **Save and Deploy**
5. Worker URL copy karo: `https://deal-tracker.YOURNAME.workers.dev`

---

## Step 4 — KV Binding lagao (2 min)

1. Worker pe click karo → **Settings** → **Variables**
2. **KV Namespace Bindings** → **Add binding**
3. Variable name: `CLICKS`
4. KV namespace: `CLICKS` (jo Step 2 mein banaya)
5. **Save**

---

## Step 5 — Worker URL website mein daalo (2 min)

`generate_website.py` open karo, yeh line dhundo:
```python
const TRACKER_URL = '';  // e.g. 'https://deal-tracker.yourname.workers.dev'
```

Apna URL daalo:
```python
const TRACKER_URL = 'https://deal-tracker.YOURNAME.workers.dev';
```

Phir run karo:
```
python generate_website.py
```

---

## Step 6 — GitHub Secret add karo (1 min)

GitHub repo → Settings → Secrets → Actions → New secret:
```
Name:  TRACKER_URL
Value: https://deal-tracker.YOURNAME.workers.dev
```

---

## Step 7 — Commit karo

```
COMMIT_UPGRADE.bat
```

---

## ✅ Test karo

1. Website open karo
2. Kisi bhi product pe **"Buy on Amazon"** click karo
3. Worker URL pe jaao: `https://deal-tracker.YOURNAME.workers.dev/today`
4. JSON mein tumhara click dikhega!

---

## 📊 Dashboards

| URL | Kya dikhata hai |
|-----|-----------------|
| `/today` | Aaj ke clicks, top products |
| `/top` | All-time top 10 products |
| `/stats` | Saare ASINs ke click counts |

---

## 🤖 Auto-report

Har roz **10:00 PM IST** pe GitHub Action chalega:
- Top clicked products fetch karega
- Telegram pe report post karega
- `hot_products.json` update karega
- Agla din ke posts mein hot products 50% chance se feature honge

**Isse tumhe pata chalega exactly kaunse products convert ho rahe hain** —
aur system automatically unhe promote karega!
