import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# --- HELIUM 10 BRAND IDENTITY ---
st.set_page_config(page_title="Helium 10 KDP Elite v6", layout="wide", page_icon="💎")

# Your ScraperAPI Key
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

# --- HELIUM 10 UI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    [data-testid="stSidebar"] { background-color: #0c1c2c; }
    .stButton>button { 
        background-color: #00aaff; color: white; border-radius: 4px; 
        font-weight: bold; border: none; height: 3.5em; width: 100%;
    }
    .stButton>button:hover { background-color: #0088cc; }
    .h10-card {
        background: white; padding: 20px; border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-top: 5px solid #00aaff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("<h1 style='color: white; text-align: center;'>HELIUM 10</h1>", unsafe_allow_html=True)
st.sidebar.markdown("---")
menu = st.sidebar.radio("TOOLS", ["Magnet (7-Slot Gen)", "Profits (Niche Analyzer)", "X-Ray (Market Intel)"])

# --- CORE DATA ENGINE ---
def fetch_amazon_data(market, query, country):
    payload = {
        'api_key': SCRAPER_API_KEY,
        'url': f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks",
        'country_code': country, 'premium': 'true', 'render': 'true'
    }
    try:
        # Increased timeout to prevent "Empty" results
        return requests.get('http://api.scraperapi.com', params=payload, timeout=100)
    except: return None

# --- TOOL 1: MAGNET (7-Slot Multi-Lang Generator) ---
if menu == "Magnet (7-Slot Gen)":
    st.title("🧲 Magnet: Keyword Research")
    st.info("Generates optimized keywords in the target market language.")
    
    col_lang, col_query = st.columns([1, 2])
    with col_lang:
        lang = st.selectbox("Market Language", ["French (FR)", "English (US/UK)", "German (DE)"])
    with col_query:
        seed = st.text_input("Enter Niche Keyword:", value="agenda scolaire")

    if st.button("GET KEYWORDS"):
        # Specialized 7-Slot Logic for French Market
        if "French" in lang:
            keywords = [f"{seed} 2025 2026", f"meilleur {seed} étudiant", f"{seed} scolaire collège", f"organisateur {seed} journalier", f"cadeau rentrée {seed}", f"planificateur {seed} a5", f"{seed} primaire lycée"]
        else:
            keywords = [f"best {seed} 2025", f"{seed} for students", f"personalized {seed} planner", f"large print {seed} book", f"academic {seed} journal", f"minimalist {seed}", f"daily {seed} organization"]
        
        st.success(f"Top 7 Backend Slots for {lang}:")
        for i, k in enumerate(keywords): st.code(f"Slot {i+1}: {k}")

# --- TOOL 2: PROFITS (Niche Analyzer) ---
elif menu == "Profits (Niche Analyzer)":
    st.title("📈 Profits: Market Profitability")
    c1, c2 = st.columns([1, 2])
    with c1: 
        mkt = st.selectbox("Select Marketplace", ["amazon.fr", "amazon.com", "amazon.de"])
    with c2: 
        q = st.text_input("Analyze Niche Keyword:", value="cahier de texte")

    if st.button("ANALYZE MARKET"):
        cc = 'fr' if 'fr' in mkt else ('de' if 'de' in mkt else 'us')
        with st.spinner(f"Establishing secure tunnel to {mkt}..."):
            res = fetch_amazon_data(mkt, q, cc)
            if res and res.status_code == 200:
                soup = BeautifulSoup(res.content, "html.parser")
                items = soup.select('div[data-component-type="s-search-result"]')
                df_data = []
                for item in items[:20]:
                    t = item.h2.text.strip()[:70] if item.h2 else "N/A"
                    a = item.get('data-asin', 'N/A')
                    p = item.select_one('.a-price .a-offscreen').text if item.select_one('.a-price .a-offscreen') else "N/A"
                    df_data.append({"Title": t, "ASIN": a, "Price": p})
                
                if df_data:
                    st.dataframe(pd.DataFrame(df_data), use_container_width=True)
                else:
                    st.error("No items found. Try a broader keyword.")
            else: st.error("API Connection Refused. Please wait 60 seconds.")

# --- TOOL 3: X-RAY (Market Intel) ---
elif menu == "X-Ray (Market Intel)":
    st.title("💎 X-Ray: Market Overview")
    st.markdown('<div class="h10-card"><h4>Market Viability Report</h4><p>Analyze price averages and competition levels for your chosen niche.</p></div>', unsafe_allow_html=True)
    st.warning("Note: X-Ray uses Deep Scanning. This may take up to 60 seconds.")

st.sidebar.markdown("---")
st.sidebar.caption("KDP Helium Elite v6.0 | Partner Suite")
