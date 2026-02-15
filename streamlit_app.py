import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="KDP Niche & Keyword Spy", layout="wide", page_icon="🔑")

# Hardcoded API Key for seamless access
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

st.title("🔑 KDP Niche & Keyword Intelligence")
st.markdown("Analyze competitor data and extract the best keywords for your 7 backend slots.")
st.divider()

# --- INPUT SECTION ---
col1, col2 = st.columns([1, 2])
with col1:
    market = st.selectbox("Select Marketplace", ["amazon.fr", "amazon.com", "amazon.co.uk", "amazon.de"])
with col2:
    query = st.text_input("Enter Niche Keyword:", value="agenda scolaire 2026 2027")

# --- KEYWORD EXTRACTION ENGINE ---
def extract_top_keywords(titles):
    # Common stop words to filter out (English & French)
    stop_words = {
        'a', 'an', 'the', 'for', 'with', 'and', 'in', 'on', 'of', 'to', 'is', 'it', 'that',
        'de', 'la', 'le', 'et', 'pour', 'des', 'du', 'un', 'une', 'les', 'dans', 'par'
    }
    all_words = []
    for title in titles:
        # Extract alphanumeric words and convert to lowercase
        words = re.findall(r'\w+', title.lower())
        all_words.extend([w for w in words if w not in stop_words and len(w) > 2 and not w.isdigit()])
    
    return Counter(all_words).most_common(10)

# --- MAIN ANALYSIS PROCESS ---
if st.button("🚀 Run Deep Analysis"):
    if query:
        # Determine localization for proxy
        proxy_country = 'fr' if 'fr' in market else 'us'
        
        payload = {
            'api_key': SCRAPER_API_KEY,
            'url': f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks",
            'country_code': proxy_country,
            'premium': 'true'
        }
        
        with st.spinner(f'Analyzing {market} market...'):
            try:
                response = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    items = soup.select('div[data-component-type="s-search-result"]')
                    
                    titles = []
                    data_list = []
                    
                    for item in items[:25]: # Analyze top 25 results
                        title_tag = item.h2
                        if not title_tag: continue
                        
                        full_title = title_tag.text.strip()
                        titles.append(full_title)
                        
                        price_tag = item.select_one('.a-price .a-offscreen')
                        price = price_tag.text if price_tag else "N/A"
                        
                        asin = item.get('data-asin', 'N/A')
                        rating = item.select_one('span.a-icon-alt').text.split()[0] if item.select_one('span.a-icon-alt') else "0"

                        data_list.append({
                            "Title": full_title[:75] + "...",
                            "ASIN": asin,
                            "Price": price,
                            "Rating": rating,
                            "Link": f"https://www.{market}/dp/{asin}"
                        })

                    if data_list:
                        # --- KEYWORDS DASHBOARD ---
                        st.subheader("💡 Strategic Keywords for your 7 Slots")
                        st.write("These keywords appear most frequently in top-selling titles:")
                        
                        top_keywords = extract_top_keywords(titles)
                        kw_cols = st.columns(5)
                        for i, (word, count) in enumerate(top_keywords):
                            kw_cols[i % 5].metric(label=f"Keyword #{i+1}", value=word, delta=f"{count}x used")
                        
                        st.divider()
                        
                        # --- COMPETITOR DATA TABLE ---
                        st.subheader("📦 Competitor Market Data")
                        df = pd.DataFrame(data_list)
                        st.dataframe(df, use_container_width=True)
                        
                        # --- DOWNLOAD SECTION ---
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Research Report (CSV)",
                            data=csv,
                            file_name=f"KDP_Research_{query}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.error("Could not find results. Try a broader search term.")
                else:
                    st.error(f"API Error: Status {response.status_code}")
            except Exception as e:
                st.error(f"Technical Failure: {e}")
    else:
        st.warning("Please enter a keyword to start.")

st.divider()
st.caption("KDP Professional Research Suite | Powered by ScraperAPI")
