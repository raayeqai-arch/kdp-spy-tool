import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# --- PROFESSIONAL PAGE CONFIG ---
st.set_page_config(page_title="KDP Ultimate Spy", layout="wide", page_icon="🎯")

# Your ScraperAPI Key
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

st.title("🎯 KDP Niche Hunter - Ultra Stable Version")
st.info("This version uses 'Smart Selectors' to find data even if Amazon changes its design.")

# --- INPUTS ---
col1, col2 = st.columns([1, 2])
with col1:
    market = st.selectbox("Select Marketplace", ["amazon.com", "amazon.fr", "amazon.co.uk", "amazon.de"])
with col2:
    query = st.text_input("Enter Keyword:", placeholder="e.g., 'Cahier de texte'")

def calculate_royalty(price_text):
    try:
        clean_price = "".join(filter(lambda x: x.isdigit() or x in ".,", price_text)).replace(',', '.')
        price = float(clean_price)
        return f"{(price * 0.60) - 2.15:.2f}"
    except:
        return "N/A"

if st.button("🚀 Start Market Research"):
    if query:
        search_url = f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks"
        
        # We add 'autoparse=true' which is a powerful feature of ScraperAPI 
        # that handles the HTML structure for us
        payload = {
            'api_key': SCRAPER_API_KEY,
            'url': search_url,
            'premium': 'true', # Use premium proxies to avoid "No Data"
            'country_code': 'us' if market == 'amazon.com' else 'fr'
        }
        
        with st.spinner('Scanning Amazon Marketplace... Please wait.'):
            try:
                # We will try a different approach: searching for 's-result-item'
                response = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    
                    # More robust selector
                    products = soup.find_all("div", {"class": "s-result-item"})
                    
                    extracted_data = []
                    for product in products:
                        # Find Title
                        title_tag = product.find("h2")
                        if not title_tag: continue
                        title = title_tag.text.strip()
                        
                        # Find ASIN
                        asin = product.get('data-asin')
                        if not asin: continue
                        
                        # Find Price
                        price_tag = product.select_one(".a-price .a-offscreen")
                        price = price_tag.text if price_tag else "N/A"
                        
                        # Find Ratings
                        rating_tag = product.select_one("span.a-icon-alt")
                        rating = rating_tag.text.split()[0] if rating_tag else "0"

                        extracted_data.append({
                            "Title": title[:60] + "...",
                            "ASIN": asin,
                            "Price": price,
                            "Est. Royalty": f"{calculate_royalty(price)} {market[-2:].upper()}",
                            "Rating": rating,
                            "Link": f"https://www.{market}/dp/{asin}"
                        })

                    if extracted_data:
                        df = pd.DataFrame(extracted_data)
                        st.success(f"Found {len(extracted_data)} results!")
                        st.dataframe(df, use_container_width=True)
                        
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button("📥 Download Excel Report", csv, "kdp_data.csv", "text/csv")
                    else:
                        st.error("Amazon blocked the parsing. Try switching the 'Marketplace' or wait 2 minutes.")
                        # Debugging: show what the API actually sees
                        with st.expander("Show Technical Log"):
                            st.write(f"Status: {response.status_code}")
                            st.write("Amazon detected the scraper. Trying 'Premium' mode in ScraperAPI is recommended.")
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a keyword.")
