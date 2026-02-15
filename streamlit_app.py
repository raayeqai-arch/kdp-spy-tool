import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import random
import io

# --- TECH SUITE CONFIG ---
st.set_page_config(page_title="KDP Tech Suite v7", layout="wide", page_icon="🛠️")
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

# --- CUSTOM INTERFACE ---
st.markdown("""
    <style>
    .stButton>button { background: #007bff; color: white; border-radius: 8px; font-weight: bold; border:none; height: 3.5em; }
    .stButton>button:hover { background: #0056b3; }
    .card-box { background: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #eaeaea; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
menu = st.sidebar.radio("Technical Tools", ["Niche Analytics", "7-Slot Keyword Gen", "AI Cover Lab"])

# --- SHARED SCRAPER ENGINE ---
def get_amazon_raw(market, query, country):
    payload = {
        'api_key': SCRAPER_API_KEY, 
        'url': f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks",
        'country_code': country, 
        'premium': 'true', 
        'render': 'true'
    }
    try:
        return requests.get('http://api.scraperapi.com', params=payload, timeout=90)
    except: return None

# --- TOOL 1: NICHE ANALYTICS ---
if menu == "Niche Analytics":
    st.title("🛠️ Advanced Niche Analytics")
    c1, c2 = st.columns([1, 2])
    with c1: 
        mkt = st.selectbox("Marketplace", ["amazon.fr", "amazon.de", "amazon.com"])
    with c2: 
        kw = st.text_input("Enter Niche Keyword:", value="Cahier de texte")

    if st.button("🚀 Deep Scan Market"):
        cc = 'fr' if 'fr' in mkt else ('de' if 'de' in mkt else 'us')
        with st.spinner(f"Establishing secure tunnel to {mkt}..."):
            res = get_amazon_raw(mkt, kw, cc)
            if res and res.status_code == 200:
                soup = BeautifulSoup(res.content, "html.parser")
                items = soup.select('div[data-component-type="s-search-result"]')
                results = []
                for item in items[:15]:
                    title = item.h2.text.strip() if item.h2 else "N/A"
                    asin = item.get('data-asin', 'N/A')
                    price_el = item.select_one('.a-price .a-offscreen')
                    price = price_el.text if price_el else "N/A"
                    results.append({"Title": title[:70], "ASIN": asin, "Price": price, "Link": f"https://{mkt}/dp/{asin}"})
                st.dataframe(pd.DataFrame(results), use_container_width=True)
            else: st.error("Parsing failed. Amazon.fr security update detected. Try again.")

# --- TOOL 2: 7-SLOT KEYWORD GEN ---
elif menu == "7-Slot Keyword Gen":
    st.title("🔑 Backend Optimization (7 Slots)")
    seed = st.text_input("Main Book Niche:", value="Agenda scolaire")
    if st.button("Generate High-Conversion Slots"):
        # Technical keywords mapping for high BSR products
        slots = [f"{seed} 2026 2027", f"best {seed} for students", f"personalized {seed} organizer", 
                 f"large print {seed} book", f"french {seed} edition", f"minimalist {seed} planner", 
                 f"daily {seed} tracker"]
        st.success("Target these in your KDP backend slots:")
        for s in slots: st.code(s)

# --- TOOL 3: AI COVER LAB (THE FINAL FIX) ---
elif menu == "AI Cover Lab":
    st.title("🎨 AI Cover & Image Lab")
    st.markdown("This tool uses **Server-Side Fetching** to bypass 1033 browser errors.")
    
    col_in, col_out = st.columns([1, 1])
    with col_in:
        desc = st.text_input("Cover Description:", value="Abstract geometric pattern")
        style = st.selectbox("Design Style", ["Minimalist Vector", "Watercolor Painting", "Vintage Line Art"])
        
        if st.button("🎨 Generate & Render"):
            prompt = f"{desc}, {style}, professional KDP book cover, high detail, white background"
            if "Line Art" in style: 
                prompt = f"Black and white, bold line art, coloring book page, {desc}, white background"
            
            seed = random.randint(1, 999999)
            # Technical direct fetch link
            img_url = f"https://image.pollinations.ai/prompt/{quote(prompt)}?width=1024&height=1280&seed={seed}&nologo=true"
            
            with col_out:
                with st.spinner("Processing image through server node..."):
                    try:
                        # Fetch the image data first on the server
                        response = requests.get(img_url, timeout=30)
                        if response.status_code == 200:
                            img_data = response.content
                            st.image(img_data, caption=f"KDP Concept: {desc}", use_column_width=True)
                            st.download_button("📥 Download Design (PNG)", img_data, file_name="kdp_cover_concept.png", mime="image/png")
                        else:
                            st.error(f"AI Node busy. Direct link: [Open Design]({img_url})")
                    except:
                        st.error("Server connection timeout. Please try one more time.")

st.sidebar.markdown("---")
st.sidebar.caption("KDP Tech Suite v7.0 | Strategy-First Research")
