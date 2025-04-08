import os
import json
from transformers import pipeline
from utils.summarize import extract_text_from_pdf, summarize_text_offline

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

# Initialize model
device = "cpu"
print(f"Device set to use {device}")
summarizer = pipeline("summarization", model=config["model_name"], device=-1)

# Process each paper
for filename in os.listdir("papers"):
    if filename.endswith(".pdf"):
        print(f"\n📄 Processing {filename}")
        path = os.path.join("papers", filename)
        text = extract_text_from_pdf(path)
        if not text:
            print(f"❌ PDF not found or empty: {path}")
            continue

        summary = summarize_text_offline(text, summarizer)
        print("\n📝 Summary:\n")
        print(summary)




'''import os
from utils.fetch_paper import fetch_and_download_papers
from utils.summarize import extract_text_from_pdf
from utils.offline_summarizer import summarize_text_offline

# Step 1: Download papers (already handles deduplication)
papers = fetch_and_download_papers(max_results=2)

# Step 2: Loop through each downloaded paper
for paper_filename in os.listdir("papers"):
    if paper_filename.endswith(".pdf"):
        print(f"\n📄 Processing {paper_filename}")
        pdf_path = os.path.join("papers", paper_filename)

        try:
            text = extract_text_from_pdf(pdf_path)
            summary = summarize_text_offline(text)

            print("\n🧠 Summary:\n")
            print(summary[:1500])  # Truncate output for console readability

        except Exception as e:
            print(f"⚠️ Failed to process {paper_filename}: {e}")
'''


'''import os
from utils.fetch_paper import fetch_and_download_papers
from utils.summarize import extract_text_from_pdf, summarize_text_with_gpt

# Step 1: Fetch + download
fetch_and_download_papers(query="natural language processing", max_results=2)

# Step 2: Process each PDF
for filename in os.listdir("papers"):
    if filename.endswith(".pdf"):
        path = os.path.join("papers", filename)
        print(f"\n📄 Processing {filename}")

        text = extract_text_from_pdf(path)
        if not text or len(text) < 1000:
            print("⚠️ Skipping — text too short or unreadable.")
            continue

        summary = summarize_text_with_gpt(text)
        print(f"\n📝 Summary:\n{summary}\n")

'''

'''import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.fetch_paper import fetch_and_download_papers


if __name__ == "__main__":
    papers = fetch_and_download_papers(max_results=2)
    for paper in papers:
        print(f"\n📄 {paper['title']}\n📝 {paper['summary'][:300]}...\n")
'''