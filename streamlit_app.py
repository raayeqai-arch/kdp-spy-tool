import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- ADVANCED PAGE CONFIG ---
st.set_page_config(page_title="KDP Global Spy v4", layout="wide", page_icon="🌍")

# Your ScraperAPI Key
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

st.title("🌍 KDP Global Niche Hunter")
st.write("Specialized in Multi-Market Analysis (USA, France, UK, Germany)")

# --- INPUT SECTION ---
col1, col2 = st.columns([1, 2])
with col1:
    market = st.selectbox("Select Marketplace", ["amazon.fr", "amazon.com", "amazon.co.uk", "amazon.de"])
with col2:
    query = st.text_input("Enter Niche Keyword (e.g., 'agenda', 'cahier de texte'):", placeholder="agenda")

def get_royalty(price_text):
    try:
        clean = "".join(filter(lambda x: x.isdigit() or x in ".,", price_text)).replace(',', '.')
        price = float(clean)
        # KDP Standard Royalty: (60% - Printing 2.15)
        return f"{(price * 0.60) - 2.15:.2f}"
    except:
        return "N/A"

if st.button("🚀 Start Global Research"):
    if query:
        # Determine the proxy country based on the marketplace
        country_code = 'fr' if 'amazon.fr' in market else ('us' if 'amazon.com' in market else 'gb')
        
        target_url = f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks"
        
        # ScraperAPI Professional Payload
        payload = {
            'api_key': SCRAPER_API_KEY,
            'url': target_url,
            'country_code': country_code, # IMPORTANT: Tells ScraperAPI to use local proxies
            'render': 'false',
            'premium': 'true' # Using premium proxies to bypass strict EU blocks
        }
        
        with st.spinner(f'Accessing {market} using local {country_code.upper()} proxies...'):
            try:
                response = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    
                    # New resilient search items selector
                    products = soup.select('div[data-component-type="s-search-result"]')
                    
                    market_data = []
                    for item in products[:20]:
                        title_tag = item.h2
                        if not title_tag: continue
                        
                        asin = item.get('data-asin', 'N/A')
                        price_tag = item.select_one('.a-price .a-offscreen')
                        price = price_tag.text if price_tag else "N/A"
                        
                        rating_tag = item.select_one('span.a-icon-alt')
                        stars = rating_tag.text.split()[0] if rating_tag else "0"
                        
                        # Extra logic for France prices (sometimes uses commas)
                        royalty = get_royalty(price)

                        market_data.append({
                            "Title": title_tag.text.strip()[:65] + "...",
                            "ASIN": asin,
                            "Price": price,
                            "Est. Profit": f"{royalty} {market[-2:].upper()}",
                            "Ratings": stars,
                            "Link": f"https://www.{market}/dp/{asin}"
                        })

                    if market_data:
                        st.success(f"Successfully unlocked {market} data!")
                        st.table(pd.DataFrame(market_data))
                    else:
                        st.error("Still blocked. Try a different keyword or check your ScraperAPI credits.")
                else:
                    st.error(f"Market Blocked: Status {response.status_code}")
            except Exception as e:
                st.error(f"Technical Error: {e}")
    else:
        st.warning("Please enter a keyword.")
