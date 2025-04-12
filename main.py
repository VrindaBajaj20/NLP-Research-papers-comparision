import gradio as gr
from utils.fetch_paper import PaperFetcher
from extract_text import extract_text_from_pdf
from utils.offline_summarizer import PaperSummarizer
from rank_display import rank_and_display
import arxiv
import os

# Initialize components
fetcher = PaperFetcher()
summarizer = PaperSummarizer()

def format_results(papers: list) -> str:
    """Format results as markdown with proper error handling"""
    if not papers:
        return "## ⚠️ No valid papers found"
    
    output = ["## 📚 Search Results"]
    
    for i, paper in enumerate(papers, 1):
        output.append(f"""
### #{i}: {paper.get('title', 'Untitled')}
**Authors:** {', '.join(paper.get('authors', ['Unknown'])[:3])}
**Published:** {paper.get('published', 'Unknown date')}
**Categories:** {', '.join(paper.get('categories', ['Unknown'])[:3])}

**🔑 Keywords:** {paper.get('Keywords', 'None')}

**📝 Summary:**  
{paper.get('summary', 'No summary available')}

[PDF]({paper.get('pdf_url', '#')}) | [arXiv]({paper.get('arxiv_url', '#')})
""")
    
    return "\n".join(output)

def search_and_summarize(
    topic: str,
    max_results: int = 5,
    recent_days: int = 365,
    sort_by: str = "Relevance"
) -> str:
    """Main processing pipeline"""
    if not topic.strip():
        return "⚠️ Please enter a search topic"
    
    try:
        papers = fetcher.fetch_papers(
            query=topic,
            max_results=max_results,
            days=recent_days,
            sort_by=arxiv.SortCriterion.Relevance if sort_by == "Relevance" 
                  else arxiv.SortCriterion.SubmittedDate
        )

        if not papers:
            return (f"🔍 No papers found for '{topic}'\n\n"
                   "Try:\n"
                   "- More specific terms (e.g., 'transformer attention')\n"
                   "- Different time range\n"
                   "- Checking spelling")

        results = []
        for paper in papers:
            try:
                # Skip empty/invalid PDFs
                if os.path.getsize(paper['path']) == 0:
                    continue
                    
                text = extract_text_from_pdf(paper['path'])
                if not text:
                    continue
                
                # Process in chunks
                chunks = summarizer.chunk_text(text)
                summaries = []
                for chunk in chunks:
                    summary = summarizer.generate_summary(chunk)
                    if summary:
                        summaries.append(summary)
                
                if not summaries:
                    continue
                    
                full_summary = " ".join(summaries)
                keywords = summarizer.extract_keywords(full_summary)
                
                paper.update({
                    "summary": full_summary,
                    "keywords": keywords,
                    "Contributions": summarizer.extract_contributions(full_summary)
                })
                results.append(paper)
            except Exception as e:
                print(f"⚠️ Error processing {paper.get('title', 'unknown')}: {e}")

        if not results:
            return "⚠️ Found papers but couldn't process any content"

        ranked = rank_and_display(results, return_ranked=True)
        return format_results(ranked)

    except Exception as e:
        print(f"⚠️ Search error: {e}")
        return f"⚠️ Search failed: {str(e)}"

# Gradio Interface
with gr.Blocks(title="Academic Paper Summarizer") as demo:
    gr.Markdown("""# 📚 Academic Paper Summarizer
    Search, summarize, and discover research papers""")
    
    with gr.Row():
        with gr.Column():
            topic = gr.Textbox(label="Research Topic", 
                              placeholder="e.g., attention mechanisms in transformers")
            with gr.Row():
                max_results = gr.Slider(1, 10, value=5, label="Max Results")
                recent_days = gr.Slider(7, 730, value=365, label="Published in last (days)")
            sort_by = gr.Radio(["Relevance", "Recent"], value="Relevance", label="Sort By")
            search_btn = gr.Button("Search Papers", variant="primary")
        
        with gr.Column():
            output = gr.Markdown()
    
    search_btn.click(
        search_and_summarize,
        inputs=[topic, max_results, recent_days, sort_by],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch()


'''import os
from utils.search_arxiv import search_arxiv
from extract_text import extract_text_from_pdf
from utils.offline_summarizer import chunk_text, generate_summary, extract_keywords, extract_contributions

# Parameters
SEARCH_QUERY = "prethermalization rydberg"
NUM_PAPERS = 2
CHUNK_SIZE = 1000
OVERLAP = 100
SUMMARY_DIR = "summaries"

# Ensure summary directory exists
os.makedirs(SUMMARY_DIR, exist_ok=True)

# Step 1: Search and download papers
paper_paths = search_arxiv(query=SEARCH_QUERY, max_results=NUM_PAPERS)

# Step 2: Process each paper
for idx, (pdf_path, paper_id, title) in enumerate(paper_paths, start=1):
    print(f"\n[+] Processing Paper {idx}:\n{title}")

    # Extract full text from PDF
    full_text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(full_text, max_tokens=CHUNK_SIZE)

    print(f"[i] Split into {len(chunks)} chunks")

    # Step 3: Summarize each chunk
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"  • Summarizing chunk {i+1}/{len(chunks)}...")
        summary = generate_summary(chunk)
        if summary.strip():  # avoid blank chunks
            chunk_summaries.append(summary)

    # Step 4: Merge summaries for final abstract
    combined_summary_input = " ".join(chunk_summaries)
    print("🔄 Generating final summary...")
    final_summary = generate_summary(combined_summary_input)

    # Optional: Refine final summary
    print("✨ Refining summary for better readability...")
    final_summary = generate_summary(final_summary)

    # Step 5: Extract keywords and contributions
    keywords = extract_keywords(full_text)
    keywords = list(set([kw.lower() for kw in keywords if len(kw) > 3]))
    # simple clean-up

    contributions = extract_contributions(full_text)

    # Step 6: Save final output
    import re
    safe_title = re.sub(r"[^\w\-_.]", "_", title)

    output_file = os.path.join(SUMMARY_DIR, f"{idx}_{paper_id}_{safe_title}_summary.txt")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("🗝️ Important Keywords:\n")
        f.write("- " + "\n- ".join(keywords) + "\n\n")

        f.write("🚀 Main Contributions:\n")
        f.write("\n".join(contributions).strip() + "\n\n")


        f.write("📚 Summary:\n")
        f.write(final_summary.strip() if final_summary.strip() else "Summary not available.")

    print(f"✅ Summary saved to {output_file}")
'''




'''
#longass journey 
from utils.search_arxiv import search_arxiv
from utils.fetch_paper import fetch_and_download_papers  # Or download_pdf if you're using a helper
from extract_text import extract_text_from_pdf
from utils.summarize import summarize_text_offline
import os

if __name__ == "__main__":
    topic = "contrastive learning in NLP"
    papers = fetch_and_download_papers(query=topic, max_results=2)

    os.makedirs("data", exist_ok=True)

    for idx, paper in enumerate(papers):
        pdf_path = paper.get("path")
        title = paper.get("title")

        print(f"\n[+] Processing Paper {idx+1}:\n{title}")

        if not os.path.exists(pdf_path):
            print(f"❌ File not found: {pdf_path}")
            continue

        full_text = extract_text_from_pdf(pdf_path)

        if not full_text:
            print(f"❌ Skipping summary for paper {idx+1} due to extraction failure.")
            continue

        summary = summarize_text_offline(full_text)

        summary_path = f"data/summary_{idx+1}.txt"
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)

        print(f"\n📌 Summary {idx+1}:\n{summary}")'''



'''
#works w facebert-cnn
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
summarizer = pipeline("summarization", model=   ["model_name"], device=-1)

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
'''



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