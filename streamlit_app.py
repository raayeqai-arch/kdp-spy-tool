import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

# --- GLOBAL CONFIG ---
st.set_page_config(page_title="KDP Spy Ultra v6", layout="wide", page_icon="🚀")
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

st.title("🚀 KDP Niche Intelligence (Global Recovery v6)")
st.markdown("Equipped with **Adaptive Content Discovery** for Amazon.fr stability.")
st.divider()

# --- INPUT SECTION ---
col1, col2 = st.columns([1, 2])
with col1:
    market = st.selectbox("Marketplace", ["amazon.fr", "amazon.com", "amazon.co.uk"])
with col2:
    query = st.text_input("Enter Niche Keyword:", value="agenda scolaire 2026 2027")

# --- KEYWORD ENGINE ---
def extract_top_keywords(titles):
    stop_words = {'a', 'an', 'the', 'for', 'with', 'and', 'in', 'on', 'of', 'to', 'is', 'de', 'la', 'le', 'et', 'pour', 'des', 'du', 'un', 'une', 'les'}
    all_words = []
    for title in titles:
        words = re.findall(r'\w+', title.lower())
        all_words.extend([w for w in words if w not in stop_words and len(w) > 2 and not w.isdigit()])
    return Counter(all_words).most_common(10)

# --- MAIN SCRAPER ---
if st.button("🔍 Run Adaptive Market Analysis"):
    if query:
        proxy_country = 'fr' if 'fr' in market else 'us'
        
        # Enhanced Payload for France
        payload = {
            'api_key': SCRAPER_API_KEY,
            'url': f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks",
            'country_code': proxy_country,
            'premium': 'true',
            'render': 'true',
            'session_number': '789' # Reset session
        }
        
        with st.spinner(f'Initiating Adaptive Scan on {market}...'):
            try:
                response = requests.get('http://api.scraperapi.com', params=payload, timeout=90)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    # Adaptive Selector: Find any div that has an ASIN
                    items = soup.find_all("div", {"data-asin": True})
                    
                    data_list = []
                    titles = []
                    
                    for item in items:
                        asin = item.get('data-asin')
                        if not asin or len(asin) != 10: continue
                        
                        # Find title: look for any header or text near the ASIN link
                        title_el = item.find("h2") or item.select_one(f'a[href*="{asin}"] span')
                        title = title_el.text.strip() if title_el else "Unknown Title"
                        
                        # Find price: look for any element with currency symbol
                        price_el = item.select_one('.a-price .a-offscreen') or item.find(text=re.compile(r'[€$£]'))
                        price = price_el.text if hasattr(price_el, 'text') else str(price_el)
                        
                        if title != "Unknown Title":
                            titles.append(title)
                            data_list.append({
                                "Title": title[:70],
                                "ASIN": asin,
                                "Price": price if len(price) < 15 else "View on Site",
                                "Link": f"https://www.{market}/dp/{asin}"
                            })

                    if data_list:
                        # Display Keywords
                        st.subheader("💡 Strategic Keywords Found")
                        top_kw = extract_top_keywords(titles)
                        cols = st.columns(5)
                        for i, (word, count) in enumerate(top_kw):
                            cols[i % 5].metric(word, f"{count}x")
                        
                        st.divider()
                        st.subheader("📦 Market Overview")
                        st.table(pd.DataFrame(data_list[:20]))
                    else:
                        st.error("Amazon France layout is still blocking parsing. Please try again in 10 minutes.")
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
