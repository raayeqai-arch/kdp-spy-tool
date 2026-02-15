import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import time

# Page Configuration
st.set_page_config(page_title="KDP Spy Tool Pro v2", layout="wide")

st.title("🛡️ KDP Niche Analyzer (Anti-Block Version)")
st.markdown("---")

# User-Agent List to avoid blocking
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
]

# Sidebar
st.sidebar.header("Search Parameters")
market = st.sidebar.selectbox("Select Marketplace", ["amazon.com", "amazon.fr", "amazon.co.uk"])
results_limit = st.sidebar.slider("Number of Results", 5, 20, 10)

search_query = st.text_input("Enter Niche Keyword:")

def get_amazon_data(query, marketplace):
    url = f"https://www.{marketplace}/s?k={query.replace(' ', '+')}&i=stripbooks"
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.5",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }
    
    try:
        # Adding a small random delay to mimic human behavior
        time.sleep(random.uniform(1.5, 3.0))
        response = requests.get(url, headers=headers, timeout=20)
        return response
    except Exception as e:
        return None

if st.button("Analyze Niche"):
    if search_query:
        with st.spinner(f'Searching {market}... Please wait.'):
            response = get_amazon_data(search_query, market)
            
            if response and response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                products = soup.find_all("div", {"data-component-type": "s-search-result"})
                
                data_list = []
                for product in products[:results_limit]:
                    title = product.h2.text.strip() if product.h2 else "N/A"
                    asin = product.get('data-asin', 'N/A')
                    
                    # Price Extraction
                    price_element = product.find("span", "a-offscreen")
                    price = price_element.text if price_element else "N/A"
                    
                    # Ratings
                    rating_element = product.find("span", "a-icon-alt")
                    rating = rating_element.text.split(" ")[0] if rating_element else "0"
                    
                    # Competition Logic (Score)
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
                    st.success(f"Successfully analyzed {len(data_list)} items!")
                    
                    # Displaying results in a professional table
                    st.dataframe(df, use_container_width=True)
                    
                    # Export Data Button
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Download Results as CSV", csv, "kdp_research.csv", "text/csv")
                else:
                    st.error("Amazon returned a blank page. They might be suspicious. Try again in 5 minutes.")
            
            elif response and response.status_code == 503:
                st.error("Blocked by Amazon (503). Changing 'User-Agent' and waiting 2 minutes is recommended.")
            else:
                st.error("Connection failed. Check your internet or try a different keyword.")
    else:
        st.warning("Please enter a keyword.")

st.markdown("---")
st.info("💡 **Pro Tip:** If you get blocked frequently, try searching for less common keywords or reduce the search frequency.")
