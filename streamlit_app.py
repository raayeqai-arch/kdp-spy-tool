import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Page Configuration
st.set_page_config(page_title="KDP Spy Tool Pro", layout="wide")

st.title("🚀 KDP Niche Analyzer")
st.markdown("---")

# Sidebar for Search Settings
st.sidebar.header("Search Settings")
search_query = st.text_input("Enter Niche Keyword (e.g., 'Fitness Journal'):")
market = st.sidebar.selectbox("Marketplace", ["amazon.com", "amazon.co.uk", "amazon.fr"])

if st.button("Analyze Niche"):
    if search_query:
        # Professional Headers to mimic a real browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": f"https://www.{market}/"
        }
        
        url = f"https://www.{market}/s?k={search_query.replace(' ', '+')}&i=stripbooks"
        
        with st.spinner(f'Fetching live data from {market}...'):
            try:
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    # Targeting Amazon's search result containers
                    products = soup.find_all("div", {"data-component-type": "s-search-result"})
                    
                    data_list = []
                    for product in products[:15]:  # Get top 15 results
                        title = product.h2.text.strip() if product.h2 else "N/A"
                        
                        # Extract ASIN
                        asin = product.get('data-asin', 'N/A')
                        
                        # Extract Price
                        price_whole = product.find("span", "a-price-whole")
                        price_fraction = product.find("span", "a-price-fraction")
                        price = f"{price_whole.text}{price_fraction.text}" if price_whole else "N/A"
                        
                        # Extract Rating
                        rating_element = product.find("span", {"class": "a-icon-alt"})
                        rating = rating_element.text.split(" ")[0] if rating_element else "N/A"

                        data_list.append({
                            "Title": title,
                            "ASIN": asin,
                            "Price": price,
                            "Rating": rating,
                            "Link": f"https://www.{market}/dp/{asin}"
                        })

                    if data_list:
                        df = pd.DataFrame(data_list)
                        st.success(f"Found {len(data_list)} results for '{search_query}'")
                        
                        # Visualizing Data
                        st.dataframe(df, use_container_width=True)
                        
                        # Simple Analytics
                        st.subheader("Quick Analysis")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"Marketplace: {market}")
                        with col2:
                            st.info(f"Search Depth: Top 15 Results")
                            
                    else:
                        st.warning("No products found. Amazon might be blocking the request or the niche is too narrow.")
                
                elif response.status_code == 503:
                    st.error("Amazon Service Unavailable (503). They are likely detecting automated traffic.")
                else:
                    st.error(f"Error: Received Status Code {response.status_code}")
                    
            except Exception as e:
                st.error(f"Technical Error: {str(e)}")
    else:
        st.warning("Please enter a keyword to start.")

st.markdown("---")
st.caption("Note: This tool uses basic scraping. For high-volume research, consider integrating a proxy or Rainforest API.")
