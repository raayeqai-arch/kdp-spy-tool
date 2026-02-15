import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Page Config
st.set_page_config(page_title="KDP Spy Tool Pro (ScraperAPI)", layout="wide")

st.title("🚀 KDP Niche Analyzer - ScraperAPI Edition")
st.markdown("---")

# Sidebar Configuration
st.sidebar.header("Setup")
api_key = st.sidebar.text_input("Enter ScraperAPI Key:", type="password")
market = st.sidebar.selectbox("Marketplace", ["amazon.com", "amazon.fr", "amazon.co.uk"])
search_query = st.text_input("Enter Niche Keyword (e.g., 'Cahier de texte'):")

if st.button("Deep Analysis"):
    if not api_key:
        st.warning("Please enter your ScraperAPI Key in the sidebar.")
    elif not search_query:
        st.warning("Please enter a keyword.")
    else:
        # Constructing the ScraperAPI Proxy URL
        # This will route your request through their professional proxies
        payload = { 
            'api_key': api_key, 
            'url': f"https://www.{market}/s?k={search_query.replace(' ', '+')}&i=stripbooks" 
        }
        
        with st.spinner('ScraperAPI is bypassing Amazon protection...'):
            try:
                response = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    products = soup.find_all("div", {"data-component-type": "s-search-result"})
                    
                    data_list = []
                    for product in products[:20]: # Fetching top 20 results
                        title = product.h2.text.strip() if product.h2 else "N/A"
                        asin = product.get('data-asin', 'N/A')
                        
                        # Price
                        price_element = product.find("span", "a-offscreen")
                        price = price_element.text if price_element else "N/A"
                        
                        # Ratings
                        rating_element = product.find("span", "a-icon-alt")
                        rating = rating_element.text.split(" ")[0] if rating_element else "0"
                        
                        # Reviews count
                        review_count = product.find("span", {"class": "a-size-base", "dir": "auto"})
                        reviews = review_count.text if review_count else "0"

                        data_list.append({
                            "Title": title,
                            "ASIN": asin,
                            "Price": price,
                            "Rating": rating,
                            "Reviews": reviews,
                            "Link": f"https://www.{market}/dp/{asin}"
                        })

                    if data_list:
                        df = pd.DataFrame(data_list)
                        st.success(f"Successfully analyzed {len(data_list)} books for '{search_query}'")
                        st.dataframe(df, use_container_width=True)
                        
                        # CSV Download
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button("📥 Download Research Report", csv, "kdp_market_research.csv", "text/csv")
                    else:
                        st.error("Results found but couldn't be parsed. Try a different keyword.")
                else:
                    st.error(f"ScraperAPI Error: Status {response.status_code}. Check your API Key.")
            except Exception as e:
                st.error(f"Technical Error: {e}")

st.markdown("---")
st.info("💡 **Tip:** Use your ScraperAPI key from your dashboard to bypass 503 errors forever.")
