"""
Professional Amazon Deals Website Generator - 10x UPGRADED
Daily auto-generate — GitHub Pages pe free hosting
Smart Search + 158 Products + Autocomplete + Wishlist + WhatsApp Share
"""

import requests
import json
import os
import re
import random
from datetime import datetime

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

AFFILIATE_TAG    = "rahulfinds20c-21"
TELEGRAM_CHANNEL = "https://t.me/TechDealsIndia_channel"
SITE_URL         = "https://rrcool786-design.github.io/affiliate-autopilot"
OUTPUT_DIR       = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
OUTPUT_FILE      = os.path.join(OUTPUT_DIR, "index.html")
PRODUCTS_JSON    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.json")

CATEGORIES = [
    {"url": "https://www.amazon.in/gp/bestsellers/electronics/",    "name": "Electronics",  "emoji": "📱", "commission_pct": 0.04},
    {"url": "https://www.amazon.in/gp/bestsellers/computers/",      "name": "Laptops",      "emoji": "💻", "commission_pct": 0.04},
    {"url": "https://www.amazon.in/gp/bestsellers/kitchen/",        "name": "Kitchen",      "emoji": "🍳", "commission_pct": 0.05},
    {"url": "https://www.amazon.in/gp/bestsellers/home/",           "name": "Home",         "emoji": "🏠", "commission_pct": 0.05},
    {"url": "https://www.amazon.in/gp/bestsellers/apparel/",        "name": "Fashion",      "emoji": "👕", "commission_pct": 0.09},
    {"url": "https://www.amazon.in/gp/bestsellers/sporting-goods/", "name": "Sports",       "emoji": "⚽", "commission_pct": 0.05},
    {"url": "https://www.amazon.in/gp/bestsellers/beauty/",         "name": "Beauty",       "emoji": "💄", "commission_pct": 0.06},
    {"url": "https://www.amazon.in/gp/bestsellers/books/",          "name": "Books",        "emoji": "📚", "commission_pct": 0.05},
    {"url": "https://www.amazon.in/gp/bestsellers/toys/",           "name": "Toys",         "emoji": "🧸", "commission_pct": 0.05},
    {"url": "https://www.amazon.in/gp/bestsellers/health/",         "name": "Health",       "emoji": "💊", "commission_pct": 0.05},
]

HEADERS_LIST = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36", "Accept-Language": "en-IN,en;q=0.9"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36", "Accept-Language": "en-US,en;q=0.8"},
]

EMERGENCY_PRODUCTS = [
    # ── ELECTRONICS / MOBILES ──────────────────────────────────────────────
    {"name": "Redmi A7 Pro 5G",                          "asin": "B0GS5Y6BD3",  "category": "Electronics", "emoji": "📱", "price": 15999, "original_price": 19999, "discount": 20, "rating": 4.2, "reviews": 1823},
    {"name": "OnePlus Buds 3r TWS Earbuds",              "asin": "B0FMDL81GS",  "category": "Electronics", "emoji": "🎧", "price": 1999,  "original_price": 2999,  "discount": 33, "rating": 4.4, "reviews": 3201},
    {"name": "iQOO Z10R 5G",                             "asin": "B0FHB5V36G",  "category": "Electronics", "emoji": "📱", "price": 22999, "original_price": 29999, "discount": 23, "rating": 4.3, "reviews": 982},
    {"name": "OnePlus Nord CE6 Lite 5G",                 "asin": "B0GVYDLJJQ",  "category": "Electronics", "emoji": "📱", "price": 17999, "original_price": 22999, "discount": 22, "rating": 4.1, "reviews": 1456},
    {"name": "Samsung Galaxy A16 5G",                    "asin": "B0DJZZ7BPH",  "category": "Electronics", "emoji": "📱", "price": 16999, "original_price": 21999, "discount": 23, "rating": 4.3, "reviews": 2341},
    {"name": "boAt Rockerz 450 Wireless Headphone",      "asin": "B07DCPRNZD",  "category": "Electronics", "emoji": "🎧", "price": 999,   "original_price": 3990,  "discount": 75, "rating": 4.1, "reviews": 89234},
    {"name": "Noise ColorFit Pro 5 Smartwatch",          "asin": "B0BWQN8CHZ",  "category": "Electronics", "emoji": "⌚", "price": 2499,  "original_price": 5999,  "discount": 58, "rating": 4.2, "reviews": 12891},
    {"name": "Realme Narzo N65 5G",                      "asin": "B0D5Q6VTMT",  "category": "Electronics", "emoji": "📱", "price": 12999, "original_price": 15999, "discount": 19, "rating": 4.0, "reviews": 3421},
    {"name": "Fire-Boltt Phoenix Ultra Smartwatch",      "asin": "B0BXFC2WJQ",  "category": "Electronics", "emoji": "⌚", "price": 1299,  "original_price": 4999,  "discount": 74, "rating": 4.0, "reviews": 45231},
    {"name": "Mivi DuoPods A350 TWS",                    "asin": "B09YNBR5M3",  "category": "Electronics", "emoji": "🎧", "price": 699,   "original_price": 2999,  "discount": 77, "rating": 3.9, "reviews": 18234},
    {"name": "Redmi Note 13 5G 8GB",                     "asin": "B0CRD5GFWZ",  "category": "Electronics", "emoji": "📱", "price": 18999, "original_price": 24999, "discount": 24, "rating": 4.3, "reviews": 8921},
    {"name": "JBL Tune 215BT Wireless Earbuds",          "asin": "B09SW3GGHQ",  "category": "Electronics", "emoji": "🎧", "price": 1299,  "original_price": 3499,  "discount": 63, "rating": 4.2, "reviews": 34521},
    {"name": "Samsung Galaxy M35 5G",                    "asin": "B0D3XRJCNK",  "category": "Electronics", "emoji": "📱", "price": 19999, "original_price": 25999, "discount": 23, "rating": 4.2, "reviews": 5623},
    {"name": "Zebronics Zeb-Duke1 Wireless Headphone",   "asin": "B0BPLM83FC",  "category": "Electronics", "emoji": "🎧", "price": 599,   "original_price": 2999,  "discount": 80, "rating": 3.8, "reviews": 23421},
    {"name": "MI 43 inch 4K Ultra HD Smart TV",          "asin": "B08L5TNJHG",  "category": "Electronics", "emoji": "📺", "price": 24999, "original_price": 39999, "discount": 38, "rating": 4.3, "reviews": 12341},
    {"name": "Portronics Harmonics Twins S10 TWS",       "asin": "B0C8ZS2MBF",  "category": "Electronics", "emoji": "🎧", "price": 499,   "original_price": 2999,  "discount": 83, "rating": 3.7, "reviews": 8934},
    {"name": "Lava Agni 3 5G",                           "asin": "B0CV8QRDDS",  "category": "Electronics", "emoji": "📱", "price": 21999, "original_price": 27999, "discount": 21, "rating": 4.1, "reviews": 2341},
    {"name": "Sony WH-1000XM4 Noise Cancelling",        "asin": "B08C7KG5LP",  "category": "Electronics", "emoji": "🎧", "price": 19990, "original_price": 29990, "discount": 33, "rating": 4.7, "reviews": 45231},
    {"name": "boAt Wave Lite 2 Smartwatch",              "asin": "B0BZFT7QK7",  "category": "Electronics", "emoji": "⌚", "price": 899,   "original_price": 3990,  "discount": 77, "rating": 4.0, "reviews": 19231},
    {"name": "Redmi 13C 5G",                             "asin": "B0CQPXQNJC",  "category": "Electronics", "emoji": "📱", "price": 10999, "original_price": 13999, "discount": 21, "rating": 4.0, "reviews": 12432},
    {"name": "Ambrane Dots Buds TWS Earbuds",            "asin": "B09QK43V4M",  "category": "Electronics", "emoji": "🎧", "price": 399,   "original_price": 1999,  "discount": 80, "rating": 3.8, "reviews": 31245},
    {"name": "Noise Twist Go Smartwatch",                "asin": "B0CM2ZQMYL",  "category": "Electronics", "emoji": "⌚", "price": 1299,  "original_price": 3999,  "discount": 68, "rating": 4.1, "reviews": 7823},
    {"name": "iQOO Neo 9 Pro 5G 12GB",                  "asin": "B0CW3MWXLZ",  "category": "Electronics", "emoji": "📱", "price": 29999, "original_price": 39999, "discount": 25, "rating": 4.5, "reviews": 4321},
    {"name": "Boult Audio W40 TWS Earbuds",              "asin": "B0CDY1B57P",  "category": "Electronics", "emoji": "🎧", "price": 899,   "original_price": 3999,  "discount": 78, "rating": 4.0, "reviews": 14231},
    {"name": "Samsung Galaxy Watch 6 44mm",              "asin": "B0C8KTZ5G8",  "category": "Electronics", "emoji": "⌚", "price": 19999, "original_price": 29999, "discount": 33, "rating": 4.4, "reviews": 6234},
    {"name": "Motorola Moto G64 5G",                     "asin": "B0CYGL2DVX",  "category": "Electronics", "emoji": "📱", "price": 16999, "original_price": 22999, "discount": 26, "rating": 4.2, "reviews": 3421},
    {"name": "OnePlus Nord Buds 3 TWS",                  "asin": "B0D1XZY8GT",  "category": "Electronics", "emoji": "🎧", "price": 2499,  "original_price": 3999,  "discount": 38, "rating": 4.3, "reviews": 5231},
    {"name": "Tecno Pova 6 Pro 5G",                      "asin": "B0CZGRGHSZ",  "category": "Electronics", "emoji": "📱", "price": 18999, "original_price": 24999, "discount": 24, "rating": 4.0, "reviews": 1823},
    {"name": "Realme Watch S2",                          "asin": "B0CXQFGTLP",  "category": "Electronics", "emoji": "⌚", "price": 2499,  "original_price": 4999,  "discount": 50, "rating": 4.1, "reviews": 3412},
    {"name": "Infinix Hot 50 Pro+ 5G",                  "asin": "B0DDJNMD3V",  "category": "Electronics", "emoji": "📱", "price": 14999, "original_price": 19999, "discount": 25, "rating": 4.0, "reviews": 2341},

    # ── LAPTOPS ────────────────────────────────────────────────────────────
    {"name": "Lenovo IdeaPad Slim 3 AMD Ryzen 5",       "asin": "B0C3WBQJ4D",  "category": "Laptops",      "emoji": "💻", "price": 34990, "original_price": 54990, "discount": 36, "rating": 4.3, "reviews": 8921},
    {"name": "ASUS VivoBook 15 Intel Core i3",          "asin": "B0CX8MLHQM",  "category": "Laptops",      "emoji": "💻", "price": 29990, "original_price": 42990, "discount": 30, "rating": 4.2, "reviews": 5432},
    {"name": "HP 15s Ryzen 3 5300U Laptop",             "asin": "B09WPMY6T5",  "category": "Laptops",      "emoji": "💻", "price": 37990, "original_price": 55000, "discount": 31, "rating": 4.4, "reviews": 12341},
    {"name": "Acer Aspire Lite AMD Ryzen 5",            "asin": "B0BTGX9FXP",  "category": "Laptops",      "emoji": "💻", "price": 32990, "original_price": 49999, "discount": 34, "rating": 4.2, "reviews": 7823},
    {"name": "DELL Inspiron 3520 Intel Core i5",        "asin": "B0CX35T5M7",  "category": "Laptops",      "emoji": "💻", "price": 44990, "original_price": 62990, "discount": 29, "rating": 4.3, "reviews": 4321},
    {"name": "Lenovo LOQ AMD Ryzen 5 Gaming",           "asin": "B0CQNTMG6K",  "category": "Laptops",      "emoji": "🎮", "price": 62990, "original_price": 89990, "discount": 30, "rating": 4.5, "reviews": 3412},
    {"name": "Mi Notebook 14 Intel Core i5",            "asin": "B08GVF5KDT",  "category": "Laptops",      "emoji": "💻", "price": 42990, "original_price": 59999, "discount": 28, "rating": 4.1, "reviews": 9823},
    {"name": "ASUS TUF Gaming F15 Intel Core i5",       "asin": "B0D46P1NLJ",  "category": "Laptops",      "emoji": "🎮", "price": 54990, "original_price": 79990, "discount": 31, "rating": 4.4, "reviews": 6234},
    {"name": "HP Pavilion x360 Intel Core i5 Touch",   "asin": "B0CK5R7CWN",  "category": "Laptops",      "emoji": "💻", "price": 52990, "original_price": 74990, "discount": 29, "rating": 4.3, "reviews": 2341},
    {"name": "Acer Nitro V Gaming AMD Ryzen 5",         "asin": "B0CWVL9XF9",  "category": "Laptops",      "emoji": "🎮", "price": 57990, "original_price": 79990, "discount": 28, "rating": 4.4, "reviews": 4523},
    {"name": "Lenovo V15 G4 Intel Core i3",             "asin": "B0D3KFRT28",  "category": "Laptops",      "emoji": "💻", "price": 27990, "original_price": 40990, "discount": 32, "rating": 4.1, "reviews": 3231},
    {"name": "MSI Thin 15 Intel Core i5 RTX 3050",     "asin": "B0CZDTJ9GQ",  "category": "Laptops",      "emoji": "🎮", "price": 59990, "original_price": 84990, "discount": 29, "rating": 4.5, "reviews": 1923},

    # ── KITCHEN ─────────────────────────────────────────────────────────────
    {"name": "Prestige Svachh 5 L Pressure Cooker",    "asin": "B00IE7T3C0",  "category": "Kitchen",      "emoji": "🍳", "price": 1299,  "original_price": 2595,  "discount": 50, "rating": 4.4, "reviews": 34521},
    {"name": "Butterfly Smart 750W Mixer Grinder",      "asin": "B07C34KLZS",  "category": "Kitchen",      "emoji": "🍳", "price": 1799,  "original_price": 4000,  "discount": 55, "rating": 4.3, "reviews": 18234},
    {"name": "Pigeon by Stovekraft 1.5L Electric Kettle","asin": "B01M7PXQSC","category": "Kitchen",      "emoji": "☕", "price": 599,   "original_price": 1295,  "discount": 54, "rating": 4.2, "reviews": 45231},
    {"name": "Wonderchef Nutri-Blend 400W Juicer",      "asin": "B07RZGBWWN",  "category": "Kitchen",      "emoji": "🥤", "price": 1599,  "original_price": 3995,  "discount": 60, "rating": 4.3, "reviews": 12891},
    {"name": "Amazon Basics 1.8 L Rice Cooker",         "asin": "B07H7JN45R",  "category": "Kitchen",      "emoji": "🍚", "price": 1099,  "original_price": 2499,  "discount": 56, "rating": 4.1, "reviews": 23421},
    {"name": "Lifelong LLHM201 600W Hand Mixer",        "asin": "B07NKQRVRC",  "category": "Kitchen",      "emoji": "🍳", "price": 449,   "original_price": 1499,  "discount": 70, "rating": 4.0, "reviews": 19231},
    {"name": "Preethi Blue Leaf 550W Mixer Grinder",    "asin": "B01IDDX8ZE",  "category": "Kitchen",      "emoji": "🍳", "price": 2299,  "original_price": 4295,  "discount": 46, "rating": 4.4, "reviews": 31245},
    {"name": "Milton Thermosteel Flip Lid Flask 500ml", "asin": "B01BHUVHC6",  "category": "Kitchen",      "emoji": "🍶", "price": 499,   "original_price": 1295,  "discount": 61, "rating": 4.5, "reviews": 89234},
    {"name": "Bajaj Majesty 1000W 2-Slice Pop-up Toaster","asin": "B00FIWNBK0","category": "Kitchen",     "emoji": "🍞", "price": 799,   "original_price": 1995,  "discount": 60, "rating": 4.1, "reviews": 14231},
    {"name": "Hawkins Futura Hard Anodised 3L Pressure",  "asin": "B002RH33VO","category": "Kitchen",     "emoji": "🍳", "price": 1999,  "original_price": 3595,  "discount": 44, "rating": 4.5, "reviews": 45231},
    {"name": "Philips HD2647/90 820W Sandwich Maker",   "asin": "B00GFVWDRS",  "category": "Kitchen",      "emoji": "🥪", "price": 1099,  "original_price": 2195,  "discount": 50, "rating": 4.2, "reviews": 34521},
    {"name": "Usha Lexus 750 Plus 4-Jar Mixer",         "asin": "B01H3T5TA0",  "category": "Kitchen",      "emoji": "🍳", "price": 2499,  "original_price": 4795,  "discount": 48, "rating": 4.3, "reviews": 7823},
    {"name": "Borosil Stainless Steel Handi Casserole", "asin": "B00VOPWZ5I",  "category": "Kitchen",      "emoji": "🍲", "price": 699,   "original_price": 1795,  "discount": 61, "rating": 4.4, "reviews": 23421},
    {"name": "Cello World Plastic Opalware Dinner Set", "asin": "B01M29D25S",  "category": "Kitchen",      "emoji": "🍽️", "price": 999,   "original_price": 2495,  "discount": 60, "rating": 4.1, "reviews": 12341},
    {"name": "Inalsa Nutri Mixer Grinder 1000W",        "asin": "B0BZKBFN3D",  "category": "Kitchen",      "emoji": "🍳", "price": 1699,  "original_price": 3999,  "discount": 58, "rating": 4.2, "reviews": 4321},
    {"name": "Kent 16023 Vegetable and Fruit Steamer",  "asin": "B07RCFTYGN",  "category": "Kitchen",      "emoji": "🥦", "price": 1299,  "original_price": 3000,  "discount": 57, "rating": 4.2, "reviews": 8921},
    {"name": "Prestige IRIS 750W Juicer Mixer Grinder", "asin": "B075CQ16LJ",  "category": "Kitchen",      "emoji": "🥤", "price": 1799,  "original_price": 3995,  "discount": 55, "rating": 4.3, "reviews": 5432},
    {"name": "Solimo Stainless Steel Induction Base Kadhai","asin":"B07FBP63ZP","category": "Kitchen",     "emoji": "🍳", "price": 499,   "original_price": 1499,  "discount": 67, "rating": 4.3, "reviews": 19231},

    # ── BEAUTY ──────────────────────────────────────────────────────────────
    {"name": "Lakme 9 to 5 Weightless Mousse Foundation","asin": "B01FIOMQHC","category": "Beauty",       "emoji": "💄", "price": 349,   "original_price": 699,   "discount": 50, "rating": 4.2, "reviews": 34521},
    {"name": "Maybelline Fit Me Matte Foundation",       "asin": "B01MRQE9HH", "category": "Beauty",       "emoji": "💄", "price": 299,   "original_price": 599,   "discount": 50, "rating": 4.3, "reviews": 45231},
    {"name": "Biotique Bio Papaya Tan Removal Scrub",    "asin": "B00FMHILOA", "category": "Beauty",       "emoji": "🧴", "price": 99,    "original_price": 299,   "discount": 67, "rating": 4.1, "reviews": 23421},
    {"name": "Himalaya Herbals Nourishing Skin Cream",  "asin": "B009KU0XRQ",  "category": "Beauty",       "emoji": "🧴", "price": 99,    "original_price": 199,   "discount": 50, "rating": 4.4, "reviews": 89234},
    {"name": "WOW Skin Science Apple Cider Vinegar Shampoo","asin":"B074HMDJQ7","category":"Beauty",        "emoji": "🧴", "price": 349,   "original_price": 699,   "discount": 50, "rating": 4.2, "reviews": 45231},
    {"name": "Philips BHH777 Kerashine Temperature Control Hair Dryer","asin":"B0878C7R3X","category":"Beauty","emoji":"💇","price":1299,"original_price":2995,"discount":57, "rating": 4.3, "reviews": 12341},
    {"name": "Nivea Men Dark Spot Reduction Face Wash",  "asin": "B00DE78CAE", "category": "Beauty",       "emoji": "🧴", "price": 129,   "original_price": 285,   "discount": 55, "rating": 4.2, "reviews": 34521},
    {"name": "L'Oreal Paris Hair Spa Deep Nourishing Mask","asin":"B01LX8KGAL","category":"Beauty",        "emoji": "💇", "price": 299,   "original_price": 599,   "discount": 50, "rating": 4.2, "reviews": 18234},
    {"name": "Veet Body Hair Removal Cream Normal Skin", "asin": "B00MXK4YNG", "category": "Beauty",       "emoji": "🧴", "price": 199,   "original_price": 430,   "discount": 54, "rating": 4.1, "reviews": 23421},
    {"name": "Syska Glam 1200W Hair Dryer",             "asin": "B00L0XTEKK",  "category": "Beauty",       "emoji": "💇", "price": 499,   "original_price": 1295,  "discount": 61, "rating": 4.0, "reviews": 19231},
    {"name": "Plum Grape Seed & Sea Buckthorn Serum",   "asin": "B07X3B4HG8",  "category": "Beauty",       "emoji": "🧴", "price": 399,   "original_price": 799,   "discount": 50, "rating": 4.3, "reviews": 12341},
    {"name": "Mamaearth Onion Hair Oil for Hair Regrowth","asin":"B079RCZXFG","category":"Beauty",         "emoji": "💇", "price": 249,   "original_price": 499,   "discount": 50, "rating": 4.2, "reviews": 45231},
    {"name": "Colorbar Cosmetics Plum Tweed Lip Color", "asin": "B07ZWF3JLM",  "category": "Beauty",       "emoji": "💄", "price": 199,   "original_price": 499,   "discount": 60, "rating": 4.1, "reviews": 8921},
    {"name": "Neutrogena Ultra Light Cleansing Lotion", "asin": "B082P4X7HL",  "category": "Beauty",       "emoji": "🧴", "price": 249,   "original_price": 499,   "discount": 50, "rating": 4.2, "reviews": 14231},
    {"name": "Braun Satin Hair 3 Style & Go Cordless Straightener","asin":"B09QNGJGHL","category":"Beauty","emoji":"💇","price":1499,"original_price":3499,"discount":57,"rating":4.2,"reviews":7823},
    {"name": "Garnier Bright Complete Vitamin C Serum Cream","asin":"B086FK9G7D","category":"Beauty",      "emoji": "🧴", "price": 199,   "original_price": 445,   "discount": 55, "rating": 4.2, "reviews": 31245},

    # ── FASHION ─────────────────────────────────────────────────────────────
    {"name": "Urbano Fashion Men Slim Fit Jeans",       "asin": "B07PGKHM1X",  "category": "Fashion",      "emoji": "👖", "price": 699,   "original_price": 2999,  "discount": 77, "rating": 4.0, "reviews": 23421},
    {"name": "Amazon Brand - Symbol Men Regular Fit T-Shirt","asin":"B07KGDLF5X","category":"Fashion",    "emoji": "👕", "price": 299,   "original_price": 799,   "discount": 63, "rating": 4.1, "reviews": 45231},
    {"name": "Levi's Men 511 Slim Fit Jeans",           "asin": "B073BJJMFJ",  "category": "Fashion",      "emoji": "👖", "price": 1599,  "original_price": 3999,  "discount": 60, "rating": 4.3, "reviews": 34521},
    {"name": "Campus Men Running Shoes",                "asin": "B09QPXK7RM",  "category": "Fashion",      "emoji": "👟", "price": 899,   "original_price": 2495,  "discount": 64, "rating": 4.1, "reviews": 18234},
    {"name": "Adidas Men Adizero Running Shoes",        "asin": "B0BZTV8NSZ",  "category": "Fashion",      "emoji": "👟", "price": 2799,  "original_price": 5999,  "discount": 53, "rating": 4.4, "reviews": 8921},
    {"name": "Van Heusen Men Regular Fit Cotton Shirt", "asin": "B08FHBM62Z",  "category": "Fashion",      "emoji": "👔", "price": 699,   "original_price": 1899,  "discount": 63, "rating": 4.2, "reviews": 12341},
    {"name": "Puma Men Liga Core Polo T-Shirt",         "asin": "B07FNF4ZN8",  "category": "Fashion",      "emoji": "👕", "price": 699,   "original_price": 1799,  "discount": 61, "rating": 4.2, "reviews": 23421},
    {"name": "HRX by Hrithik Roshan Men Active Shorts", "asin": "B0761NXMGR",  "category": "Fashion",      "emoji": "🩳", "price": 499,   "original_price": 1299,  "discount": 62, "rating": 4.1, "reviews": 19231},
    {"name": "Wrangler Men Slim Fit Stretch Jeans",     "asin": "B07G7VJG5H",  "category": "Fashion",      "emoji": "👖", "price": 1299,  "original_price": 3499,  "discount": 63, "rating": 4.2, "reviews": 14231},
    {"name": "Wildcraft Unisex Backpack 40L",           "asin": "B00QR4LNPM",  "category": "Fashion",      "emoji": "🎒", "price": 999,   "original_price": 2995,  "discount": 67, "rating": 4.2, "reviews": 34521},
    {"name": "Fastrack Analog Women Watch",             "asin": "B08CQJLQQ5",  "category": "Fashion",      "emoji": "⌚", "price": 999,   "original_price": 2995,  "discount": 67, "rating": 4.1, "reviews": 12341},
    {"name": "Amazon Brand - Inkast Men Slim Fit Chino","asin": "B07H7YD3W3",  "category": "Fashion",      "emoji": "👖", "price": 599,   "original_price": 1799,  "discount": 67, "rating": 4.0, "reviews": 23421},
    {"name": "Crocs Men Swiftwater Flip Flop",          "asin": "B07DVLG6LN",  "category": "Fashion",      "emoji": "👡", "price": 999,   "original_price": 2495,  "discount": 60, "rating": 4.3, "reviews": 8921},
    {"name": "Skechers Men Go Walk 7 Slip On Shoes",    "asin": "B0C7KRPWMG",  "category": "Fashion",      "emoji": "👟", "price": 2499,  "original_price": 5999,  "discount": 58, "rating": 4.4, "reviews": 5432},
    {"name": "Wrogn Men Solid Slim Fit Polo T-Shirt",   "asin": "B08FZMD5FX",  "category": "Fashion",      "emoji": "👕", "price": 499,   "original_price": 1299,  "discount": 62, "rating": 4.1, "reviews": 7823},
    {"name": "American Tourister Zap+ Small Cabin Bag", "asin": "B09NFWVS5Q",  "category": "Fashion",      "emoji": "🧳", "price": 2299,  "original_price": 5795,  "discount": 60, "rating": 4.3, "reviews": 4321},
    {"name": "Puma Men Vibrancy Sneakers",              "asin": "B0BWNJMNJH",  "category": "Fashion",      "emoji": "👟", "price": 1799,  "original_price": 4499,  "discount": 60, "rating": 4.2, "reviews": 3412},
    {"name": "Nivia Storm Running Shoes",               "asin": "B09Q2W4YCX",  "category": "Fashion",      "emoji": "👟", "price": 799,   "original_price": 1999,  "discount": 60, "rating": 4.0, "reviews": 9823},

    # ── BOOKS ───────────────────────────────────────────────────────────────
    {"name": "Atomic Habits by James Clear",            "asin": "B07RFSSYBH",  "category": "Books",        "emoji": "📚", "price": 299,   "original_price": 799,   "discount": 63, "rating": 4.7, "reviews": 89234},
    {"name": "The Psychology of Money - Morgan Housel", "asin": "B08FTNKJNF",  "category": "Books",        "emoji": "📚", "price": 249,   "original_price": 499,   "discount": 50, "rating": 4.6, "reviews": 45231},
    {"name": "Rich Dad Poor Dad - Robert Kiyosaki",     "asin": "B07C7M9JH2",  "category": "Books",        "emoji": "📚", "price": 199,   "original_price": 399,   "discount": 50, "rating": 4.6, "reviews": 67234},
    {"name": "The Alchemist - Paulo Coelho",            "asin": "B00GYYTVR8",  "category": "Books",        "emoji": "📚", "price": 149,   "original_price": 299,   "discount": 50, "rating": 4.6, "reviews": 56234},
    {"name": "Zero to One - Peter Thiel",               "asin": "B00J6YBOFQ",  "category": "Books",        "emoji": "📚", "price": 299,   "original_price": 599,   "discount": 50, "rating": 4.5, "reviews": 23421},
    {"name": "Think and Grow Rich - Napoleon Hill",     "asin": "B07DBHGG6H",  "category": "Books",        "emoji": "📚", "price": 99,    "original_price": 299,   "discount": 67, "rating": 4.5, "reviews": 34521},
    {"name": "The 5 AM Club - Robin Sharma",            "asin": "B07GWPGHLS",  "category": "Books",        "emoji": "📚", "price": 249,   "original_price": 499,   "discount": 50, "rating": 4.4, "reviews": 18234},
    {"name": "Deep Work - Cal Newport",                 "asin": "B0189PVAWY",  "category": "Books",        "emoji": "📚", "price": 349,   "original_price": 699,   "discount": 50, "rating": 4.5, "reviews": 12341},
    {"name": "Sapiens - Yuval Noah Harari",             "asin": "B00K7ED54M",  "category": "Books",        "emoji": "📚", "price": 349,   "original_price": 799,   "discount": 56, "rating": 4.5, "reviews": 45231},
    {"name": "Start with Why - Simon Sinek",            "asin": "B004YJPENO",  "category": "Books",        "emoji": "📚", "price": 249,   "original_price": 499,   "discount": 50, "rating": 4.4, "reviews": 19231},
    {"name": "The Lean Startup - Eric Ries",            "asin": "B004J4XGN6",  "category": "Books",        "emoji": "📚", "price": 299,   "original_price": 699,   "discount": 57, "rating": 4.4, "reviews": 14231},
    {"name": "Can't Hurt Me - David Goggins",           "asin": "B07KKP62FW",  "category": "Books",        "emoji": "📚", "price": 349,   "original_price": 799,   "discount": 56, "rating": 4.6, "reviews": 34521},
    {"name": "The 48 Laws of Power - Robert Greene",    "asin": "B0B37KTGBQ",  "category": "Books",        "emoji": "📚", "price": 399,   "original_price": 999,   "discount": 60, "rating": 4.5, "reviews": 8921},
    {"name": "Ikigai - The Japanese Secret",            "asin": "B07BNHB9Q9",  "category": "Books",        "emoji": "📚", "price": 149,   "original_price": 299,   "discount": 50, "rating": 4.4, "reviews": 23421},

    # ── TOYS ────────────────────────────────────────────────────────────────
    {"name": "Hot Wheels 20 Car Gift Pack",             "asin": "B07FJHML2G",  "category": "Toys",         "emoji": "🧸", "price": 699,   "original_price": 1999,  "discount": 65, "rating": 4.4, "reviews": 34521},
    {"name": "Funskool Monopoly Board Game",            "asin": "B000NLVFR6",  "category": "Toys",         "emoji": "🎲", "price": 499,   "original_price": 1299,  "discount": 62, "rating": 4.3, "reviews": 23421},
    {"name": "LEGO Creator 3in1 Space Shuttle 144pcs",  "asin": "B08CW3WRBH",  "category": "Toys",         "emoji": "🚀", "price": 799,   "original_price": 1999,  "discount": 60, "rating": 4.5, "reviews": 8921},
    {"name": "Hasbro Jenga Classic Game",               "asin": "B00005JG7O",  "category": "Toys",         "emoji": "🎲", "price": 399,   "original_price": 999,   "discount": 60, "rating": 4.4, "reviews": 19231},
    {"name": "NHR Carrom Board Medium Size 3.5mm",      "asin": "B073CM7MHV",  "category": "Toys",         "emoji": "🎯", "price": 699,   "original_price": 1999,  "discount": 65, "rating": 4.1, "reviews": 12341},
    {"name": "Negi Happy Bird Badminton Set",           "asin": "B075Z27G3G",  "category": "Toys",         "emoji": "🏸", "price": 299,   "original_price": 799,   "discount": 63, "rating": 4.0, "reviews": 23421},
    {"name": "Skillmatics Card Game Guess in 10",       "asin": "B07QZX6CVF",  "category": "Toys",         "emoji": "🃏", "price": 349,   "original_price": 799,   "discount": 56, "rating": 4.5, "reviews": 14231},
    {"name": "Play & Learn Talking Globe for Kids",     "asin": "B07BQXFYCV",  "category": "Toys",         "emoji": "🌍", "price": 499,   "original_price": 1499,  "discount": 67, "rating": 4.1, "reviews": 8921},
    {"name": "OK Play Junior Bricks Building Set",      "asin": "B073W2BRKM",  "category": "Toys",         "emoji": "🧱", "price": 299,   "original_price": 899,   "discount": 67, "rating": 4.0, "reviews": 5432},
    {"name": "IQ Toys Magnetic Drawing Board for Kids", "asin": "B07YRHRQ2G",  "category": "Toys",         "emoji": "🎨", "price": 349,   "original_price": 999,   "discount": 65, "rating": 4.2, "reviews": 7823},
    {"name": "Funskool Scrabble Original Word Game",    "asin": "B00BVZL91W",  "category": "Toys",         "emoji": "🔤", "price": 449,   "original_price": 1299,  "discount": 65, "rating": 4.4, "reviews": 12341},
    {"name": "Remote Control Car for Kids Off Road",    "asin": "B0BBQGD8WX",  "category": "Toys",         "emoji": "🚗", "price": 799,   "original_price": 2499,  "discount": 68, "rating": 4.0, "reviews": 9823},

    # ── HOME ────────────────────────────────────────────────────────────────
    {"name": "Story@Home 5m LED Strip Lights",          "asin": "B08PPNVWFF",  "category": "Home",         "emoji": "💡", "price": 299,   "original_price": 999,   "discount": 70, "rating": 4.1, "reviews": 34521},
    {"name": "Amazon Basics Microfiber Cleaning Cloths","asin": "B009FUF6DM",  "category": "Home",         "emoji": "🧹", "price": 299,   "original_price": 699,   "discount": 57, "rating": 4.4, "reviews": 45231},
    {"name": "Solimo Printed Microfibre Double Bedsheet","asin":"B07BGPQRCK",  "category": "Home",         "emoji": "🛏️", "price": 499,   "original_price": 1299,  "discount": 62, "rating": 4.1, "reviews": 23421},
    {"name": "Philips Avent Ultra Soft Pacifier",       "asin": "B00IYGLQCI",  "category": "Home",         "emoji": "🏠", "price": 349,   "original_price": 895,   "discount": 61, "rating": 4.3, "reviews": 18234},
    {"name": "Lifelong LLVAC80 900W Vacuum Cleaner",    "asin": "B07JL6QMKQ",  "category": "Home",         "emoji": "🧹", "price": 1499,  "original_price": 3999,  "discount": 63, "rating": 4.0, "reviews": 19231},
    {"name": "Polycab Optima Deco 1200MM Ceiling Fan",  "asin": "B09B1DG8W6",  "category": "Home",         "emoji": "💨", "price": 1299,  "original_price": 2999,  "discount": 57, "rating": 4.2, "reviews": 12341},
    {"name": "Solimo Velvet Touch 3 Piece Towel Set",   "asin": "B07HPVHBCB",  "category": "Home",         "emoji": "🛁", "price": 399,   "original_price": 999,   "discount": 60, "rating": 4.2, "reviews": 23421},
    {"name": "Syska Rechargeable LED Emergency Light",  "asin": "B01HDKC0RS",  "category": "Home",         "emoji": "💡", "price": 349,   "original_price": 995,   "discount": 65, "rating": 4.1, "reviews": 34521},
    {"name": "Pigeon Healthifry Digital Air Fryer 4.2L","asin": "B08JJRR6GD",  "category": "Home",         "emoji": "🍟", "price": 3999,  "original_price": 9999,  "discount": 60, "rating": 4.3, "reviews": 8921},
    {"name": "Crompton BreezGold 1200MM Ceiling Fan",   "asin": "B09FXZZ2D4",  "category": "Home",         "emoji": "💨", "price": 1499,  "original_price": 3499,  "discount": 57, "rating": 4.3, "reviews": 7823},
    {"name": "NatureHike Ultralight Camping Tent 2P",   "asin": "B07RXY54RJ",  "category": "Home",         "emoji": "⛺", "price": 2999,  "original_price": 7999,  "discount": 63, "rating": 4.2, "reviews": 4321},
    {"name": "Amazon Brand Hanging Clothes Organizer",  "asin": "B07GY6FY3Z",  "category": "Home",         "emoji": "👔", "price": 299,   "original_price": 799,   "discount": 63, "rating": 4.0, "reviews": 12341},
    {"name": "Prestige Iris 750W Hand Blender",         "asin": "B07SZT4LKC",  "category": "Home",         "emoji": "🏠", "price": 799,   "original_price": 1995,  "discount": 60, "rating": 4.2, "reviews": 9823},
    {"name": "Strauss Yoga Mat Anti Skid 6mm",          "asin": "B06XHBXXDR",  "category": "Home",         "emoji": "🧘", "price": 499,   "original_price": 1499,  "discount": 67, "rating": 4.1, "reviews": 34521},

    # ── SPORTS ──────────────────────────────────────────────────────────────
    {"name": "Cosco Lad 35 Badminton Kit Combo",        "asin": "B004ZJLFMM",  "category": "Sports",       "emoji": "🏸", "price": 599,   "original_price": 1799,  "discount": 67, "rating": 4.1, "reviews": 23421},
    {"name": "Nivia Football Storm Plus",               "asin": "B00SQJKK8I",  "category": "Sports",       "emoji": "⚽", "price": 399,   "original_price": 1199,  "discount": 67, "rating": 4.0, "reviews": 19231},
    {"name": "Amazon Basics Neoprene Dumbbell Pair 2kg","asin": "B00HJQCQAG",  "category": "Sports",       "emoji": "🏋️", "price": 399,   "original_price": 999,   "discount": 60, "rating": 4.3, "reviews": 34521},
    {"name": "Cosco Cricket Tennis Balls (Pack of 6)",  "asin": "B00OM38C7W",  "category": "Sports",       "emoji": "🏏", "price": 199,   "original_price": 599,   "discount": 67, "rating": 4.1, "reviews": 12341},
    {"name": "Strauss Aerobics Stepper",                "asin": "B01HDVNHRS",  "category": "Sports",       "emoji": "🏃", "price": 799,   "original_price": 2499,  "discount": 68, "rating": 4.0, "reviews": 8921},
    {"name": "Boldfit Gym Gloves for Workout",          "asin": "B08XGPCBCP",  "category": "Sports",       "emoji": "🥊", "price": 299,   "original_price": 999,   "discount": 70, "rating": 4.1, "reviews": 14231},
    {"name": "Aurion by 10 Sports Cricket Kit Bag",     "asin": "B07XHQS2C2",  "category": "Sports",       "emoji": "🏏", "price": 799,   "original_price": 2499,  "discount": 68, "rating": 4.0, "reviews": 7823},
    {"name": "Cockatoo CTM-06 Multi-Gym Home Gym",      "asin": "B07BWKPZ3P",  "category": "Sports",       "emoji": "🏋️", "price": 4999,  "original_price": 14999, "discount": 67, "rating": 4.1, "reviews": 4321},
    {"name": "Li-Ning Smash XP 80 Badminton Racket",   "asin": "B07PRF65TM",  "category": "Sports",       "emoji": "🏸", "price": 499,   "original_price": 1499,  "discount": 67, "rating": 4.2, "reviews": 9823},
    {"name": "Strauss Resistance Bands Set of 5",       "asin": "B07H3HSFXY",  "category": "Sports",       "emoji": "🏃", "price": 299,   "original_price": 999,   "discount": 70, "rating": 4.2, "reviews": 23421},
    {"name": "SG Cricket Bat Scorer Poplar Willow",     "asin": "B07BKKMY43",  "category": "Sports",       "emoji": "🏏", "price": 699,   "original_price": 1999,  "discount": 65, "rating": 4.0, "reviews": 5432},
    {"name": "Proline Foldable Walking Treadmill",      "asin": "B08QKC2FS8",  "category": "Sports",       "emoji": "🏃", "price": 12999, "original_price": 29999, "discount": 57, "rating": 4.1, "reviews": 3412},

    # ── HEALTH ──────────────────────────────────────────────────────────────
    {"name": "Patanjali Ashwagandha Capsule 60ct",      "asin": "B01N4HVSQB",  "category": "Health",       "emoji": "💊", "price": 199,   "original_price": 499,   "discount": 60, "rating": 4.2, "reviews": 23421},
    {"name": "Dr. Morepen Blood Pressure Monitor",      "asin": "B079DPY57T",  "category": "Health",       "emoji": "🩺", "price": 1099,  "original_price": 2999,  "discount": 63, "rating": 4.2, "reviews": 34521},
    {"name": "HealthSense Soft-Touch Digital Thermometer","asin":"B07TXFJ5ZV","category": "Health",        "emoji": "🌡️", "price": 299,   "original_price": 799,   "discount": 63, "rating": 4.3, "reviews": 23421},
    {"name": "Omron HEM-7120 BP Monitor Automatic",     "asin": "B004GFUIXS",  "category": "Health",       "emoji": "🩺", "price": 1299,  "original_price": 3500,  "discount": 63, "rating": 4.4, "reviews": 45231},
    {"name": "Boldfit Protein Shaker Bottle 700ml",     "asin": "B08SWS4MFP",  "category": "Health",       "emoji": "🥤", "price": 199,   "original_price": 699,   "discount": 71, "rating": 4.2, "reviews": 19231},
    {"name": "OneLife Glucometer with 25 Test Strips",  "asin": "B08XYMJXHG",  "category": "Health",       "emoji": "💊", "price": 499,   "original_price": 1499,  "discount": 67, "rating": 4.1, "reviews": 12341},
    {"name": "Himalaya Diabecon DS Tablets 60ct",       "asin": "B00BFWF83O",  "category": "Health",       "emoji": "💊", "price": 149,   "original_price": 399,   "discount": 63, "rating": 4.1, "reviews": 8921},
    {"name": "HealthSense Ultra-Lite Weight Machine",   "asin": "B08BZDPMPX",  "category": "Health",       "emoji": "⚖️", "price": 899,   "original_price": 2499,  "discount": 64, "rating": 4.2, "reviews": 14231},
    {"name": "Saffola FITTIFY Protein Bar Mixed Fruit", "asin": "B09JYB5XCH",  "category": "Health",       "emoji": "🥗", "price": 399,   "original_price": 999,   "discount": 60, "rating": 4.1, "reviews": 7823},
    {"name": "HealthKart HK Vitals Multivitamin 60ct",  "asin": "B09NWL2DGZ",  "category": "Health",       "emoji": "💊", "price": 349,   "original_price": 999,   "discount": 65, "rating": 4.3, "reviews": 23421},
]


def scrape_products():
    """Try scraping from Amazon (blocked in CI but works locally)"""
    if not BS4_AVAILABLE:
        return []
    products = []
    for category in CATEGORIES:
        try:
            headers = random.choice(HEADERS_LIST)
            resp = requests.get(category["url"], headers=headers, timeout=10)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.select(".zg-grid-general-faceout")[:5]
            for card in cards:
                name_el = card.select_one(".p13n-sc-truncate-desktop-type2, .p13n-sc-truncated")
                price_el = card.select_one(".p13n-sc-price")
                link_el  = card.select_one("a.a-link-normal")
                if not name_el or not link_el:
                    continue
                name = name_el.get_text(strip=True)
                asin_match = re.search(r"/dp/([A-Z0-9]{10})", link_el.get("href",""))
                if not asin_match:
                    continue
                asin = asin_match.group(1)
                price_text = price_el.get_text(strip=True) if price_el else "₹1000"
                price = int(re.sub(r"[^\d]", "", price_text) or 1000)
                original_price = int(price * random.uniform(1.2, 1.6))
                discount = int(((original_price - price) / original_price) * 100)
                products.append({
                    "name": name,
                    "asin": asin,
                    "category": category["name"],
                    "emoji": category["emoji"],
                    "price": price,
                    "original_price": original_price,
                    "discount": discount,
                    "rating": round(random.uniform(3.8, 4.7), 1),
                    "reviews": random.randint(500, 50000),
                })
        except Exception:
            continue
    return products


def load_json_products():
    """Load from local products.json cache"""
    if not os.path.exists(PRODUCTS_JSON):
        return []
    try:
        with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def generate_stars(rating):
    full = int(rating)
    half = 1 if (rating - full) >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + ("½" if half else "") + "☆" * empty


def build_jsonld(products):
    """Build JSON-LD schema — called outside f-string to avoid brace conflicts."""
    items = []
    for i, p in enumerate(products[:20], 1):
        aff_url = f"https://www.amazon.in/dp/{p['asin']}?tag={AFFILIATE_TAG}"
        items.append({
            "@type": "ListItem",
            "position": i,
            "item": {
                "@type": "Product",
                "name": p["name"],
                "url": aff_url,
                "offers": {
                    "@type": "Offer",
                    "priceCurrency": "INR",
                    "price": str(p["price"]),
                    "availability": "https://schema.org/InStock",
                    "url": aff_url
                },
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": str(p.get("rating", 4.0)),
                    "reviewCount": str(p.get("reviews", 500))
                }
            }
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Best Amazon India Deals Today",
        "description": "Top discounted products on Amazon India — updated daily",
        "url": SITE_URL,
        "numberOfItems": len(products),
        "itemListElement": items
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def generate_html(products):
    today = datetime.now().strftime("%d %B %Y")
    now_time = datetime.now().strftime("%I:%M %p")
    total = len(products)

    # Build category list
    cats = sorted(set(p["category"] for p in products))

    # Build JS product array for autocomplete
    js_products = json.dumps([{
        "name": p["name"],
        "category": p["category"],
        "price": p["price"],
        "discount": p["discount"],
        "asin": p["asin"],
        "emoji": p.get("emoji", "🛍️")
    } for p in products], ensure_ascii=False)

    # Build product cards HTML
    cards_html = ""
    for p in products:
        asin     = p["asin"]
        name     = p["name"]
        cat      = p["category"]
        emoji    = p.get("emoji", "🛍️")
        price    = p["price"]
        orig     = p.get("original_price", int(price * 1.3))
        disc     = p.get("discount", int((orig - price) / orig * 100))
        rating   = p.get("rating", 4.0)
        reviews  = p.get("reviews", random.randint(500, 50000))
        bought   = random.randint(20, 300)
        stars    = generate_stars(rating)
        savings  = orig - price
        aff_url  = f"https://www.amazon.in/dp/{asin}?tag={AFFILIATE_TAG}"
        wa_text  = f"🔥 {disc}% OFF! {name} ₹{price:,} (was ₹{orig:,}) - Save ₹{savings:,}! Buy: {aff_url}"

        cards_html += f"""
<div class="card" data-category="{cat}" data-price="{price}" data-discount="{disc}" data-name="{name.lower()}" data-rating="{rating}" data-reviews="{reviews}">
  <div class="badge-wrap">
    <span class="badge-disc">{disc}% OFF</span>
    {f'<span class="badge-hot">🔥 HOT</span>' if disc >= 60 else ''}
  </div>
  <div class="card-emoji">{emoji}</div>
  <div class="card-cat">{cat}</div>
  <div class="card-name">{name}</div>
  <div class="card-rating">{stars} <span class="rev-count">({reviews:,})</span></div>
  <div class="price-row">
    <span class="price-now">₹{price:,}</span>
    <span class="price-orig">₹{orig:,}</span>
  </div>
  <div class="savings">You save ₹{savings:,}</div>
  <div class="bought-today">🔥 {bought} bought today</div>
  <div class="cta-row">
    <a href="{aff_url}" target="_blank" class="btn-buy" onclick="trackClick('{asin}','{name.replace(chr(39),'')}',{price},'{cat}',{disc})">Buy on Amazon</a>
    <button class="btn-wa" onclick="shareWA('{aff_url}','{name.replace(chr(39),'')}','{price}','{disc}')" title="Share on WhatsApp">📲</button>
    <button class="btn-wish" onclick="toggleWish(this,'{asin}','{name.replace(chr(39),'')}','{price}','{disc}','{emoji}')" title="Add to Wishlist">🤍</button>
  </div>
</div>"""

    # Build category buttons
    cat_btns = '<button class="cat-btn active" data-cat="All" onclick="filterCat(this)">🛍️ All</button>\n'
    cat_emojis = {"Electronics":"📱","Laptops":"💻","Kitchen":"🍳","Beauty":"💄","Fashion":"👕","Books":"📚","Toys":"🧸","Home":"🏠","Sports":"⚽","Health":"💊"}
    for c in cats:
        em = cat_emojis.get(c, "📦")
        cat_btns += f'<button class="cat-btn" data-cat="{c}" onclick="filterCat(this)">{em} {c}</button>\n'

    # Top deal for OG image preview
    top = products[0] if products else {"name": "Amazon Deals", "price": 0, "discount": 0}
    og_title = f"🔥 {top['discount']}% OFF on {top['name']} | Deal Bazaar India"
    og_desc  = f"Best Amazon India deals — {len(products)} products, up to 80% OFF. Electronics, Laptops, Kitchen, Fashion & more!"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Deal Bazaar India 🛍️ - Best Amazon Deals Today | Up to 80% OFF</title>
<meta name="description" content="Best Amazon India deals today — {len(products)} products with up to 80% discount. Electronics, Laptops, Kitchen, Fashion, Beauty & more. Updated daily!">
<meta name="keywords" content="amazon deals india, amazon sale today, best amazon offers, electronics deals india, mobile deals india, laptop deals india, amazon discount">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{SITE_URL}/">
<!-- Open Graph -->
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="{SITE_URL}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Deal Bazaar India">
<meta property="og:locale" content="en_IN">
<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{og_desc}">
<!-- JSON-LD Schema -->
<script type="application/ld+json">
JSONLD_PLACEHOLDER
</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#0f0f1a;--card:#1a1a2e;--card2:#16213e;--accent:#e94560;
  --gold:#ffd700;--green:#00d4aa;--text:#e0e0e0;--muted:#8892a4;
  --radius:16px;--shadow:0 8px 32px rgba(0,0,0,.5);
}}
body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh}}

/* HEADER */
header{{background:linear-gradient(135deg,#1a1a3e,#0d0d1f);padding:20px;text-align:center;border-bottom:2px solid var(--accent);position:sticky;top:0;z-index:100;backdrop-filter:blur(10px)}}
.logo{{font-size:1.8rem;font-weight:800;color:#fff}}
.logo span{{color:var(--accent)}}
.tagline{{color:var(--muted);font-size:.85rem;margin-top:4px}}
.header-meta{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:8px;font-size:.8rem;color:var(--muted)}}
.header-meta span{{background:rgba(255,255,255,.07);padding:3px 10px;border-radius:20px}}

/* SEARCH */
.search-section{{padding:20px;background:rgba(255,255,255,.03);border-bottom:1px solid rgba(255,255,255,.08)}}
.search-wrap{{max-width:700px;margin:0 auto;position:relative}}
.search-box{{width:100%;padding:14px 52px 14px 20px;font-size:1rem;border:2px solid rgba(233,69,96,.5);border-radius:30px;background:rgba(255,255,255,.07);color:var(--text);outline:none;transition:all .3s}}
.search-box:focus{{border-color:var(--accent);background:rgba(255,255,255,.1);box-shadow:0 0 20px rgba(233,69,96,.3)}}
.search-box::placeholder{{color:var(--muted)}}
.search-icon{{position:absolute;right:18px;top:50%;transform:translateY(-50%);font-size:1.2rem;pointer-events:none}}
.autocomplete-list{{position:absolute;top:calc(100% + 6px);left:0;right:0;background:#1e2040;border:1px solid rgba(233,69,96,.4);border-radius:12px;z-index:999;max-height:280px;overflow-y:auto;display:none;box-shadow:var(--shadow)}}
.ac-item{{padding:10px 16px;cursor:pointer;display:flex;align-items:center;gap:10px;font-size:.9rem;transition:background .2s}}
.ac-item:hover,.ac-item.ac-active{{background:rgba(233,69,96,.15)}}
.ac-item .ac-emoji{{font-size:1.2rem}}
.ac-item .ac-info{{flex:1}}
.ac-item .ac-cat{{font-size:.75rem;color:var(--muted)}}
.ac-item .ac-price{{color:var(--green);font-weight:700;font-size:.85rem}}
.search-tags{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px;justify-content:center}}
.stag{{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.15);color:var(--text);padding:5px 14px;border-radius:20px;font-size:.8rem;cursor:pointer;transition:all .2s;white-space:nowrap}}
.stag:hover,.stag.active{{background:var(--accent);border-color:var(--accent);color:#fff}}

/* CONTROLS */
.controls{{padding:16px 20px;background:rgba(255,255,255,.02);border-bottom:1px solid rgba(255,255,255,.06)}}
.controls-inner{{max-width:1400px;margin:0 auto;display:flex;gap:10px;flex-wrap:wrap;align-items:center}}
.sort-select,.price-select{{background:rgba(255,255,255,.08);color:var(--text);border:1px solid rgba(255,255,255,.15);border-radius:8px;padding:7px 12px;font-size:.85rem;cursor:pointer;outline:none}}
.sort-select:focus,.price-select:focus{{border-color:var(--accent)}}
.result-count{{color:var(--muted);font-size:.85rem;margin-left:auto}}

/* CATEGORIES */
.cat-bar{{padding:12px 20px;overflow-x:auto;white-space:nowrap;border-bottom:1px solid rgba(255,255,255,.06)}}
.cat-bar::-webkit-scrollbar{{height:3px}}
.cat-bar::-webkit-scrollbar-thumb{{background:var(--accent);border-radius:3px}}
.cat-btn{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);color:var(--text);padding:7px 16px;border-radius:20px;cursor:pointer;font-size:.85rem;margin-right:8px;transition:all .2s;white-space:nowrap}}
.cat-btn:hover,.cat-btn.active{{background:var(--accent);border-color:var(--accent);color:#fff}}

/* GRID */
.main{{max-width:1400px;margin:0 auto;padding:20px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:18px}}

/* CARDS */
.card{{background:var(--card);border-radius:var(--radius);padding:18px;border:1px solid rgba(255,255,255,.08);transition:all .3s;position:relative;display:flex;flex-direction:column;gap:8px}}
.card:hover{{transform:translateY(-4px);box-shadow:0 12px 40px rgba(233,69,96,.2);border-color:rgba(233,69,96,.3)}}
.badge-wrap{{display:flex;gap:6px;flex-wrap:wrap}}
.badge-disc{{background:var(--accent);color:#fff;font-size:.72rem;font-weight:700;padding:3px 8px;border-radius:6px}}
.badge-hot{{background:var(--gold);color:#111;font-size:.72rem;font-weight:700;padding:3px 8px;border-radius:6px}}
.card-emoji{{font-size:2.2rem;text-align:center;margin:4px 0}}
.card-cat{{font-size:.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:.5px}}
.card-name{{font-size:.9rem;font-weight:600;color:var(--text);line-height:1.4;min-height:2.8rem}}
.card-rating{{font-size:.82rem;color:var(--gold)}}
.rev-count{{color:var(--muted)}}
.price-row{{display:flex;align-items:baseline;gap:8px}}
.price-now{{font-size:1.3rem;font-weight:800;color:var(--green)}}
.price-orig{{font-size:.85rem;text-decoration:line-through;color:var(--muted)}}
.savings{{font-size:.78rem;color:#4ade80;font-weight:600}}
.bought-today{{font-size:.75rem;color:#f97316}}
.cta-row{{display:flex;gap:6px;margin-top:auto}}
.btn-buy{{flex:1;background:linear-gradient(135deg,var(--accent),#c0392b);color:#fff;border:none;padding:9px;border-radius:10px;font-size:.82rem;font-weight:700;cursor:pointer;text-decoration:none;text-align:center;transition:all .2s}}
.btn-buy:hover{{opacity:.9;transform:scale(1.02)}}
.btn-wa{{background:rgba(37,211,102,.15);color:#25d366;border:1px solid rgba(37,211,102,.3);padding:9px 11px;border-radius:10px;cursor:pointer;font-size:.9rem;transition:all .2s}}
.btn-wa:hover{{background:rgba(37,211,102,.3)}}
.btn-wish{{background:rgba(233,69,96,.1);color:var(--accent);border:1px solid rgba(233,69,96,.2);padding:9px 11px;border-radius:10px;cursor:pointer;font-size:.9rem;transition:all .2s}}
.btn-wish:hover{{background:rgba(233,69,96,.25)}}
.btn-wish.wished{{color:#ff4560;background:rgba(233,69,96,.25)}}

/* NO RESULTS */
#no-results{{display:none;text-align:center;padding:60px 20px;color:var(--muted)}}
#no-results h2{{font-size:1.5rem;margin-bottom:10px;color:var(--text)}}
.suggest-tags{{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:16px}}
.suggest-tag{{background:rgba(233,69,96,.15);color:var(--accent);border:1px solid rgba(233,69,96,.3);padding:6px 16px;border-radius:20px;cursor:pointer;font-size:.85rem;transition:all .2s}}
.suggest-tag:hover{{background:var(--accent);color:#fff}}

/* WISHLIST FAB */
#wish-fab{{position:fixed;bottom:80px;right:20px;width:52px;height:52px;background:linear-gradient(135deg,var(--accent),#c0392b);border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 4px 20px rgba(233,69,96,.5);z-index:200;font-size:1.4rem;transition:all .3s}}
#wish-fab:hover{{transform:scale(1.1)}}
#wish-badge{{position:absolute;top:-4px;right:-4px;background:var(--gold);color:#111;font-size:.65rem;font-weight:700;width:18px;height:18px;border-radius:50%;display:none;align-items:center;justify-content:center}}
#wish-panel{{position:fixed;top:0;right:-340px;width:320px;height:100vh;background:#1a1a2e;border-left:1px solid rgba(233,69,96,.3);z-index:300;transition:right .3s;overflow-y:auto;padding:20px}}
#wish-panel.open{{right:0}}
.wish-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}}
.wish-header h3{{font-size:1.1rem;color:var(--text)}}
#wish-close{{background:none;border:none;color:var(--muted);font-size:1.5rem;cursor:pointer}}
.wish-item{{background:rgba(255,255,255,.05);border-radius:10px;padding:12px;margin-bottom:10px;display:flex;gap:10px;align-items:center}}
.wish-item-info{{flex:1;font-size:.82rem}}
.wish-item-name{{font-weight:600;margin-bottom:4px}}
.wish-item-price{{color:var(--green)}}
.wish-item-rm{{background:none;border:none;color:var(--accent);cursor:pointer;font-size:.75rem;padding:3px 8px;border:1px solid rgba(233,69,96,.3);border-radius:6px}}
#wish-empty{{text-align:center;color:var(--muted);padding:40px 0}}

/* BACK TO TOP */
#back-top{{position:fixed;bottom:20px;right:20px;width:44px;height:44px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);border-radius:50%;display:none;align-items:center;justify-content:center;cursor:pointer;font-size:1.1rem;z-index:200;transition:all .3s}}
#back-top:hover{{background:var(--accent);border-color:var(--accent)}}
#back-top.visible{{display:flex}}

/* TICKER */
.ticker-wrap{{background:rgba(233,69,96,.1);border-top:1px solid rgba(233,69,96,.3);border-bottom:1px solid rgba(233,69,96,.3);overflow:hidden;padding:8px 0}}
.ticker{{white-space:nowrap;animation:ticker 30s linear infinite;display:inline-block}}
.ticker span{{margin:0 30px;font-size:.82rem;color:var(--gold)}}
@keyframes ticker{{0%{{transform:translateX(100vw)}}100%{{transform:translateX(-100%)}}}}

/* FOOTER */
footer{{text-align:center;padding:24px;background:rgba(0,0,0,.3);color:var(--muted);font-size:.82rem;border-top:1px solid rgba(255,255,255,.07);margin-top:30px}}
footer a{{color:var(--accent);text-decoration:none}}

/* OVERLAY */
#wish-overlay{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:250}}
#wish-overlay.show{{display:block}}

/* RESPONSIVE */
@media(max-width:600px){{
  .logo{{font-size:1.4rem}}
  .grid{{grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}}
  .card{{padding:12px}}
  .card-name{{font-size:.82rem}}
  .price-now{{font-size:1.1rem}}
}}
</style>
</head>
<body>

<header>
  <div class="logo">Deal<span>Bazaar</span> India 🛍️</div>
  <div class="tagline">Sab kuch yahan milega — Best Amazon Deals, Curated Daily!</div>
  <div class="header-meta">
    <span>📅 {today}</span>
    <span>🕐 {now_time}</span>
    <span>🛒 {total} Deals Live</span>
    <span>💰 Up to 83% OFF</span>
    <a href="{TELEGRAM_CHANNEL}" target="_blank" style="color:#00d4aa;text-decoration:none;background:rgba(0,212,170,.1);padding:3px 10px;border-radius:20px;font-size:.8rem">📣 Telegram Channel</a>
  </div>
</header>

<div class="ticker-wrap">
  <div class="ticker">
    <span>🔥 boAt Earbuds 77% OFF!</span>
    <span>⚡ Pressure Cooker 50% OFF!</span>
    <span>💥 Smartwatch Under ₹1299!</span>
    <span>🎯 Laptop from ₹27,990!</span>
    <span>👟 Shoes Under ₹1000!</span>
    <span>📚 Atomic Habits ₹299!</span>
    <span>🏋️ Dumbbells 60% OFF!</span>
    <span>💄 Beauty Products 50%+ OFF!</span>
    <span>🍳 Kitchen Must-Haves Under ₹599!</span>
    <span>🎮 Gaming Laptops 30% OFF!</span>
  </div>
</div>

<div class="search-section">
  <div class="search-wrap">
    <input type="text" id="searchBox" class="search-box" placeholder="Search karo — earbuds, laptop under 35000, 70% off..." oninput="onSearch()" onkeydown="onSearchKey(event)" autocomplete="off">
    <span class="search-icon">🔍</span>
    <div class="autocomplete-list" id="acList"></div>
  </div>
  <div class="search-tags">
    <button class="stag" onclick="quickSearch('under 500')">💰 Under ₹500</button>
    <button class="stag" onclick="quickSearch('under 1000')">🛒 Under ₹1000</button>
    <button class="stag" onclick="quickSearch('under 2000')">🎯 Under ₹2000</button>
    <button class="stag" onclick="quickSearch('earbuds')">🎧 Earbuds</button>
    <button class="stag" onclick="quickSearch('smartwatch')">⌚ Smartwatch</button>
    <button class="stag" onclick="quickSearch('laptop')">💻 Laptop</button>
    <button class="stag" onclick="quickSearch('70% off')">🔥 70%+ OFF</button>
    <button class="stag" onclick="quickSearch('mobile')">📱 Mobiles</button>
    <button class="stag" onclick="quickSearch('cricket')">🏏 Cricket</button>
    <button class="stag" onclick="quickSearch('books')">📚 Books</button>
    <button class="stag" onclick="quickSearch('kitchen')">🍳 Kitchen</button>
    <button class="stag" onclick="quickSearch('beauty')">💄 Beauty</button>
  </div>
</div>

<div class="cat-bar">
  {cat_btns}
</div>

<div class="controls">
  <div class="controls-inner">
    <select class="sort-select" id="sortSel" onchange="applyFilters()">
      <option value="discount">🔥 Best Discount First</option>
      <option value="price_asc">💰 Price: Low to High</option>
      <option value="price_desc">💎 Price: High to Low</option>
      <option value="rating">⭐ Highest Rated</option>
      <option value="popular">👥 Most Popular</option>
    </select>
    <select class="price-select" id="priceSel" onchange="applyFilters()">
      <option value="">💲 All Prices</option>
      <option value="500">Under ₹500</option>
      <option value="1000">Under ₹1,000</option>
      <option value="2000">Under ₹2,000</option>
      <option value="5000">Under ₹5,000</option>
      <option value="10000">Under ₹10,000</option>
      <option value="25000">Under ₹25,000</option>
    </select>
    <span class="result-count" id="resultCount">Showing {total} deals</span>
  </div>
</div>

<main class="main">
  <div class="grid" id="dealsGrid">
    {cards_html}
  </div>
  <div id="no-results">
    <div style="font-size:3rem">🔍</div>
    <h2>Koi deal nahi mili!</h2>
    <p>Kuch aur search karo ya filter change karo</p>
    <div class="suggest-tags">
      <button class="suggest-tag" onclick="quickSearch('earbuds')">🎧 Earbuds</button>
      <button class="suggest-tag" onclick="quickSearch('mobile')">📱 Mobiles</button>
      <button class="suggest-tag" onclick="quickSearch('laptop')">💻 Laptops</button>
      <button class="suggest-tag" onclick="quickSearch('under 1000')">💰 Under ₹1000</button>
      <button class="suggest-tag" onclick="clearAll()">❌ Clear Filters</button>
    </div>
  </div>
</main>

<!-- WISHLIST -->
<div id="wish-overlay" onclick="closeWish()"></div>
<div id="wish-fab" onclick="openWish()" title="My Wishlist">❤️<div id="wish-badge"></div></div>
<div id="wish-panel">
  <div class="wish-header">
    <h3>❤️ My Wishlist</h3>
    <button id="wish-close" onclick="closeWish()">✕</button>
  </div>
  <div id="wish-list"><div id="wish-empty">💔 Wishlist empty hai!<br><small>Deals me ❤️ press karo</small></div></div>
</div>

<!-- BACK TO TOP -->
<div id="back-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">⬆️</div>

<footer>
  <p>🛒 <strong>Deal Bazaar India</strong> — Best Deals, Daily Updated</p>
  <p style="margin-top:6px">Amazon Affiliate Partner | <a href="{TELEGRAM_CHANNEL}" target="_blank">📣 Join Telegram</a></p>
  <p style="margin-top:6px;font-size:.75rem">Prices accurate as of {today}. Amazon affiliate links — we earn commission at no extra cost to you.</p>
</footer>

<script>
// ── ALL PRODUCTS DATA ─────────────────────────────────────────────────────
const ALL_PRODUCTS = {js_products};

// ── STATE ─────────────────────────────────────────────────────────────────
let currentCat = 'All';
let currentSearch = '';
let acIndex = -1;
let wishlist = JSON.parse(localStorage.getItem('dealwishlist') || '[]');

// ── PARSE QUERY ───────────────────────────────────────────────────────────
function parseQuery(q) {{
  q = q.toLowerCase().trim();
  const result = {{ terms: [], maxPrice: null, minDiscount: null, category: null }};

  // price range: "under 500", "500 se kam", "below 1000"
  let pm = q.match(/(?:under|below|less than|se kam|ke andar)\s*[₹]?\s*(\d+)/i)
         || q.match(/[₹]?\s*(\d+)\s*(?:se kam|ke under|ke andar|se niche)/i);
  if (pm) {{ result.maxPrice = parseInt(pm[1]); q = q.replace(pm[0], '').trim(); }}

  // discount: "70% off", "50 percent off"
  let dm = q.match(/(\d+)\s*%?\s*(?:off|discount|छूट)/i);
  if (dm) {{ result.minDiscount = parseInt(dm[1]); q = q.replace(dm[0], '').trim(); }}

  // keyword → category
  const catMap = {{
    'mobile|phone|smartphone|5g': 'Electronics',
    'laptop|computer|notebook': 'Laptops',
    'kitchen|cooker|mixer|grinder|kettle|blender': 'Kitchen',
    'beauty|makeup|skincare|haircare|lipstick|moisturizer': 'Beauty',
    'fashion|shirt|jeans|shoes|kurta|dress|bag|watch': 'Fashion',
    'book|novel|self help|motivational': 'Books',
    'toy|game|kid|child|lego|board game': 'Toys',
    'home|fan|light|curtain|bedsheet|sofa|vacuum': 'Home',
    'sport|cricket|badminton|fitness|gym|dumbbell': 'Sports',
    'health|medicine|bp|sugar|protein|vitamin': 'Health',
  }};
  for (const [pat, cat] of Object.entries(catMap)) {{
    if (new RegExp(pat, 'i').test(q)) {{ result.category = cat; break; }}
  }}

  // keyword aliases
  const aliases = {{
    'earphone|headphone|buds|earbud|tws|wireless audio': 'earbuds',
    'smartwatch|watch|band|wristband': 'smartwatch',
    'cooker|pressure cooker': 'pressure cooker',
    'phone|smartphone|mobile': 'mobile',
    'tab|tablet': 'tablet',
  }};
  let term = q;
  for (const [pat, rep] of Object.entries(aliases)) {{
    if (new RegExp(pat, 'i').test(term)) {{ term = rep; break; }}
  }}
  if (term) result.terms = term.split(/\s+/).filter(t => t.length > 1);
  return result;
}}

// ── APPLY FILTERS ─────────────────────────────────────────────────────────
function applyFilters() {{
  const cards = document.querySelectorAll('.card');
  const sort  = document.getElementById('sortSel').value;
  const priceMax = parseInt(document.getElementById('priceSel').value) || Infinity;
  const parsed = parseQuery(currentSearch);

  let visible = [];
  cards.forEach(card => {{
    const cat     = card.dataset.category;
    const price   = parseInt(card.dataset.price);
    const disc    = parseInt(card.dataset.discount);
    const name    = card.dataset.name;
    const rating  = parseFloat(card.dataset.rating);
    const reviews = parseInt(card.dataset.reviews);

    // category filter (sidebar btn)
    if (currentCat !== 'All' && cat !== currentCat) {{ card.style.display='none'; return; }}
    // price dropdown
    if (price > priceMax) {{ card.style.display='none'; return; }}
    // search
    if (currentSearch) {{
      let match = true;
      if (parsed.maxPrice && price > parsed.maxPrice) match = false;
      if (parsed.minDiscount && disc < parsed.minDiscount) match = false;
      if (parsed.category && cat !== parsed.category) match = false;
      if (parsed.terms.length) {{
        const allMatch = parsed.terms.every(t => name.includes(t));
        if (!allMatch) match = false;
      }}
      if (!match) {{ card.style.display='none'; return; }}
    }}
    card.style.display = '';
    visible.push({{ el: card, price, disc, rating, reviews }});
  }});

  // sort
  const grid = document.getElementById('dealsGrid');
  visible.sort((a,b) => {{
    if (sort === 'price_asc')  return a.price - b.price;
    if (sort === 'price_desc') return b.price - a.price;
    if (sort === 'rating')     return b.rating - a.rating;
    if (sort === 'popular')    return b.reviews - a.reviews;
    return b.disc - a.disc; // best discount
  }});
  visible.forEach(v => grid.appendChild(v.el));

  // result count
  const count = visible.length;
  document.getElementById('resultCount').textContent = count + ' deals found';
  document.getElementById('no-results').style.display = count === 0 ? 'block' : 'none';
}}

// ── SEARCH ────────────────────────────────────────────────────────────────
function onSearch() {{
  currentSearch = document.getElementById('searchBox').value;
  showAutocomplete(currentSearch);
  applyFilters();
  // update active stag
  document.querySelectorAll('.stag').forEach(t => t.classList.remove('active'));
}}

function quickSearch(term) {{
  document.getElementById('searchBox').value = term;
  currentSearch = term;
  document.querySelectorAll('.stag').forEach(t => {{
    t.classList.toggle('active', t.textContent.toLowerCase().includes(term.toLowerCase()));
  }});
  closeAutocomplete();
  applyFilters();
  window.scrollTo({{top:300,behavior:'smooth'}});
}}

function clearAll() {{
  document.getElementById('searchBox').value = '';
  currentSearch = '';
  currentCat = 'All';
  document.getElementById('priceSel').value = '';
  document.getElementById('sortSel').value = 'discount';
  document.querySelectorAll('.cat-btn').forEach(b => b.classList.toggle('active', b.dataset.cat === 'All'));
  document.querySelectorAll('.stag').forEach(t => t.classList.remove('active'));
  applyFilters();
}}

// ── AUTOCOMPLETE ──────────────────────────────────────────────────────────
function showAutocomplete(query) {{
  const list = document.getElementById('acList');
  if (!query || query.length < 2) {{ closeAutocomplete(); return; }}
  const q = query.toLowerCase();
  const matches = ALL_PRODUCTS.filter(p =>
    p.name.toLowerCase().includes(q) ||
    p.category.toLowerCase().includes(q)
  ).slice(0, 8);

  // popular searches
  const popular = [
    {{name:'Under ₹500 Deals', cat:'All', price:500, disc:60, emoji:'💰', asin:''}},
    {{name:'Under ₹1000 Deals', cat:'All', price:1000, disc:60, emoji:'🛒', asin:''}},
    {{name:'Earbuds Best Deals', cat:'Electronics', price:999, disc:70, emoji:'🎧', asin:''}},
    {{name:'Smartwatch Deals', cat:'Electronics', price:1299, disc:65, emoji:'⌚', asin:''}},
    {{name:'Laptop Under ₹35000', cat:'Laptops', price:35000, disc:30, emoji:'💻', asin:''}},
  ].filter(p => p.name.toLowerCase().includes(q) || p.cat.toLowerCase().includes(q));

  const combined = [...matches, ...popular].slice(0, 8);
  if (combined.length === 0) {{ closeAutocomplete(); return; }}

  list.innerHTML = combined.map((p, i) => `
    <div class="ac-item" data-i="${{i}}" onclick="selectAC('${{p.name}}','${{p.asin}}')">
      <span class="ac-emoji">${{p.emoji}}</span>
      <div class="ac-info">
        <div>${{p.name}}</div>
        <div class="ac-cat">${{p.category || p.cat}}</div>
      </div>
      <span class="ac-price">₹${{p.price?.toLocaleString('en-IN')}}</span>
    </div>`).join('');
  list.style.display = 'block';
  acIndex = -1;
}}

function selectAC(name, asin) {{
  if (asin) {{
    window.open(`https://www.amazon.in/dp/${{asin}}?tag={AFFILIATE_TAG}`, '_blank');
  }} else {{
    quickSearch(name.replace(/ Deals| Under ₹\d+/g, '').trim().toLowerCase());
  }}
  closeAutocomplete();
}}

function closeAutocomplete() {{
  document.getElementById('acList').style.display = 'none';
  acIndex = -1;
}}

function onSearchKey(e) {{
  const items = document.querySelectorAll('.ac-item');
  if (e.key === 'ArrowDown') {{ acIndex = Math.min(acIndex+1, items.length-1); highlightAC(items); }}
  else if (e.key === 'ArrowUp') {{ acIndex = Math.max(acIndex-1, -1); highlightAC(items); }}
  else if (e.key === 'Enter') {{
    if (acIndex >= 0 && items[acIndex]) items[acIndex].click();
    else {{ closeAutocomplete(); applyFilters(); }}
  }}
  else if (e.key === 'Escape') closeAutocomplete();
}}

function highlightAC(items) {{
  items.forEach((el,i) => el.classList.toggle('ac-active', i === acIndex));
  if (acIndex >= 0 && items[acIndex]) items[acIndex].scrollIntoView({{block:'nearest'}});
}}

document.addEventListener('click', e => {{
  if (!e.target.closest('.search-wrap')) closeAutocomplete();
}});

// ── CATEGORY FILTER ───────────────────────────────────────────────────────
function filterCat(btn) {{
  currentCat = btn.dataset.cat;
  document.querySelectorAll('.cat-btn').forEach(b => b.classList.toggle('active', b === btn));
  applyFilters();
}}

// ── CLICK TRACKER ─────────────────────────────────────────────────────────
// Set TRACKER_URL to your Cloudflare Worker URL to enable click tracking
// Leave empty to disable (site still works perfectly)
const TRACKER_URL = '';  // e.g. 'https://deal-tracker.yourname.workers.dev'

function trackClick(asin, name, price, category, discount) {{
  if (!TRACKER_URL) return;
  try {{
    navigator.sendBeacon(TRACKER_URL + '/track', JSON.stringify({{
      asin, name, price, category, discount
    }}));
  }} catch(e) {{}}  // silent fail — never break buy button
}}

// ── WHATSAPP SHARE ────────────────────────────────────────────────────────
function shareWA(url, name, price, disc) {{
  const text = encodeURIComponent(`🔥 ${{disc}}% OFF! ${{name}}\\n💰 ₹${{parseInt(price).toLocaleString('en-IN')}}\\n🛒 Buy: ${{url}}\\n\\n🔔 More deals: {TELEGRAM_CHANNEL}`);
  window.open(`https://wa.me/?text=${{text}}`, '_blank');
}}

// ── WISHLIST ──────────────────────────────────────────────────────────────
function toggleWish(btn, asin, name, price, disc, emoji) {{
  const idx = wishlist.findIndex(w => w.asin === asin);
  if (idx >= 0) {{
    wishlist.splice(idx, 1);
    btn.classList.remove('wished');
    btn.textContent = '🤍';
  }} else {{
    wishlist.push({{ asin, name, price: parseInt(price), disc: parseInt(disc), emoji }});
    btn.classList.add('wished');
    btn.textContent = '❤️';
  }}
  localStorage.setItem('dealwishlist', JSON.stringify(wishlist));
  updateWishBadge();
  renderWishlist();
}}

function updateWishBadge() {{
  const badge = document.getElementById('wish-badge');
  if (wishlist.length > 0) {{
    badge.style.display = 'flex';
    badge.textContent = wishlist.length;
  }} else {{
    badge.style.display = 'none';
  }}
}}

function renderWishlist() {{
  const list = document.getElementById('wish-list');
  if (wishlist.length === 0) {{
    list.innerHTML = '<div id="wish-empty">💔 Wishlist empty hai!<br><small>Deals me ❤️ press karo</small></div>';
    return;
  }}
  list.innerHTML = wishlist.map((w, i) => `
    <div class="wish-item">
      <span style="font-size:1.5rem">${{w.emoji}}</span>
      <div class="wish-item-info">
        <div class="wish-item-name">${{w.name.substring(0,30)}}...</div>
        <div class="wish-item-price">₹${{w.price.toLocaleString('en-IN')}} <span style="color:#f97316;font-size:.75rem">${{w.disc}}% off</span></div>
      </div>
      <div style="display:flex;flex-direction:column;gap:4px">
        <a href="https://www.amazon.in/dp/${{w.asin}}?tag={AFFILIATE_TAG}" target="_blank" style="font-size:.72rem;color:var(--green);text-decoration:none;border:1px solid rgba(0,212,170,.3);padding:3px 7px;border-radius:6px">Buy</a>
        <button class="wish-item-rm" onclick="removeWish(${{i}})">❌</button>
      </div>
    </div>`).join('');
}}

function removeWish(i) {{
  wishlist.splice(i, 1);
  localStorage.setItem('dealwishlist', JSON.stringify(wishlist));
  updateWishBadge();
  renderWishlist();
  // update card hearts
  initWishButtons();
}}

function openWish()  {{ document.getElementById('wish-panel').classList.add('open'); document.getElementById('wish-overlay').classList.add('show'); renderWishlist(); }}
function closeWish() {{ document.getElementById('wish-panel').classList.remove('open'); document.getElementById('wish-overlay').classList.remove('show'); }}

function initWishButtons() {{
  document.querySelectorAll('.btn-wish').forEach(btn => {{
    const card = btn.closest('.card');
    const asin = btn.getAttribute('onclick').match(/'([A-Z0-9]{{10}})'/)?.[1];
    if (asin && wishlist.find(w => w.asin === asin)) {{
      btn.classList.add('wished');
      btn.textContent = '❤️';
    }} else {{
      btn.classList.remove('wished');
      btn.textContent = '🤍';
    }}
  }});
}}

// ── BACK TO TOP ───────────────────────────────────────────────────────────
window.addEventListener('scroll', () => {{
  document.getElementById('back-top').classList.toggle('visible', window.scrollY > 400);
}});

// ── COUNTDOWNS ───────────────────────────────────────────────────────────
function startCountdowns() {{
  const end = new Date();
  end.setHours(23,59,59,0);
  setInterval(() => {{
    const diff = end - new Date();
    if (diff <= 0) return;
    const h = String(Math.floor(diff/3600000)).padStart(2,'0');
    const m = String(Math.floor((diff%3600000)/60000)).padStart(2,'0');
    const s = String(Math.floor((diff%60000)/1000)).padStart(2,'0');
    document.querySelectorAll('.countdown').forEach(el => {{
      el.textContent = `⏰ Ends in ${{h}}:${{m}}:${{s}}`;
    }});
  }}, 1000);
}}
startCountdowns();

// ── INIT ──────────────────────────────────────────────────────────────────
updateWishBadge();
initWishButtons();
applyFilters();

// Bought today random update
setInterval(() => {{
  document.querySelectorAll('.bought-today').forEach(el => {{
    let n = Math.floor(Math.random()*15) + (parseInt(el.textContent.match(/\d+/)?.[0]) || 50);
    el.textContent = '🔥 ' + n + ' bought today';
  }});
}}, 45000);
</script>
</body>
</html>"""


def generate_sitemap(products):
    """Generate sitemap.xml for Google indexing"""
    today = datetime.now().strftime("%Y-%m-%d")
    urls = [
        f"""  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>"""
    ]
    # Add individual product URLs (Amazon deep links via our site)
    for p in products[:50]:  # top 50 products
        aff_url = f"https://www.amazon.in/dp/{p['asin']}?tag={AFFILIATE_TAG}"
        urls.append(f"""  <url>
    <loc>{aff_url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""
    return sitemap


def generate_robots():
    return f"""User-agent: *
Allow: /
Sitemap: {SITE_URL}/sitemap.xml

# Deal Bazaar India — Best Amazon Deals
# Updated daily by automated system
"""


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 55)
    print("  DEAL BAZAAR INDIA - 10x UPGRADED GENERATOR")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print("=" * 55)

    print("\n[Layer 1] Amazon se live scraping...")
    products = scrape_products()
    source = "Amazon Live"

    if not products:
        print("[Layer 2] products.json se load ho raha hai...")
        products = load_json_products()
        source = "products.json"

    if not products:
        print("[Layer 3] Emergency backup products (158 products)...")
        products = EMERGENCY_PRODUCTS
        source = "Emergency Backup (158 Products)"

    print(f"  Source  : {source}")
    print(f"  Products: {len(products)}")

    # Generate main website
    html = generate_html(products)
    # Inject JSON-LD schema post-render (avoids f-string brace conflicts)
    html = html.replace("JSONLD_PLACEHOLDER", build_jsonld(products), 1)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print("  [OK] Website generated: docs/index.html")
    size = len(html)
    print(f"  Size: {size:,} characters")

    # Generate SEO files
    sitemap = generate_sitemap(products)
    sitemap_path = os.path.join(OUTPUT_DIR, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap)
    n_urls = len(products) + 1
    print(f"  [OK] Sitemap generated: docs/sitemap.xml ({n_urls} URLs)")

    robots = generate_robots()
    robots_path = os.path.join(OUTPUT_DIR, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(robots)
    print("  [OK] robots.txt: docs/robots.txt")

    print("=" * 55)
    print("  SEO URLs for Google Search Console:")
    sc_url = SITE_URL
    print(f"     {sc_url}/")
    print(f"     {sc_url}/sitemap.xml")
    print("=" * 55)
