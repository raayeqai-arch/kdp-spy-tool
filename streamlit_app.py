import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

# --- GLOBAL CONFIG ---
st.set_page_config(page_title="KDP Spy Ultra v7", layout="wide", page_icon="🛡️")
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

st.title("🛡️ KDP Niche Intelligence (Anti-Block v7)")
st.markdown("Advanced bypass enabled for **Amazon.fr**. This version simulates real user behavior.")
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

# --- THE ENGINE ---
if st.button("🔍 Run Deep Market Analysis"):
    if query:
        proxy_country = 'fr' if 'fr' in market else 'us'
        
        # WE USE 'ULTRA' SETTINGS FOR FRANCE
        payload = {
            'api_key': SCRAPER_API_KEY,
            'url': f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks",
            'country_code': proxy_country,
            'premium': 'true',
            'render': 'true',
            'wait_for_selector': '.s-result-item', # Crucial: Wait for results to load
            'session_number': '1010' # Fresh session ID
        }
        
        with st.spinner(f'Simulating human browse on {market}... This takes ~30 seconds.'):
            try:
                # Rendering takes time, so we set a long timeout
                response = requests.get('http://api.scraperapi.com', params=payload, timeout=120)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    items = soup.find_all("div", {"data-asin": True})
                    
                    data_list = []
                    titles = []
                    
                    for item in items:
                        asin = item.get('data-asin')
                        if not asin or len(asin) != 10: continue
                        
                        # Find title using multiple fallback methods
                        title_el = item.select_one('h2 a span') or item.find("h2")
                        title = title_el.text.strip() if title_el else "Unknown Title"
                        
                        # Find price
                        price_el = item.select_one('.a-price .a-offscreen')
                        price = price_el.text if price_el else "N/A"
                        
                        if title != "Unknown Title":
                            titles.append(title)
                            data_list.append({
                                "Title": title[:70],
                                "ASIN": asin,
                                "Price": price,
                                "Link": f"https://www.{market}/dp/{asin}"
                            })

                    if data_list:
                        st.subheader("💡 Strategic Keywords Found")
                        top_kw = extract_top_keywords(titles)
                        cols = st.columns(5)
                        for i, (word, count) in enumerate(top_kw):
                            cols[i % 5].metric(word, f"{count}x")
                        
                        st.divider()
                        st.subheader("📦 Market Overview")
                        st.dataframe(pd.DataFrame(data_list[:20]), use_container_width=True)
                    else:
                        st.error("Amazon.fr security is still too high. Wait 1 hour or change the keyword.")
                else:
                    st.error(f"ScraperAPI Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")
