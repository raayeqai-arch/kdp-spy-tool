import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="KDP AI Book Architect v12", layout="wide", page_icon="📖")

# --- SIDEBAR API CONFIG ---
st.sidebar.title("🤖 Gemini Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # تم تغيير تعريف الموديل لتجنب خطأ 404
        model = genai.GenerativeModel('models/gemini-1.5-flash')
    except Exception as e:
        st.sidebar.error(f"Setup Error: {e}")
else:
    st.sidebar.warning("Please provide an API Key.")

st.title("📖 KDP AI Book Architect (Gemini Powered)")
st.markdown("Generate professional 6x9\" KDP books. Optimized for French & English.")

# --- BOOK SETTINGS ---
col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Book Title:", value="Je me choisis: 101 Vérités")
    author = st.text_input("Author:", value="Camélia Artémis")
    lang = st.selectbox("Language:", ["French", "English", "German"])
with col2:
    chapters = st.number_input("Chapters:", 1, 20, 10)
    genre = st.selectbox("Genre:", ["Self-Help", "Educational", "Business"])

description = st.text_area("Themes:", "resilience, self-love, and healing.")

# --- GENERATION ---
if st.button("🚀 Generate & Build PDF"):
    if not api_key:
        st.error("Missing API Key!")
    else:
        full_text = ""
        progress_bar = st.progress(0)
        
        try:
            with st.spinner("Gemini is writing the chapters..."):
                for i in range(1, chapters + 1):
                    # طلب مفصل لضمان جودة المحتوى
                    prompt = f"Write Chapter {i} of a {genre} book titled '{title}'. Topic: {description}. Language: {lang}. Professional tone. 800 words."
                    response = model.generate_content(prompt)
                    
                    full_text += f"\n\n--- CHAPTER {i} ---\n\n" + response.text
                    progress_bar.progress(i / chapters)
            
            st.success("✅ Content Generated!")

            # --- PDF GENERATION (ULTRA STABLE) ---
            # مقاس KDP العالمي 6x9 إنش
            pdf = FPDF(unit='mm', format=(152.4, 228.6)) 
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            
            # استبدال الرموز غير المدعومة لتجنب الملف الفارغ
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 20, txt=title.encode('latin-1', 'replace').decode('latin-1'), ln=True, align='C')
            
            pdf.set_font("Arial", size=11)
            # تنظيف النص بالكامل قبل وضعه في الـ PDF
            clean_content = full_text.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, txt=clean_content)

            # تحويل الملف إلى Bytes لضمان سلامة التحميل
            pdf_output = pdf.output(dest='S').encode('latin-1')
            
            st.download_button(
                label="📥 Download 6x9\" KDP PDF",
                data=pdf_output,
                file_name="kdp_book_final.pdf",
                mime="application/pdf"
            )
            
        except Exception as e:
            # رسالة خطأ ذكية تخبرك بالسبب (هل هو الموديل أم الـ API)
            st.error(f"Error: {str(e)}")
