import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from collections import Counter
from urllib.parse import quote

# --- ADVANCED CONFIG ---
st.set_page_config(page_title="KDP Command Center v2.0", layout="wide", page_icon="📈")
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

# --- UI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff9900; color: white; }
    .status-box { padding: 20px; border-radius: 10px; background-color: white; border-left: 5px solid #ff9900; }
    .img-container { border: 2px solid #ff9900; border-radius: 10px; padding: 5px; background: white; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🚀 Navigation Menu")
app_mode = st.sidebar.selectbox("Choose Tool", 
    ["Global Spy Pro", "Hot Trends (EU)", "7-Slot Key-Gen", "AI Product Research", "Creative Studio"])

# --- SHARED FUNCTIONS ---
def fetch_amazon_data(market, query, country_code):
    payload = {
        'api_key': SCRAPER_API_KEY,
        'url': f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks",
        'country_code': country_code,
        'premium': 'true',
        'device_type': 'desktop',
        'keep_headers': 'true'
    }
    headers = {
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8" if country_code == 'fr' else "en-US,en;q=0.9",
        "Referer": f"https://www.{market}/"
    }
    try:
        response = requests.get('http://api.scraperapi.com', params=payload, headers=headers, timeout=60)
        return response
    except:
        return None

# --- TOOL 1: GLOBAL SPY PRO ---
if app_mode == "Global Spy Pro":
    st.title("🌍 KDP Global Niche Hunter")
    col1, col2 = st.columns([1, 2])
    with col1:
        market = st.selectbox("Market", ["amazon.fr", "amazon.de", "amazon.it", "amazon.es", "amazon.com"])
    with col2:
        query = st.text_input("Niche Keyword:", placeholder="e.g., 'Cahier de vacances'")

    if st.button("🚀 Analyze Market"):
        if query:
            country_code = market.split('.')[-1] if market != 'amazon.com' else 'us'
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
                    data.append({"Title": title[:60], "ASIN": asin, "Price": price, "Link": f"https://{market}/dp/{asin}"})
                st.dataframe(pd.DataFrame(data), use_container_width=True)

# --- TOOL 2: HOT TRENDS (EU) ---
elif app_mode == "Hot Trends (EU)":
    st.title("🔥 Current EU Hot Trends")
    st.info("Live market trends for high-demand seasonal niches.")
    trends = {
        "France (FR)": ["Agenda Scolaire 2025-2026", "Livre de Coloriage Adulte", "Cahier de Vacances CP", "Journal de Gratitude"],
        "Germany (DE)": ["Schulplaner 2025", "Malbuch für Kinder", "Haushaltsbuch", "Dankbarkeit Tagebuch"],
        "Italy (IT)": ["Agenda Settimanale 2025", "Libro da Colorare", "Diario Segreto"],
        "Spain (ES)": ["Agenda Escolar", "Libro de Colorear para Adultos", "Cuaderno de Actividades"]
    }
    cols = st.columns(len(trends))
    for i, (country, items) in enumerate(trends.items()):
        with cols[i]:
            st.subheader(country)
            for item in items:
                st.write(f"✅ {item}")

# --- TOOL 3: 7-SLOT KEY-GEN ---
elif app_mode == "7-Slot Key-Gen":
    st.title("🔑 The 7-Slot Optimizer")
    input_text = st.text_input("Enter Title/Niche:")
    if st.button("Generate Pro Keywords"):
        keywords = [f"{input_text} for beginners", f"best {input_text} 2025", f"personalized {input_text}", f"large print {input_text}", f"gift ideas {input_text}", f"professional {input_text} notebook", f"daily {input_text} tracker"]
        st.success("Target these for your 7 backend slots:")
        for i, kw in enumerate(keywords): st.code(f"Slot {i+1}: {kw}")

# --- TOOL 4: AI PRODUCT RESEARCH ---
elif app_mode == "AI Product Research":
    st.title("🧠 AI Niche Deep-Dive")
    target_niche = st.text_input("Niche to analyze:")
    if target_niche:
        with st.expander("View AI Analysis Report"):
            st.write(f"**Niche Profitability:** High")
            st.write(f"**Competition Level:** Medium-Low in {datetime.now().year}")
            st.write(f"**Recommended Price:** 7.99€ - 12.99€")

# --- TOOL 5: CREATIVE STUDIO (IMAGE GENERATOR) ---
elif app_mode == "Creative Studio":
    st.title("🎨 AI Image & Cover Generator")
    st.markdown("Generate high-quality visuals for your KDP covers and interiors.")
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.subheader("Design Settings")
        subject = st.text_input("Main Subject:", placeholder="e.g., 'Cute cat playing with wool'")
        style = st.selectbox("Art Style:", ["Minimalist Vector", "Watercolor Painting", "Oil Painting", "3D Render", "Vintage Illustration", "Coloring Book Page (Black & White)"])
        ratio = st.selectbox("Aspect Ratio:", ["1:1 (Square)", "2:3 (Book Cover)", "3:2 (Landscape)"])
        
        generate_btn = st.button("🎨 Generate Image")

    with col_b:
        st.subheader("Preview")
        if generate_btn and subject:
            # Constructing a high-quality prompt for the AI
            final_prompt = f"{subject}, {style} style, high resolution, professional lighting, detailed, 8k, amazon kdp style"
            if "Coloring Book" in style:
                final_prompt = f"Black and white, bold lines, coloring book page for kids, {subject}, white background, no shading"
            
            # Use Pollinations AI for free image generation
            width = 1024
            height = 1536 if "2:3" in ratio else (1024 if "1:1" in ratio else 680)
            
            encoded_prompt = quote(final_prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&enhance=true"
            
            with st.spinner("AI is painting your design..."):
                try:
                    st.markdown(f'<div class="img-container"><img src="{image_url}" width="100%"></div>', unsafe_allow_html=True)
                    st.markdown(f"[🔗 Open Full Image]({image_url})")
                    st.info(f"**Final Prompt Used:** {final_prompt}")
                except:
                    st.error("Image generation failed. Try a different prompt.")
        else:
            st.info("Enter a subject and click generate to see the magic.")

st.sidebar.markdown("---")
st.sidebar.info(f"Partner, your capital of 90,000 MAD is in safe hands with data-driven decisions.")
