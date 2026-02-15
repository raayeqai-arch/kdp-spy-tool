import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="KDP Market Spy Pro", layout="wide", page_icon="📈")

# --- DATA SOURCE CONFIGURATION ---
# Your ScraperAPI Key is embedded directly as requested
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

# --- UI HEADER ---
st.title("📈 KDP Market Research Tool")
st.markdown("This tool bypasses Amazon's blocks to provide real-time niche data.")
st.divider()

# --- INPUT SECTION ---
col1, col2 = st.columns([1, 2])
with col1:
    market = st.selectbox("Select Marketplace", 
                         ["amazon.com", "amazon.fr", "amazon.co.uk", "amazon.de", "amazon.it"])
with col2:
    query = st.text_input("Enter Niche Keyword:", placeholder="e.g., 'Weekly Planner 2026'")

# --- HELPER FUNCTIONS ---
def calculate_estimated_royalty(price_text):
    """Calculates approximate KDP royalty for paperback (60% - printing cost)."""
    try:
        # Extract digits and decimal points only
        clean_price = "".join(filter(lambda x: x.isdigit() or x in ".,", price_text)).replace(',', '.')
        price = float(clean_price)
        royalty = (price * 0.60) - 2.15  # Standard KDP formula for black & white interior
        return f"{max(0, royalty):.2f}"
    except:
        return "N/A"

# --- MAIN ANALYSIS LOGIC ---
if st.button("Run Deep Analysis"):
    if query:
        amazon_search_url = f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks"
        
        # ScraperAPI Payload
        payload = {
            'api_key': SCRAPER_API_KEY,
            'url': amazon_search_url,
            'render': 'false' 
        }
        
        with st.spinner(f'Searching {market} for "{query}"...'):
            try:
                response = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    # Using advanced selectors to find search results
                    items = soup.select('div[data-component-type="s-search-result"]')
                    
                    final_data = []
                    for item in items[:25]:  # Extended to 25 results for better overview
                        # Title & Link
                        title_tag = item.select_one('h2 a span')
                        link_tag = item.select_one('h2 a')
                        
                        if not title_tag: continue
                        
                        title = title_tag.text.strip()
                        asin = item.get('data-asin', 'N/A')
                        full_link = f"https://www.{market}{link_tag['href']}" if link_tag else "#"
                        
                        # Price & Royalty
                        price_tag = item.select_one('.a-price .a-offscreen')
                        price_val = price_tag.text if price_tag else "N/A"
                        royalty = calculate_estimated_royalty(price_val)
                        
                        # Social Proof (Ratings & Reviews)
                        rating_tag = item.select_one('span.a-icon-alt')
                        stars = rating_tag.text.split()[0] if rating_tag else "0"
                        
                        review_tag = item.select_one('span.a-size-base.s-underline-text')
                        reviews = review_tag.text.replace('(', '').replace(')', '').replace(',', '') if review_tag else "0"

                        final_data.append({
                            "Book Title": title[:70] + "...",
                            "ASIN": asin,
                            "Price": price_val,
                            "Est. Royalty": f"{royalty} {market[-2:].upper()}",
                            "Stars": stars,
                            "Reviews": reviews,
                            "Amazon Link": full_link
                        })
                    
                    if final_data:
                        df = pd.DataFrame(final_data)
                        st.success(f"Successfully analyzed {len(final_data)} products.")
                        
                        # Displaying the Data Table
                        st.dataframe(df, use_container_width=True)
                        
                        # Download Button
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Research Data (CSV)",
                            data=csv,
                            file_name=f"kdp_research_{query.replace(' ', '_')}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.error("No books found. Try adjusting your keyword or marketplace.")
                else:
                    st.error(f"Access Denied or API Error. Status Code: {response.status_code}")
                    
            except Exception as e:
                st.error(f"A technical error occurred: {e}")
    else:
        st.warning("Please enter a keyword to begin your research.")

# --- FOOTER ---
st.divider()
st.caption("Developed for Professional KDP Publishers. Data powered by ScraperAPI.")
