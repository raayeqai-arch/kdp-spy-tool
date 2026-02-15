import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import io
import re

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Book Architect Pro", layout="wide", page_icon="📖")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stButton>button { background-color: #7f56d9; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .main { background-color: #f9fafb; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: API CONFIG ---
st.sidebar.title("🤖 Model Settings")
gemini_api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.sidebar.warning("Please enter your Gemini API Key to start writing.")

# --- MAIN INTERFACE ---
st.title("📖 AI Book Writer & Publisher")
st.markdown("Generate full-length KDP books (6x9\") using Gemini 1.5 Flash.")

# --- BOOK CONFIGURATION ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("General Settings")
    book_title = st.text_input("Book Title:", value="Je me choisis: 101 Vérités pour te Retrouver")
    author_name = st.text_input("Author Name:", value="Camélia Artémis")
    genre = st.selectbox("Genre:", ["Self-Help", "Educational", "Business", "Health", "Biography"])
    language = st.selectbox("Writing Language:", ["French", "English", "German", "Spanish"])

with col2:
    st.subheader("Structure & Tone")
    chapters_count = st.number_input("Number of Chapters:", min_value=1, max_value=30, value=11)
    writing_tone = st.selectbox("Writing Tone:", ["Professional", "Inspirational", "Academic", "Casual"])
    target_audience = st.radio("Target Audience:", ["Adults", "Teens", "Children"], index=0)

description = st.text_area("Book Description / Themes:", 
    "Toxic relationships, resilience, self-love, and emotional healing.")

# --- GENERATION ENGINE ---
if st.button("🚀 Generate Complete Book Content"):
    if not gemini_api_key:
        st.error("Missing API Key! Please provide it in the sidebar.")
    else:
        full_content = ""
        progress_text = "Writing your book... please wait."
        my_bar = st.progress(0, text=progress_text)
        
        try:
            # Chapter by Chapter Generation to ensure depth and stability
            for i in range(1, int(chapters_count) + 1):
                prompt = (f"Write Chapter {i} of a {genre} book titled '{book_title}'. "
                          f"Language: {language}. Tone: {writing_tone}. Audience: {target_audience}. "
                          f"The themes are: {description}. Make it around 800 words.")
                
                response = model.generate_content(prompt)
                full_content += f"\n\nCHAPTER {i}\n\n" + response.text
                
                # Update progress
                progress = i / int(chapters_count)
                my_bar.progress(progress, text=f"Generated Chapter {i} of {chapters_count}")
            
            st.success("✅ Content Generated Successfully!")
            
            # --- PDF EXPORT (KDP 6x9 Ready) ---
            st.subheader("📦 Export Options")
            
            # PDF Creation Logic
            pdf = FPDF(unit='mm', format=(152.4, 228.6)) # Standard 6x9 inches
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            
            # Title Page
            pdf.set_font("Arial", 'B', 18)
            pdf.cell(0, 20, txt=book_title, ln=True, align='C')
            pdf.set_font("Arial", 'I', 12)
            pdf.cell(0, 10, txt=f"Written by {author_name}", ln=True, align='C')
            pdf.ln(20)
            
            # Content (Cleaning text for Latin-1 compatibility to avoid Empty PDF)
            pdf.set_font("Arial", size=11)
            # FPDF (Standard) only supports Latin-1, we strip non-compatible chars
            safe_text = full_content.encode('latin-1', 'ignore').decode('latin-1')
            pdf.multi_cell(0, 10, txt=safe_text)
            
            # Final PDF generation
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            
            st.download_button(
                label="📥 Download KDP-Ready PDF (6x9)",
                data=pdf_bytes,
                file_name=f"{book_title.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
            
            # Also provide a TXT backup
            st.download_button(
                label="📄 Download Source Text (.txt)",
                data=full_content,
                file_name="book_content.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Technical Error: {e}")

st.sidebar.markdown("---")
st.sidebar.caption("KDP AI Architect v10 | 2026")
