import streamlit as st
import pandas as pd
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Book Writer Pro", layout="wide", page_icon="📖")

# --- CUSTOM CSS (To Match your Image) ---
st.markdown("""
    <style>
    .genre-card { background: white; padding: 15px; border-radius: 10px; border: 1px solid #ddd; text-align: center; transition: 0.3s; }
    .genre-card:hover { border-color: #7f56d9; background: #f9f5ff; }
    .main-button { background-color: #7f56d9; color: white; border-radius: 8px; width: 100%; height: 3em; font-weight: bold; }
    .batch-section { background-color: #f6fef9; border: 1px solid #6ce9a6; padding: 20px; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📖 AI Book Writer")
st.markdown("Generate complete books using AI. Perfect for fiction, non-fiction, guides, and more.")

# --- SECTION 1: RANDOM GENERATOR ---
with st.expander("🎲 Random Book Generator", expanded=False):
    st.write("Let AI create a complete book idea for you!")
    theme_input = st.text_input("Theme (Optional)", placeholder="e.g., 'space adventure'...")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("✨ Generate from Theme"):
            st.success("Title: The Echoes of Mars | Genre: Sci-Fi | Plot: A lost colony discovers an ancient signal.")
    with col_r2:
        if st.button("🎲 Fully Random"):
            st.info("Title: The Silent Chef | Genre: Mystery | Plot: A gourmet murder at a silent retreat.")

# --- SECTION 2: BATCH MODE ---
st.markdown('<div class="batch-section">', unsafe_allow_html=True)
st.subheader("📚 Batch Book Generator")
show_batch = st.checkbox("Show Batch Mode")
if show_batch:
    num_books = st.number_input("How many books to generate?", 1, 10, 3)
    for i in range(int(num_books)):
        st.text_input(f"Book Title {i+1} *", key=f"title_{i}")
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- SECTION 3: BOOK SETTINGS (The Core) ---
st.subheader("Book Settings")
col_s1, col_s2 = st.columns([2, 1])

with col_s1:
    genre = st.selectbox("Genre *", [
        "Children's Adventure", "Children's Educational", "Romance", 
        "Mystery", "Fantasy", "Science Fiction", "Self-Help", "How-To Guide"
    ])
    
    book_title = st.text_input("Book Title (Optional - AI will generate if left blank)")
    author = st.text_input("Author Name (Optional)", value="Anonymous")
    
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        chapters = st.number_input("Number of Chapters *", 1, 50, 10)
    with c_col2:
        words_per = st.number_input("Words per Chapter *", 100, 5000, 800)
    
    total_words = chapters * words_per
    st.caption(f"Total Book: ~{total_words:,} words ({int(total_words/250)} pages)")

    audience = st.radio("Target Audience *", ["Ages 3-7", "Ages 8-12", "Teens", "Adults"], horizontal=True)
    tone = st.selectbox("Writing Tone *", ["Professional", "Casual", "Playful", "Inspirational"])
    
    description = st.text_area("Book Description (Optional)")
    if st.button("🪄 AI Generate Description"):
        st.write("Generating a professional description based on your title...")

with col_s2:
    st.subheader("Progress")
    st.info("Configure settings and click generate.")
    
    st.subheader("🤖 AI Model *")
    model = st.radio("Choose Model", ["GPT-4o Mini (Recommended)", "GPT-4o (Premium)"])
    
    st.subheader("📦 Export Formats")
    formats = st.multiselect("Select Formats", ["PDF (KDP-ready 6x9\")", "EPUB", "MOBI", "KPF"])

# --- GENERATE ACTION ---
if st.button("🚀 Generate Book", use_container_width=True):
    with st.status("Generating Book Content...", expanded=True) as status:
        st.write("Generating Chapter 1: The Beginning...")
        st.progress(10)
        # Here you would call your OpenAI/Anthropic API
        st.write("Generating Chapter 2: The Rising Conflict...")
        st.progress(25)
        status.update(label="Book Generation Complete!", state="complete", expanded=False)
    
    st.balloons()
    st.success("Your book is ready for download!")
    st.download_button("📥 Download PDF (6x9\")", "Book Content Here", file_name="kdp_book.pdf")
