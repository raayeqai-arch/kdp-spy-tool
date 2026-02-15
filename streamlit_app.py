import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import random
import base64

# --- ELITE CONFIG ---
st.set_page_config(page_title="KDP Elite Suite v8", layout="wide", page_icon="🛠️")
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stButton>button { background: #007bff; color: white; border-radius: 8px; font-weight: bold; border:none; height: 3.5em; width: 100%; }
    .card-style { background: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #eee; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
menu = st.sidebar.radio("Project Workspace", ["Niche Analyzer", "Keyword Slot Engine", "AI Image Lab"])

# --- ENGINE: AMAZON BYPASS ---
def get_amazon_raw(market, query, country):
    payload = {
        'api_key': SCRAPER_API_KEY, 
        'url': f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks",
        'country_code': country, 
        'premium': 'true', 
        'render': 'true',
        'wait_for_selector': '.s-result-item'
    }
    try:
        return requests.get('http://api.scraperapi.com', params=payload, timeout=90)
    except: return None

# --- TOOL 1: NICHE ANALYZER ---
if menu == "Niche Analyzer":
    st.title("🛠️ Niche Analyzer (Deep Scan)")
    c1, c2 = st.columns([1, 2])
    with c1: 
        mkt = st.selectbox("Marketplace", ["amazon.fr", "amazon.de", "amazon.com"])
    with c2: 
        kw = st.text_input("Search Term:", value="Agenda scolaire")

    if st.button("🚀 Run Deep Analysis"):
        cc = 'fr' if 'fr' in mkt else ('de' if 'de' in mkt else 'us')
        with st.spinner(f"Analyzing {mkt}..."):
            res = get_amazon_raw(mkt, kw, cc)
            if res and res.status_code == 200:
                soup = BeautifulSoup(res.content, "html.parser")
                items = soup.select('div[data-component-type="s-search-result"]')
                df_list = []
                for item in items[:15]:
                    title = item.h2.text.strip() if item.h2 else "N/A"
                    asin = item.get('data-asin', 'N/A')
                    price = item.select_one('.a-price .a-offscreen').text if item.select_one('.a-price .a-offscreen') else "N/A"
                    df_list.append({"Title": title[:70], "ASIN": asin, "Price": price, "Link": f"https://{mkt}/dp/{asin}"})
                st.dataframe(pd.DataFrame(df_list), use_container_width=True)
            else: st.error("Shield active. Retrying recommended in 1 min.")

# --- TOOL 2: KEYWORD SLOT ENGINE ---
elif menu == "Keyword Slot Engine":
    st.title("🔑 Backend 7-Slot Generator")
    seed_niche = st.text_input("Enter Book Niche:", value="Agenda scolaire")
    if st.button("Generate Profitable Keywords"):
        slots = [f"{seed_niche} 2026 2027", f"best {seed_niche} student", f"personalized {seed_niche} planner", 
                 f"large print {seed_niche}", f"french {seed_niche} edition", f"minimalist {seed_niche} journal", 
                 f"daily {seed_niche} organization"]
        st.success("Target these for your 7 Amazon backend slots:")
        for s in slots: st.code(s)

# --- TOOL 3: AI IMAGE LAB (THE BASE64 FIX) ---
elif menu == "AI Image Lab":
    st.title("🎨 AI Elite Image Studio")
    st.info("Using Base64 Direct Encoding to bypass browser errors.")
    
    col_in, col_out = st.columns([1, 1])
    with col_in:
        prompt_txt = st.text_input("Cover Prompt:", value="vintage flowers pattern")
        art_style = st.selectbox("Style", ["Watercolor", "Line Art (Coloring)", "Vector"])
        
        if st.button("🎨 Generate & Embed"):
            final_p = f"{prompt_txt}, {art_style}, professional kdp cover, white background"
            if "Line Art" in art_style: 
                final_p = f"Bold black and white line art, coloring book page, {prompt_txt}, white background"
            
            seed = random.randint(1, 99999)
            image_url = f"https://image.pollinations.ai/prompt/{quote(final_p)}?width=1024&height=1280&seed={seed}&nologo=true"
            
            with col_out:
                with st.spinner("AI Engine generating Base64 stream..."):
                    try:
                        # THE CRITICAL FIX: Download and Encode
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            # Convert to Base64
                            encoded_img = base64.b64encode(response.content).decode()
                            # Display using HTML data URI to bypass CORS/Cloudflare
                            st.markdown(f'<img src="data:image/png;base64,{encoded_img}" width="100%" style="border-radius:10px; border:2px solid #007bff;">', unsafe_allow_html=True)
                            st.download_button("📥 Download PNG", response.content, "cover.png", "image/png")
                        else:
                            st.error("Server busy. Use fallback: [Direct Link]("+image_url+")")
                    except:
                        st.error("Connection timeout. Try again.")

st.sidebar.markdown("---")
st.sidebar.caption("KDP Elite Suite v8.0 | Final Stability Edition")
