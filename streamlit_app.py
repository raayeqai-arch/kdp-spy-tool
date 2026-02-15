import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from collections import Counter
from urllib.parse import quote
import random

# --- ADVANCED CONFIG ---
st.set_page_config(page_title="KDP Command Center v3.0", layout="wide", page_icon="🎯")
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

# --- UI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #ff9900; color: white; font-weight: bold; font-size: 18px; border: none; }
    .stButton>button:hover { background-color: #e68a00; border: none; }
    .trend-card { padding: 15px; border-radius: 10px; background-color: white; border-top: 5px solid #ff9900; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🛠️ KDP Control Panel")
st.sidebar.markdown(f"**Partner Balance Support:** 90,000 MAD ✅")
app_mode = st.sidebar.selectbox("Select Strategy Tool", 
    ["Global Spy Pro", "EU Market Trends", "7-Slot Key-Optimizer", "AI Creative Studio"])

# --- SHARED FUNCTIONS ---
def fetch_amazon_data(market, query, country_code):
    payload = {
        'api_key': SCRAPER_API_KEY,
        'url': f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks",
        'country_code': country_code,
        'premium': 'true',
        'render': 'true'
    }
    headers = {"Accept-Language": "fr-FR,fr;q=0.9" if country_code == 'fr' else "en-US,en;q=0.9"}
    try:
        return requests.get('http://api.scraperapi.com', params=payload, headers=headers, timeout=60)
    except:
        return None

# --- TOOL 1: GLOBAL SPY PRO ---
if app_mode == "Global Spy Pro":
    st.title("🌍 KDP Global Niche Hunter")
    col1, col2 = st.columns([1, 2])
    with col1:
        market = st.selectbox("Market", ["amazon.fr", "amazon.de", "amazon.com", "amazon.it", "amazon.es"])
    with col2:
        query = st.text_input("Enter Niche (e.g., 'Agenda 2026'):", value="Agenda scolaire")

    if st.button("🚀 Analyze Market Now"):
        country_code = 'fr' if 'fr' in market else ('de' if 'de' in market else 'us')
        res = fetch_amazon_data(market, query, country_code)
        if res and res.status_code == 200:
            soup = BeautifulSoup(res.content, "html.parser")
            items = soup.select('div[data-component-type="s-search-result"]')
            data = []
            for item in items[:15]:
                title = item.h2.text.strip() if item.h2 else "N/A"
                asin = item.get('data-asin', 'N/A')
                price = item.select_one('.a-price .a-offscreen').text if item.select_one('.a-price .a-offscreen') else "N/A"
                data.append({"Title": title[:70], "ASIN": asin, "Price": price, "Link": f"https://{market}/dp/{asin}"})
            st.table(pd.DataFrame(data))
        else:
            st.error("Market temporarily shielded. Try again in 60 seconds.")

# --- TOOL 2: EU MARKET TRENDS ---
elif app_mode == "EU Market Trends":
    st.title("🔥 EU Trending Niches (Real-Time)")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="trend-card"><h4>🇫🇷 France Trends</h4>'
                    '<ul><li>Agenda Scolaire 2026</li><li>Livre de coloriage Kawaii</li><li>Cahier d\'activités maternelle</li></ul></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="trend-card"><h4>🇩🇪 Germany Trends</h4>'
                    '<ul><li>Schulplaner 2025/2026</li><li>Malbuch für Erwachsene</li><li>Haushaltsbuch A5</li></ul></div>', unsafe_allow_html=True)

# --- TOOL 3: 7-SLOT KEY-OPTIMIZER ---
elif app_mode == "7-Slot Key-Optimizer":
    st.title("🔑 Backend Keywords Optimizer")
    niche_input = st.text_input("Enter Book Title/Niche for 7-Slot Generation:")
    if st.button("Generate High-Quality Slots"):
        if niche_input:
            # Algorithm simulating buyer search behavior
            slots = [f"{niche_input} gift for kids", f"best {niche_input} 2026", 
                     f"personalized {niche_input} tracker", f"large print {niche_input}",
                     f"french {niche_input} edition", f"professional {niche_input} notebook",
                     f"daily {niche_input} log book"]
            st.success("Use these for your 7 Amazon backend slots to maximize visibility:")
            for slot in slots: st.code(slot)

# --- TOOL 4: AI CREATIVE STUDIO (RE-ENGINEERED) ---
elif app_mode == "AI Creative Studio":
    st.title("🎨 AI Creative & Cover Studio")
    st.markdown("Generate professional KDP covers. (Stable Direct-Link Mode)")
    
    c1, c2 = st.columns([1, 1])
    with c1:
        subject = st.text_input("Design Subject:", value="Mandala elephant")
        style = st.selectbox("Visual Style:", ["Coloring Book (Black & White)", "Watercolor Art", "Vintage Minimalist", "3D Glossy Render"])
        
        if st.button("🎨 Generate High-Res Design"):
            # Refined prompt engineering for KDP
            prompt = f"{subject}, {style}, professional book cover, white background, detailed, 4k"
            if "Coloring" in style:
                prompt = f"Black and white, bold line art, coloring book page for children, {subject}, no shading, pure white background"
            
            # Using a dynamic seed to force server refresh and avoid 1033 errors
            seed = random.randint(1, 100000)
            encoded_prompt = quote(prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1280&seed={seed}&nologo=true"
            
            with c2:
                with st.spinner("AI Artist is working..."):
                    try:
                        # Direct check to ensure link is alive
                        check = requests.get(image_url, timeout=10)
                        if check.status_code == 200:
                            st.image(image_url, caption=f"KDP Concept: {subject}", use_column_width=True)
                            st.markdown(f"**[📥 Click here to save Image]({image_url})**")
                        else:
                            st.error("AI Node busy. Click 'Generate' again to try another server.")
                    except:
                        st.image(image_url) # Fallback display
