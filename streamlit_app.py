import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from collections import Counter
from urllib.parse import quote
import io

# --- ADVANCED CONFIG ---
st.set_page_config(page_title="KDP Command Center v2.5", layout="wide", page_icon="🚀")
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

# --- UI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff9900; color: white; font-weight: bold; }
    .status-box { padding: 20px; border-radius: 10px; background-color: white; border-left: 5px solid #ff9900; }
    .img-card { border: 2px solid #ff9900; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🚀 Navigation")
app_mode = st.sidebar.selectbox("Choose Tool", 
    ["Global Spy Pro", "Hot Trends (EU)", "7-Slot Optimizer", "Creative Studio"])

# --- SHARED FUNCTIONS ---
def fetch_amazon_data(market, query, country_code):
    payload = {
        'api_key': SCRAPER_API_KEY,
        'url': f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks",
        'country_code': country_code,
        'premium': 'true',
        'render': 'true'
    }
    try:
        response = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
        return response
    except:
        return None

# --- TOOL 1: GLOBAL SPY PRO ---
if app_mode == "Global Spy Pro":
    st.title("🌍 KDP Global Niche Hunter")
    col1, col2 = st.columns([1, 2])
    with col1:
        market = st.selectbox("Market", ["amazon.fr", "amazon.com", "amazon.de", "amazon.co.uk"])
    with col2:
        query = st.text_input("Niche Keyword:", placeholder="e.g., 'Cahier de texte'")

    if st.button("🚀 Analyze Market"):
        if query:
            country_code = 'fr' if 'fr' in market else ('us' if 'com' in market else 'gb')
            res = fetch_amazon_data(market, query, country_code)
            if res and res.status_code == 200:
                soup = BeautifulSoup(res.content, "html.parser")
                items = soup.select('div[data-component-type="s-search-result"]')
                data = []
                for item in items[:20]:
                    title = item.h2.text.strip() if item.h2 else "N/A"
                    asin = item.get('data-asin', 'N/A')
                    price_tag = item.select_one('.a-price .a-offscreen')
                    price = price_tag.text if price_tag else "N/A"
                    data.append({"Title": title[:70], "ASIN": asin, "Price": price, "Link": f"https://{market}/dp/{asin}"})
                st.success(f"Success! {len(data)} results found.")
                st.dataframe(pd.DataFrame(data), use_container_width=True)
            else:
                st.error("Market blocked. Try again in 2 minutes.")

# --- TOOL 2: HOT TRENDS ---
elif app_mode == "Hot Trends (EU)":
    st.title("🔥 Current EU Hot Trends")
    trends = {
        "France (FR)": ["Agenda Scolaire 2025-2026", "Livre de Coloriage Adulte", "Cahier de Vacances CP"],
        "Germany (DE)": ["Schulplaner 2025", "Malbuch für Kinder", "Haushaltsbuch"],
        "UK/USA": ["Daily Planner 2025", "Workout Journal", "Recipe Book"]
    }
    cols = st.columns(3)
    for i, (country, items) in enumerate(trends.items()):
        with cols[i]:
            st.subheader(country)
            for item in items: st.write(f"✅ {item}")

# --- TOOL 3: 7-SLOT OPTIMIZER ---
elif app_mode == "7-Slot Optimizer":
    st.title("🔑 Backend Keywords Generator")
    title_input = st.text_input("Enter your book title or main niche:")
    if st.button("Generate Keywords"):
        keywords = [f"{title_input} journal", f"best {title_input} 2025", f"personalized {title_input}", f"gift for {title_input} lovers", f"{title_input} notebook", f"large print {title_input}", f"daily {title_input} tracker"]
        st.success("Target these in your 7 backend slots:")
        for i, kw in enumerate(keywords): st.code(kw)

# --- TOOL 4: CREATIVE STUDIO (FIXED) ---
elif app_mode == "Creative Studio":
    st.title("🎨 AI Image & Cover Generator")
    st.markdown("Professional visuals for KDP covers and interiors.")
    
    col_in, col_out = st.columns([1, 1])
    
    with col_in:
        subject = st.text_input("Main Subject:", placeholder="e.g., 'A vintage galaxy with planets'")
        art_style = st.selectbox("Style:", ["Minimalist Vector", "Watercolor", "Coloring Book Page (B&W)", "Realistic 3D", "Vintage Art"])
        ratio = st.selectbox("Ratio:", ["1:1 (Square)", "2:3 (Book Cover)"])
        
        if st.button("🎨 Generate Design"):
            if subject:
                width, height = (1024, 1536) if "2:3" in ratio else (1024, 1024)
                prompt = f"{subject}, {art_style} style, clean background, professional KDP design, 8k"
                if "Coloring" in art_style:
                    prompt = f"Black and white, bold lines, coloring book page, {subject}, no shading, white background"
                
                img_url = f"https://image.pollinations.ai/prompt/{quote(prompt)}?width={width}&height={height}&nologo=true&enhance=true"
                
                with col_out:
                    with st.spinner("AI is drawing your vision..."):
                        try:
                            # We fetch the image to check if it exists and force Streamlit to refresh
                            img_response = requests.get(img_url)
                            if img_response.status_code == 200:
                                st.markdown('<div class="img-card">', unsafe_allow_html=True)
                                st.image(img_url, use_column_width=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                                st.markdown(f"**[📥 Download High-Res Image]({img_url})**")
                                st.success("Design Ready!")
                            else:
                                st.error("AI Server is busy. Please click generate again.")
                        except:
                            st.error("Connection lost. Please try once more.")
            else:
                st.warning("Please enter a subject.")
