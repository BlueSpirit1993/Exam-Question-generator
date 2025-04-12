import os
import PyPDF2
import openai
from openai import OpenAI
import streamlit as st
openai.api_key = st.secrets["openai"]["api_key"]
client = OpenAI(api_key = openai.api_key)
def extract_texts_from_zip(folder_path):
    combined_text = ""
    for root, _, files in os.walk(folder_path):
        for file in files:
            path = os.path.join(root, file)
            if file.endswith(".txt"):
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    combined_text += f.read() + "\n"
            elif file.endswith(".pdf"):
                reader = PyPDF2.PdfReader(path)
                for page in reader.pages:
                    combined_text += page.extract_text() or ""
    return combined_text

def generate_future_questions(text):
    prompt = f"""
You are a senior university exam question setter.

You are given a mix of past exam papers and course notes. Prioritize the **exam papers** when identifying trends and selecting likely future questions. Use the **course notes** only for clarification, not for question prediction.

Here is the input text (mix of papers and notes):\n\n{text[:6000]}\n\n

Your task is to:
1. Analyze the most frequently tested or trending topics based **primarily on exam papers**.
2. Generate **5 to 10 new exam questions likely to appear next year**, ranked by **likelihood** (High, Medium, Low).
3. For each question:
   - Write a concise **model answer**
   - Rate the **likelihood**
   - Add a **short reason** why this question is likely, based on past paper trends

Use this format:
1. **[Question]**  
   - **Answer**: [Model answer]  
   - **Likelihood**: High  
   - **Reason**: [Explanation]

Focus more on real exam trends, not general textbook knowledge.
"""


    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

