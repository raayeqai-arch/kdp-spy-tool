import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="KDP AI Book Architect", layout="wide", page_icon="📖")

# --- SIDEBAR API CONFIG ---
st.sidebar.title("🤖 Gemini Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.sidebar.warning("Please provide an API Key to enable writing.")

st.title("📖 KDP AI Book Architect (Gemini Powered)")
st.markdown("Generate professional 6x9\" KDP books with real content.")

# --- BOOK SETTINGS ---
col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Book Title:", value="Healing Emotional Wounds")
    author = st.text_input("Author:", value="Anonymous")
    lang = st.selectbox("Language:", ["French", "English", "German"])
with col2:
    chapters = st.number_input("Chapters:", 1, 20, 10)
    genre = st.selectbox("Genre:", ["Self-Help", "Educational", "Business"])

description = st.text_area("What is this book about?", "Recovery from toxic relationships and self-love.")

# --- GENERATION PROCESS ---
if st.button("🚀 Generate & Build PDF"):
    if not api_key:
        st.error("Missing Gemini API Key!")
    else:
        full_text = ""
        progress_bar = st.progress(0)
        
        try:
            with st.spinner("Gemini is writing... This might take a minute."):
                for i in range(1, chapters + 1):
                    prompt = f"Write Chapter {i} of a {genre} book titled '{title}'. Topic: {description}. Language: {lang}. Write 700 words."
                    response = model.generate_content(prompt)
                    
                    chapter_data = f"\n\n--- CHAPTER {i} ---\n\n" + response.text
                    full_text += chapter_data
                    progress_bar.progress(i / chapters)
            
            st.success("✅ Writing Complete!")

            # --- PDF GENERATION (STABLE) ---
            pdf = FPDF(unit='mm', format=(152.4, 228.6)) # Standard 6x9"
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            
            # Title Page
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 20, txt=title, ln=True, align='C')
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, txt=f"By {author}", ln=True, align='C')
            pdf.ln(20)

            # Body Content (Cleaning for PDF compatibility)
            pdf.set_font("Arial", size=11)
            # We use 'latin-1' replace to avoid 'empty PDF' errors with special characters
            clean_content = full_text.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, txt=clean_content)

            # Binary Output for Streamlit
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            
            st.download_button(
                label="📥 Download 6x9\" KDP PDF",
                data=pdf_bytes,
                file_name="kdp_generated_book.pdf",
                mime="application/pdf"
            )
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.sidebar.markdown("---")
st.sidebar.caption("KDP AI Suite v11 | Gemini Engine")
