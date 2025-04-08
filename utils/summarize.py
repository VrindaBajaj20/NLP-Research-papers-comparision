import re
import os
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        return ""
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text.strip()

def chunk_text_by_sentences(text, max_words=300):
    # Regex-based sentence splitter
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    current_length = 0

    for sentence in sentences:
        word_count = len(sentence.split())
        if current_length + word_count <= max_words:
            current_chunk += sentence + " "
            current_length += word_count
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
            current_length = word_count

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def summarize_text_offline(text, summarizer):
    chunks = chunk_text_by_sentences(text, max_words=300)
    all_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        summary = summarizer(chunk, max_length=200, min_length=30, do_sample=False)[0]["summary_text"]
        all_summaries.append(summary)
    return "\n".join(all_summaries)






'''from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text

'''


'''import os
from dotenv import load_dotenv
import fitz  # PyMuPDF
from openai import OpenAI

# Load the .env variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def summarize_text_with_gpt(text, model="gpt-3.5-turbo", max_tokens=1000):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert at reading and summarizing scientific papers."},
            {"role": "user", "content": f"Summarize the following research paper in 100-200 words:\n\n{text}"}
        ],
        max_tokens=max_tokens,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()
'''