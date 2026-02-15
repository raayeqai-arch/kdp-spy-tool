import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote
import random

# --- ADVANCED UI CONFIG ---
st.set_page_config(page_title="KDP Partner Suite v5", layout="wide", page_icon="🛡️")
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

st.markdown("""
    <style>
    .stButton>button { background: linear-gradient(90deg, #ff9900, #ffcc00); color: white; border-radius: 12px; font-weight: bold; height: 3.5em; border: none; }
    .card { padding: 20px; border-radius: 15px; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 5px solid #ff9900; margin-bottom: 20px; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e3b4e,#2e3b4e); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR DASHBOARD ---
st.sidebar.title("🎮 Partner Command")
st.sidebar.info(f"Support Balance: 90,000 MAD ✅")
menu = st.sidebar.radio("Navigation", ["Global Spy Pro", "EU Market Trends", "7-Backend Key-Gen", "AI Design Studio"])

# --- SHARED FUNCTIONS ---
def get_amazon_data(market, query, country):
    payload = {
        'api_key': SCRAPER_API_KEY, 'url': f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks",
        'country_code': country, 'premium': 'true', 'render': 'true'
    }
    try:
        return requests.get('http://api.scraperapi.com', params=payload, timeout=90)
    except: return None

# --- TOOL 1: GLOBAL SPY PRO ---
if menu == "Global Spy Pro":
    st.title("🛡️ Market Spy (Advanced Unlock)")
    c1, c2 = st.columns([1, 2])
    with c1: target_m = st.selectbox("Market", ["amazon.fr", "amazon.de", "amazon.com"])
    with c2: target_q = st.text_input("Niche:", value="Agenda scolaire 2026")

    if st.button("🚀 Analyze Market"):
        cc = 'fr' if 'fr' in target_m else ('de' if 'de' in target_m else 'us')
        with st.spinner(f"Unlocking {target_m}..."):
            res = get_amazon_data(target_m, target_q, cc)
            if res and res.status_code == 200:
                soup = BeautifulSoup(res.content, "html.parser")
                items = soup.select('div[data-component-type="s-search-result"]')
                results = []
                for item in items[:15]:
                    title = item.h2.text.strip() if item.h2 else "N/A"
                    asin = item.get('data-asin', 'N/A')
                    price = item.select_one('.a-price .a-offscreen').text if item.select_one('.a-price .a-offscreen') else "N/A"
                    results.append({"Title": title[:65], "ASIN": asin, "Price": price, "Link": f"https://{target_m}/dp/{asin}"})
                st.dataframe(pd.DataFrame(results), use_container_width=True)
            else: st.error("Access issue. Please try a simpler keyword first.")

# --- TOOL 2: EU MARKET TRENDS ---
elif menu == "EU Market Trends":
    st.title("🔥 EU Trend Radar")
    t_cols = st.columns(3)
    with t_cols[0]:
        st.markdown('<div class="card"><h4>🇫🇷 France</h4><ul><li>Agenda 2026-2027</li><li>Coloriage Zen</li><li>Journal Bord de Mer</li></ul></div>', unsafe_allow_html=True)
    with t_cols[1]:
        st.markdown('<div class="card"><h4>🇩🇪 Germany</h4><ul><li>Schulplaner 2026</li><li>Haushaltsbuch</li><li>Malbuch Tiere</li></ul></div>', unsafe_allow_html=True)
    with t_cols[2]:
        st.markdown('<div class="card"><h4>🇮🇹 Italy / 🇪🇸 Spain</h4><ul><li>Agenda Settimanale</li><li>Libro da colorare</li><li>Diario Escolar</li></ul></div>', unsafe_allow_html=True)

# --- TOOL 3: 7-BACKEND KEY-GEN ---
elif menu == "7-Backend Key-Gen":
    st.title("🔑 Backend Keywords Master")
    base_niche = st.text_input("Enter Niche (e.g., 'Agenda'):", value="Agenda scolaire")
    if st.button("Generate Strategic Keywords"):
        slots = [f"{base_niche} student 2026", f"best {base_niche} gift", f"french {base_niche} planner", f"large {base_niche} notebook", f"minimalist {base_niche}", f"academic {base_niche} year", f"daily {base_niche} tracker"]
        st.success("Target these in your 7 backend slots:")
        for s in slots: st.code(s)

# --- TOOL 4: AI DESIGN STUDIO (THE FIX) ---
elif menu == "AI Design Studio":
    st.title("🎨 AI Creative Studio (Multi-Node Recovery)")
    st.markdown("If the image doesn't appear, use the **'Magic Link'** below.")
    
    sc1, sc2 = st.columns([1, 1])
    with sc1:
        subject = st.text_input("Description:", value="Vintage cat in garden")
        style = st.selectbox("Style", ["Watercolor", "Vector Art", "Coloring Book (B&W)", "Realistic"])
        
        if st.button("🎨 Generate Design"):
            prompt = f"{subject}, {style}, professional KDP cover, high resolution"
            if "Coloring" in style: prompt = f"Bold black and white line art, coloring book, {subject}, white background"
            
            seed = random.randint(1, 999999)
            # Generating direct link
            image_url = f"https://image.pollinations.ai/prompt/{quote(prompt)}?width=1024&height=1280&seed={seed}&nologo=true"
            
            with sc2:
                st.subheader("Results")
                # Fallback: Link + Image
                st.markdown(f"### 🪄 [CLICK HERE TO OPEN IMAGE]({image_url})")
                st.image(image_url, caption="Preview (If not loading, use the link above)", use_column_width=True)
                st.info("Tip: If you see a blank box, it's due to high server traffic. The link above will always work.")
