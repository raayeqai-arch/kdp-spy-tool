import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

# --- ADVANCED PAGE CONFIG ---
st.set_page_config(page_title="KDP Spy Ultra 2026", layout="wide", page_icon="🚀")

# Hardcoded API Key
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

st.title("🚀 KDP Niche & Keyword Intelligence (Stable v5)")
st.markdown("Equipped with **Smart Browser Rendering** to bypass Amazon.fr blocks.")
st.divider()

# --- INPUT SECTION ---
col1, col2 = st.columns([1, 2])
with col1:
    market = st.selectbox("Marketplace", ["amazon.fr", "amazon.com", "amazon.co.uk"])
with col2:
    query = st.text_input("Enter Niche Keyword:", value="agenda scolaire 2026 2027")

# --- IMPROVED KEYWORD ENGINE ---
def extract_top_keywords(titles):
    stop_words = {'a', 'an', 'the', 'for', 'with', 'and', 'in', 'on', 'of', 'to', 'is', 'de', 'la', 'le', 'et', 'pour', 'des', 'du', 'un', 'une', 'les', 'dans'}
    all_words = []
    for title in titles:
        words = re.findall(r'\w+', title.lower())
        all_words.extend([w for w in words if w not in stop_words and len(w) > 2 and not w.isdigit()])
    return Counter(all_words).most_common(10)

# --- MAIN ENGINE ---
if st.button("🔍 Run Deep Market Analysis"):
    if query:
        # Determining the localized proxy and rendering settings
        proxy_country = 'fr' if 'fr' in market else 'us'
        
        # KEY CHANGE: Added 'render': 'true' and 'wait_for_selector'
        # This makes ScraperAPI act like a real Chrome browser
        payload = {
            'api_key': SCRAPER_API_KEY,
            'url': f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks",
            'country_code': proxy_country,
            'premium': 'true',
            'render': 'true', # Simulate a real browser
            'session_number': '123' # Keeps the session stable
        }
        
        with st.spinner(f'Bypassing {market} security systems... This may take 20 seconds.'):
            try:
                # Using a longer timeout because rendering takes time
                response = requests.get('http://api.scraperapi.com', params=payload, timeout=90)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    # Updated selector for 2026 Amazon layout
                    items = soup.select('div[data-component-type="s-search-result"]')
                    
                    titles = []
                    data_list = []
                    
                    for item in items[:20]:
                        title_tag = item.h2
                        if not title_tag: continue
                        
                        full_title = title_tag.text.strip()
                        titles.append(full_title)
                        
                        price_tag = item.select_one('.a-price .a-offscreen')
                        price = price_tag.text if price_tag else "N/A"
                        
                        asin = item.get('data-asin', 'N/A')

                        data_list.append({
                            "Title": full_title[:65] + "...",
                            "ASIN": asin,
                            "Price": price,
                            "Link": f"https://www.{market}/dp/{asin}"
                        })

                    if data_list:
                        # --- KEYWORDS DASHBOARD ---
                        st.subheader("💡 High-Value Keywords (7 Slots)")
                        top_keywords = extract_top_keywords(titles)
                        kw_cols = st.columns(5)
                        for i, (word, count) in enumerate(top_keywords):
                            kw_cols[i % 5].metric(label=f"Rank {i+1}", value=word, delta=f"{count}x")
                        
                        st.divider()
                        
                        # --- DATA TABLE ---
                        st.subheader("📦 Market Overview")
                        st.dataframe(pd.DataFrame(data_list), use_container_width=True)
                    else:
                        st.error("Parsing failed. Amazon.fr is showing a different layout today. Try again in 5 minutes.")
                else:
                    st.error(f"API Blocked: Status {response.status_code}. Try switching Marketplace.")
            except Exception as e:
                st.error(f"Technical Failure: {e}")
    else:
        st.warning("Please enter a keyword.")
