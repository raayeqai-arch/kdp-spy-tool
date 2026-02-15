import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import io

# --- CONFIG ---
st.set_page_config(page_title="Gemini Book Publisher", layout="wide")

# اطلب من المستخدم إدخال مفتاح Gemini API
gemini_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if gemini_key:
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

st.title("📖 Gemini AI Book Writer (KDP Ready)")
st.info("هذا الموديل يستخدم Gemini لتوليد محتوى كامل وتصديره بصيغة PDF حقيقية.")

# --- UI SETTINGS (Based on your shared images) ---
col1, col2 = st.columns(2)
with col1:
    genre = st.selectbox("Genre", ["Self-Help", "Educational", "Fantasy", "Business"])
    title = st.text_input("Book Title:", value="Je me choisis: 101 Vérités")
    author = st.text_input("Author Name:", value="Camélia Artémis")

with col2:
    chapters_count = st.number_input("Number of Chapters:", 1, 20, 11)
    target_audience = st.radio("Target Audience:", ["Adults", "Teens", "Children"], index=0)

description = st.text_area("Brief Description/Theme:", "les relations toxiques, la résilience, le développement personnel")

# --- GENERATION LOGIC ---
if st.button("🚀 Generate Full Book with Gemini"):
    if not gemini_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    else:
        full_text = ""
        progress_bar = st.progress(0)
        
        try:
            with st.spinner("Gemini is writing your book... Please wait."):
                for i in range(1, chapters_count + 1):
                    # إنشاء طلب لكل فصل لضمان الدقة
                    prompt = f"Write Chapter {i} of a {genre} book titled '{title}'. Theme: {description}. Tone: Professional. Language: French. Length: 800 words."
                    response = model.generate_content(prompt)
                    
                    chapter_content = response.text
                    full_text += f"\n\n--- Chapter {i} ---\n\n" + chapter_content
                    
                    # تحديث شريط التقدم
                    progress_bar.progress(i / chapters_count)
            
            st.success("Book content generated successfully!")
            
            # --- PDF CREATION (FIXED) ---
            pdf = FPDF(format='letter') # أو استخدم (152.4, 228.6) لـ 6x9 inches
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            
            # إضافة العنوان
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt=title, ln=True, align='C')
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"By {author}", ln=True, align='C')
            
            # إضافة المحتوى (تنظيف النص من الرموز غير المدعومة في FPDF)
            pdf.ln(10)
            clean_text = full_text.encode('latin-1', 'ignore').decode('latin-1')
            pdf.multi_cell(0, 10, txt=clean_text)
            
            # تصدير الملف كـ Bytes لضمان عدم تلفه
            pdf_output = pdf.output(dest='S').encode('latin-1')
            
            st.download_button(
                label="📥 Download KDP-ready PDF",
                data=pdf_output,
                file_name="gemini_kdp_book.pdf",
                mime="application/pdf"
            )
            
        except Exception as e:
            st.error(f"Error during generation: {e}")

st.sidebar.markdown("---")
st.sidebar.caption("Partner Suite v10 | Powered by Gemini 1.5")
