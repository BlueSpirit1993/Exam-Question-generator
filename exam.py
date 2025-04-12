import streamlit as st
import fitz  # PyMuPDF
import zipfile
import io
from openai import OpenAI

# === CONFIG ===
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")  # Replace with your OpenAI key

st.set_page_config(page_title="🧠 Future Exam Question Generator", layout="wide")
st.title("📚 Future Exam Question Generator")
st.write("Upload a `.zip` file containing **past year papers (PDFs)** to generate fresh exam questions using ChatGPT.")

# === Extract text from each PDF ===
def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# === Generate Questions using GPT ===
def generate_questions(text, subject="General", num_questions=5):
    prompt = f"""
You are an experienced exam setter for {subject}. Based on the content below from past year papers, generate {num_questions} original and challenging future exam questions (do not copy). 

Only return the numbered questions.

Content:
{text[:3000]}  # limit to avoid exceeding token limit
"""
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content

# === Upload ZIP ===
uploaded_zip = st.file_uploader("📤 Upload ZIP file of PDFs", type="zip")

if uploaded_zip:
    zip_bytes = io.BytesIO(uploaded_zip.read())
    with zipfile.ZipFile(zip_bytes, "r") as zip_ref:
        pdf_files = [f for f in zip_ref.namelist() if f.endswith(".pdf")]

        if not pdf_files:
            st.error("❌ No PDFs found in the ZIP file.")
        else:
            st.success(f"✅ Found {len(pdf_files)} PDF(s). Processing...")
            all_text = ""

            for file in pdf_files:
                st.write(f"📄 Extracting from: `{file}`")
                pdf_bytes = zip_ref.read(file)
                text = extract_text_from_pdf(pdf_bytes)
                all_text += f"\n=== From {file} ===\n{text}\n"

            # Optionally: let user enter subject & number of questions
            subject = st.text_input("📘 Subject of the papers", value="Math")
            num_questions = st.slider("🔢 Number of questions to generate", 1, 20, 5)

            if st.button("✨ Generate Future Exam Questions"):
                with st.spinner("Generating..."):
                    questions = generate_questions(all_text, subject, num_questions)
                st.markdown("## 🧾 Generated Questions")
                st.text_area("🧠 Questions", questions, height=400)
