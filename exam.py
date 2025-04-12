import streamlit as st
import zipfile
import os
from utils import extract_texts_from_zip, generate_future_questions

st.set_page_config(page_title="Future Question Generator", layout="wide")

st.title("🧠 Future-Year Question Generator")
st.markdown("Upload a `.zip` of past year questions and generate possible future questions.")

uploaded_file = st.file_uploader("Upload a .zip file of question papers", type="zip")

if uploaded_file:
    with open("uploaded.zip", "wb") as f:
        f.write(uploaded_file.read())

    with zipfile.ZipFile("anl.zip", "r") as zip_ref:
        zip_ref.extractall("extracted_papers")

    all_text = extract_texts_from_zip("extracted_papers")
    st.success("Files extracted and content loaded!")

    if st.button("✨ Generate Future Questions"):
        with st.spinner("Generating..."):
            future_questions = generate_future_questions(all_text)
        st.subheader("🔮 Future-Year Style Questions")
        st.write(future_questions)
