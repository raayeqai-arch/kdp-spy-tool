import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# إعداد الصفحة
st.set_page_config(page_title="KDP Auto-Analyzer", layout="wide")

# دمج كود الـ API الخاص بك مباشرة
SCRAPER_API_KEY = "e08bf59c7ece2da93a40bb0608d59f47"

st.title("🚀 KDP Automated Niche Finder")
st.write("الأداة الآن مرتبطة مباشرة بحسابك في ScraperAPI")

# اختيار السوق والكلمة المفتاحية
col1, col2 = st.columns([1, 3])
with col1:
    market = st.selectbox("Marketplace", ["amazon.com", "amazon.fr", "amazon.co.uk"])
with col2:
    query = st.text_input("Enter Niche Keyword:", "")

def get_royalty(price_str):
    try:
        # تنظيف السعر وحساب الربح التقريبي (60% ناقص تكلفة الطباعة)
        p = float(price_str.replace('$', '').replace('€', '').replace('£', '').replace(',', '.'))
        return f"{(p * 0.60) - 2.15:.2f}"
    except:
        return "N/A"

if st.button("Start Deep Analysis"):
    if query:
        # إعداد الرابط عبر ScraperAPI
        payload = {
            'api_key': SCRAPER_API_KEY,
            'url': f"https://www.{market}/s?k={query.replace(' ', '+')}&i=stripbooks"
        }
        
        with st.spinner('Fetching live data...'):
            try:
                # الطلب يمر عبر البروكسي لتجنب الحظر
                response = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    products = soup.find_all("div", {"data-component-type": "s-search-result"})
                    
                    final_data = []
                    for item in products[:15]:
                        title = item.h2.text.strip()[:60] + "..." if item.h2 else "N/A"
                        asin = item.get('data-asin', 'N/A')
                        price_element = item.find("span", "a-offscreen")
                        price = price_element.text if price_element else "N/A"
                        rating = item.find("span", "a-icon-alt").text.split()[0] if item.find("span", "a-icon-alt") else "0"
                        
                        final_data.append({
                            "Book Title": title,
                            "ASIN": asin,
                            "Price": price,
                            "Est. Royalty": f"{get_royalty(price)} {market[-2:]}",
                            "Rating": rating,
                            "Link": f"https://www.{market}/dp/{asin}"
                        })
                    
                    if final_data:
                        df = pd.DataFrame(final_data)
                        st.success(f"Found {len(final_data)} high-quality results!")
                        st.table(df) # عرض النتائج في جدول مرتب
                        
                        # زر تحميل التقرير
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button("📥 Download Excel Report", csv, "kdp_research.csv", "text/csv")
                    else:
                        st.error("No data found. Amazon might have updated its layout.")
                else:
                    st.error(f"Error: {response.status_code}. Please check your ScraperAPI balance.")
            except Exception as e:
                st.error(f"Technical error occurred: {e}")
    else:
        st.warning("Please enter a keyword to search.")

st.markdown("---")
st.caption("Developed for KDP Professional Publishing Analysis")
