from transformers import pipeline
from typing import Optional

class PaperSummarizer:
    def __init__(self):
        self.model = None
        
    def load_model(self):
        """Lazy load the summarization model"""
        if self.model is None:
            self.model = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1  # Use CPU
            )
    
    def summarize(self, text: str) -> Optional[str]:
        """Generate a concise summary"""
        if not text.strip():
            return None
            
        try:
            self.load_model()
            return self.model(
                text,
                max_length=150,
                min_length=30,
                do_sample=False
            )[0]['summary_text']
        except Exception as e:
            print(f"Summarization error: {e}")
            return None

'''from utils.offline_summarizer import chunk_text
from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text_offline(text, default_max=200, default_min=100):
    chunks = chunk_text(text)
    summaries = []

    for chunk in chunks:
        input_length = len(chunk.split())
        max_len = min(default_max, int(input_length * 0.6))  # Keep summary 60% or less
        min_len = min(default_min, int(input_length * 0.3))

        # Fallback in case input is very short
        max_len = max(max_len, 30)
        min_len = max(min_len, 10)

        summary = summarizer(
            chunk,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )
        summaries.append(summary[0]['summary_text'])

    full_summary = "\n\n".join(summaries)
    return full_summary'''




'''# utils/summarizer.py
from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def chunk_text(text, max_chunk_tokens=1024):
    sentences = text.split('. ')
    current_chunk = ""
    chunks = []

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_tokens:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def summarize_text_offline(text, max_length=200, min_length=100):
    chunks = chunk_text(text)
    summaries = []

    for chunk in chunks:
        summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
        summaries.append(summary[0]['summary_text'])

    full_summary = "\n\n".join(summaries)
    return full_summary
'''



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