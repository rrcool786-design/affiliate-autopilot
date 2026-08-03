# 🔍 SEO Setup — Google Indexing Guide
## Yeh karo aur website Google pe rank karegi

---

## ✅ Step 1 — GitHub pe push karo (COMMIT_UPGRADE.bat run karo)

```
COMMIT_UPGRADE.bat double-click karo
```

Yeh automatically push karega:
- `docs/index.html` — website (JSON-LD schema + OG tags included)
- `docs/sitemap.xml` — 157 product URLs
- `docs/robots.txt` — Google crawling allow

---

## ✅ Step 2 — Google Search Console mein submit karo (FREE, 5 min)

1. **search.google.com/search-console** pe jaao
2. **"Add Property"** click karo
3. **URL prefix** choose karo → enter karo:
   ```
   https://rrcool786-design.github.io/affiliate-autopilot/
   ```
4. **Verify** karo → "HTML tag" method choose karo
5. Woh dega ek `<meta name="google-site-verification" content="XXXXX">` tag
6. `generate_website.py` mein is line ke baad add karo:
   ```python
   <link rel="canonical" href="{SITE_URL}/">
   ```
   Yeh add karo:
   ```python
   <meta name="google-site-verification" content="TUMHARA_CODE_YAHAN">
   ```
7. Phir `generate_website.py` run karo → commit karo

---

## ✅ Step 3 — Sitemap submit karo

Search Console mein:
1. Left sidebar → **Sitemaps**
2. Enter karo: `sitemap.xml`
3. **Submit** karo

Google 24-48 ghante mein index karega.

---

## ✅ Step 4 — Bing Webmaster Tools (bonus traffic)

1. **bing.com/webmasters** pe jaao
2. "Import from Google Search Console" → one-click setup
3. Free traffic from Bing + DuckDuckGo bhi milega

---

## 📊 Kya expect karo

| Timeline | Result |
|----------|--------|
| 1-2 days | Google crawl karega |
| 1 week   | Indexed pages dikhenge |
| 2-4 weeks | Ranking shuru — "amazon deals india" type queries |
| 1-3 months | Organic traffic aana shuru |

---

## 🎯 Target Keywords (automatically optimized)

- `amazon deals india today`
- `best amazon offers india`
- `amazon electronics sale india`
- `redmi phone offer today`
- `laptop under 35000 amazon`
- `earbuds under 2000 amazon india`

---

## 🔁 Auto-update (already working!)

`update_website.yml` GitHub Action:
- Runs daily at 06:30 IST
- Re-generates website with fresh data
- Updates sitemap.xml with today's date
- Auto-commits → auto-deploys to GitHub Pages

**You literally don't have to do anything after Step 1-3 above.**
