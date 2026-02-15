import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# --- HELIUM 10 ELITE UI CONFIG ---
st.set_page_config(page_title="Helium 10 KDP Elite", layout="wide", page_icon="💎")

# Your ScraperAPI Key
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

# --- BRANDED STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f0f4f7; }
    [data-testid="stSidebar"] { background-color: #0c1c2c; }
    .stButton>button { background-color: #00aaff; color: white; border-radius: 4px; font-weight: bold; border: none; height: 3.5em; width: 100%; }
    .h10-card { background: white; padding: 20px; border-radius: 4px; border-top: 5px solid #00aaff; box-shadow: 0 2px 10px rgba(0,0,0,0.05); text-align: center; }
    .product-box { background: white; padding: 15px; border-radius: 8px; border: 1px solid #e0e6ed; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR LOGO & NAV ---
st.sidebar.markdown("<h1 style='color: white; text-align: center;'>HELIUM 10</h1>", unsafe_allow_html=True)
st.sidebar.markdown("---")
menu = st.sidebar.radio("TOOLS", ["Black Box (Niche Spy)", "Magnet (7-Slot Optimizer)", "Profits (Visual Sales Analysis)"])

# --- CORE LOGIC ---
def fetch_h10_data(market, query, country):
    payload = {
        'api_key': SCRAPER_API_KEY,
        'url': f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks",
        'country_code': country, 'premium': 'true', 'render': 'true'
    }
    try:
        return requests.get('http://api.scraperapi.com', params=payload, timeout=90)
    except: return None

def calculate_monthly_sales(price_str):
    try:
        price = float(re.sub(r'[^\d.]', '', price_str.replace(',', '.')))
        if price < 10: return "Estimated 250 - 600 Sales/mo"
        if price < 20: return "Estimated 80 - 200 Sales/mo"
        return "Estimated 20 - 50 Sales/mo"
    except: return "Data Pending"

# --- TOOL 1: BLACK BOX (Niche Research) ---
if menu == "Black Box (Niche Spy)":
    st.title("📦 Black Box: Niche Research")
    c1, c2 = st.columns([1, 2])
    with c1: market = st.selectbox("Marketplace", ["amazon.fr", "amazon.de", "amazon.com"])
    with c2: query = st.text_input("Enter Keyword:", value="cahier de texte")

    if st.button("SEARCH"):
        cc = market.split('.')[-1] if market != 'amazon.com' else 'us'
        res = fetch_h10_data(market, query, cc)
        if res and res.status_code == 200:
            soup = BeautifulSoup(res.content, "html.parser")
            items = soup.select('div[data-component-type="s-search-result"]')
            data = []
            for item in items[:20]:
                title = item.h2.text.strip()[:70] if item.h2 else "N/A"
                asin = item.get('data-asin', 'N/A')
                price = item.select_one('.a-price .a-offscreen').text if item.select_one('.a-price .a-offscreen') else "N/A"
                data.append({"Title": title, "ASIN": asin, "Price": price})
            st.dataframe(pd.DataFrame(data), use_container_width=True)

# --- TOOL 2: MAGNET (Localized 7-Slot KeyGen) ---
elif menu == "Magnet (7-Slot Optimizer)":
    st.title("🧲 Magnet: Keyword Research (Localized)")
    market_lang = st.selectbox("Target Marketplace", ["France (FR)", "USA (EN)", "Germany (DE)"])
    seed = st.text_input("Seed Keyword (Title/Niche):", value="agenda scolaire")

    if st.button("GET PRO KEYWORDS"):
        if "France" in market_lang:
            keywords = [f"{seed} 2025 2026", f"meilleur {seed} etudiant", f"{seed} scolaire college", f"organisateur {seed} journalier", f"cadeau rentree {seed}", f"planificateur {seed} a5", f"{seed} primaire lycee"]
        elif "Germany" in market_lang:
            keywords = [f"{seed} 2025 2026", f"schulplaner {seed}", f"hausaufgabenheft {seed}", f"kalender {seed}", f"wochenplaner {seed}", f"planer {seed} a5", f"geschenk {seed}"]
        else:
            keywords = [f"best {seed} 2025", f"{seed} for students", f"personalized {seed} planner", f"large print {seed} book", f"academic {seed} journal", f"minimalist {seed}", f"daily {seed} organization"]
        
        st.info(f"Top 7 Backend Slots for {market_lang}:")
        for i, k in enumerate(keywords): st.code(f"Slot {i+1}: {k}")

# --- TOOL 3: PROFITS (Visual Sales & Product Analysis) ---
elif menu == "Profits (Visual Sales Analysis)":
    st.title("📈 Profits: Visual Sales Spy")
    mkt_res = st.selectbox("Select Market", ["amazon.fr", "amazon.com"])
    niche_q = st.text_input("Enter Niche to Spy:", value="cahier de texte")

    if st.button("ANALYZE SALES"):
        cc = 'fr' if 'fr' in mkt_res else 'us'
        res = fetch_h10_data(mkt_res, niche_q, cc)
        if res and res.status_code == 200:
            soup = BeautifulSoup(res.content, "html.parser")
            products = soup.select('div[data-component-type="s-search-result"]')
            
            for prod in products[:12]:
                asin = prod.get('data-asin', 'N/A')
                title = prod.h2.text.strip() if prod.h2 else "N/A"
                price = prod.select_one('.a-price .a-offscreen').text if prod.select_one('.a-price .a-offscreen') else "N/A"
                img = prod.select_one('img.s-image')['src']
                
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    with col1: st.image(img, width=130)
                    with col2:
                        st.markdown(f"**{title}**")
                        st.markdown(f"**ASIN:** `{asin}` | **Price:** `{price}`")
                        st.success(f"🔥 {calculate_monthly_sales(price)}")
                        st.markdown("---")

st.sidebar.markdown("---")
st.sidebar.caption("KDP Helium Elite v5 | Partner Support")
