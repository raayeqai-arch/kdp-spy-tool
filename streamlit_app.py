import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="KDP Global Spy Pro", layout="wide", page_icon="🌍")
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

st.title("🌍 KDP Global Niche Hunter (Advanced FR Unblock)")
st.info("Specialized logic for Amazon.fr & Amazon.com bypass.")

# --- INPUTS ---
col1, col2 = st.columns([1, 2])
with col1:
    market = st.selectbox("Target Market", ["amazon.fr", "amazon.com", "amazon.co.uk"])
with col2:
    query = st.text_input("Niche Keyword:", placeholder="e.g., 'Agenda Scolaire'")

# --- SEASONAL STRATEGY ---
def get_kdp_advice(kw):
    curr_month = datetime.now().month
    if "agenda" in kw.lower() or "planner" in kw.lower():
        if 2 <= curr_month <= 5:
            return "🛠️ **Preparation Phase:** Design and upload now for the summer back-to-school rush."
        return "📈 **Observation Phase:** Monitor competition and adjust keywords."
    return "📊 **Regular Niche:** Consistent demand. Focus on design quality."

# --- MAIN ENGINE ---
if st.button("🚀 Analyze Market"):
    if query:
        st.info(get_kdp_advice(query))
        
        # Determine Proxy Country
        proxy_country = 'fr' if 'fr' in market else 'us'
        
        # ScraperAPI with Advanced Parameters
        payload = {
            'api_key': SCRAPER_API_KEY,
            'url': f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks",
            'country_code': proxy_country,
            'premium': 'true', # Using premium is mandatory for Amazon.fr
            'device_type': 'desktop',
            'keep_headers': 'true' # Keeps our custom language headers
        }
        
        # Specific headers for France to fool Amazon's regional check
        headers = {
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": f"https://www.{market}/"
        }

        with st.spinner(f'Unlocking {market} via {proxy_country.upper()} Premium Tunnel...'):
            try:
                response = requests.get('http://api.scraperapi.com', params=payload, headers=headers, timeout=60)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    # Targeting the exact result items
                    items = soup.select('div[data-component-type="s-search-result"]')
                    
                    data_list = []
                    for item in items[:20]:
                        title_tag = item.h2
                        if not title_tag: continue
                        
                        asin = item.get('data-asin', 'N/A')
                        price_tag = item.select_one('.a-price .a-offscreen')
                        price = price_tag.text if price_tag else "N/A"
                        
                        rating_tag = item.select_one('span.a-icon-alt')
                        stars = rating_tag.text.split()[0] if rating_tag else "0"

                        data_list.append({
                            "Title": title_tag.text.strip()[:65] + "...",
                            "ASIN": asin,
                            "Price": price,
                            "Stars": stars,
                            "Link": f"https://www.{market}/dp/{asin}"
                        })

                    if data_list:
                        st.success(f"Success! {len(data_list)} books found in {market}.")
                        st.dataframe(pd.DataFrame(data_list), use_container_width=True)
                    else:
                        st.error("Amazon France returned a custom layout. Try a generic keyword like 'agenda' to test.")
                else:
                    st.error(f"Blocked (Status {response.status_code}). ScraperAPI credits might be low or Amazon is rotating IPs.")
            except Exception as e:
                st.error(f"Technical Error: {e}")
