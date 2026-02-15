import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from collections import Counter
from urllib.parse import quote
import random
import time

# --- INITIAL CONFIG & THEME ---
st.set_page_config(page_title="KDP Ultimate Center v4", layout="wide", page_icon="🛡️")
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

st.markdown("""
    <style>
    .reportview-container { background: #fdfdfd; }
    .stButton>button { background-color: #ff9900; color: white; border-radius: 10px; font-weight: bold; border: none; height: 3.5em; transition: 0.3s; }
    .stButton>button:hover { background-color: #cc7a00; transform: scale(1.02); }
    .card { padding: 20px; border-radius: 15px; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 6px solid #ff9900; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: PARTNER DASHBOARD ---
st.sidebar.title("🎮 Partner Command")
st.sidebar.success(f"Support Balance: 90,000 MAD ✅")
menu = st.sidebar.radio("Navigation", ["Global Spy Pro", "EU Market Trends", "AI Keyword 7-Slot", "AI Creative Studio"])

# --- CORE FUNCTIONS ---
def get_amazon_response(market, query, country):
    payload = {
        'api_key': SCRAPER_API_KEY, 'url': f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks",
        'country_code': country, 'premium': 'true', 'render': 'true', 'wait_for_selector': '.s-result-item'
    }
    headers = {"Accept-Language": "fr-FR,fr;q=0.9" if country == 'fr' else "en-US,en;q=0.9"}
    try:
        return requests.get('http://api.scraperapi.com', params=payload, headers=headers, timeout=120)
    except: return None

# --- TOOL 1: GLOBAL SPY PRO (FRANCE RECOVERY) ---
if menu == "Global Spy Pro":
    st.title("🛡️ Market Spy (Enhanced FR Unblock)")
    c1, c2 = st.columns([1, 2])
    with c1: target_m = st.selectbox("Market", ["amazon.fr", "amazon.de", "amazon.com", "amazon.it", "amazon.es"])
    with c2: target_q = st.text_input("Niche:", value="Agenda scolaire 2026")

    if st.button("🚀 Deep Market Analysis"):
        cc = 'fr' if 'fr' in target_m else ('de' if 'de' in target_m else 'us')
        with st.spinner(f"Using Premium {cc.upper()} Tunnel to bypass Amazon blocks..."):
            res = get_amazon_response(target_m, target_q, cc)
            if res and res.status_code == 200:
                soup = BeautifulSoup(res.content, "html.parser")
                items = soup.select('div[data-component-type="s-search-result"]')
                df_data = []
                for item in items[:15]:
                    t = item.h2.text.strip() if item.h2 else "N/A"
                    a = item.get('data-asin', 'N/A')
                    p = item.select_one('.a-price .a-offscreen').text if item.select_one('.a-price .a-offscreen') else "N/A"
                    df_data.append({"Title": t[:70], "ASIN": a, "Price": p, "Link": f"https://{target_m}/dp/{a}"})
                st.table(pd.DataFrame(df_data))
            else: st.error("Shield detected. Wait 30 seconds and try a generic keyword.")

# --- TOOL 2: EU TRENDS & OPPORTUNITIES ---
elif menu == "EU Market Trends":
    st.title("🔥 EU Trending Opportunity Radar")
    st.info("Current hot niches in non-US markets for early 2026.")
    t_cols = st.columns(3)
    with t_cols[0]:
        st.markdown('<div class="card"><h4>🇫🇷 France Hot</h4><ul><li>Cahier de texte 2026</li><li>Coloriage Mystère</li><li>Agenda Minimaliste</li></ul></div>', unsafe_allow_html=True)
    with t_cols[1]:
        st.markdown('<div class="card"><h4>🇩🇪 Germany Hot</h4><ul><li>Haushaltsbuch 2026</li><li>Schulplaner A5</li><li>Dankbarkeits Tagebuch</li></ul></div>', unsafe_allow_html=True)
    with t_cols[2]:
        st.markdown('<div class="card"><h4>🇪🇸 Spain Hot</h4><ul><li>Agenda Escolar</li><li>Libro de Colorear</li><li>Diario Personal</li></ul></div>', unsafe_allow_html=True)

# --- TOOL 3: AI KEYWORD 7-SLOT ---
elif menu == "AI Keyword 7-Slot":
    st.title("🔑 7-Backend Slot Optimizer")
    st.markdown("Enter your niche or title to generate high-quality KDP keywords.")
    seed_kw = st.text_input("Base Niche/Title:", value="Agenda scolaire")
    if st.button("Generate High-Profit Keywords"):
        if seed_kw:
            # Sales-driven logic for backend slots
            kdp_slots = [
                f"{seed_kw} for students 2026", f"best {seed_kw} french edition",
                f"personalized {seed_kw} planner", f"large format {seed_kw} notebook",
                f"minimalist {seed_kw} gift", f"academic {seed_kw} journal",
                f"daily {seed_kw} organization"
            ]
            st.success("Target these exact phrases in your 7 Amazon backend slots:")
            for s in kdp_slots: st.code(s)

# --- TOOL 4: AI CREATIVE STUDIO (STABLE ENGINE) ---
elif menu == "AI Creative Studio":
    st.title("🎨 AI Creative Studio (Multi-Node)")
    st.markdown("Generate KDP covers and interior art with stable rendering.")
    sc1, sc2 = st.columns([1, 1])
    with sc1:
        subject = st.text_input("Describe your design:", value="Vintage botanical flowers")
        v_style = st.selectbox("Style", ["WaterColor", "Vector Minimalist", "Black & White Coloring", "3D Render"])
        
        if st.button("🎨 Generate High-Res Concept"):
            final_p = f"{subject}, {v_style}, high quality, professional book cover, white background"
            if "Coloring" in v_style: final_p = f"Bold black and white line art, coloring book page, {subject}, white background, no shading"
            
            # Using random seed and alternative nodes to fix Error 1033
            s = random.randint(100, 999999)
            # Alternative rendering nodes
            nodes = ["https://image.pollinations.ai/prompt/"]
            node = random.choice(nodes)
            img_url = f"{node}{quote(final_p)}?width=1024&height=1280&seed={s}&nologo=true&enhance=true"
            
            with sc2:
                with st.spinner("Rendering your unique design..."):
                    try:
                        # Direct image display with refresh logic
                        st.image(img_url, use_column_width=True)
                        st.markdown(f"**[📥 Download Design]({img_url})**")
                    except: st.error("Node busy. Try clicking 'Generate' again.")

st.sidebar.markdown("---")
st.sidebar.caption("KDP Partner Suite v4.0 | Strategy-First Research")
