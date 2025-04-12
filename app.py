import gradio as gr
from utils.fetch_paper import PaperFetcher
from utils.summarize import PaperSummarizer
import time

class PaperApp:
    def __init__(self):
        self.fetcher = PaperFetcher()
        self.summarizer = PaperSummarizer()
        
    def process_query(self, query: str, max_results: int = 3) -> dict:
        """Full processing pipeline"""
        start_time = time.time()
        
        # Step 1: Fetch papers
        papers = self.fetcher.fetch_papers(query, max_results)
        if not papers:
            return {"status": "error", "message": "No papers found"}
        
        # Step 2: Process each paper
        results = []
        for paper in papers:
            processed = {
                "title": paper["title"],
                "authors": paper["authors"],
                "published": paper["published"],
                "arxiv_url": paper["arxiv_url"],
                "pdf_url": paper["pdf_url"],
                "abstract": paper["summary"],
                "download_time": f"{time.time() - start_time:.1f}s"
            }
            
            # Step 3: Generate summary
            summary = self.summarizer.summarize(paper["summary"])
            processed["summary"] = summary or "Summary unavailable"
            
            results.append(processed)
        
        return {
            "status": "success",
            "query": query,
            "processing_time": f"{time.time() - start_time:.2f} seconds",
            "papers": results
        }

    def display_results(self, query: str, max_results: int = 3) -> str:
        """Format results for Gradio"""
        result = self.process_query(query, max_results)
        
        if result["status"] != "success":
            return "🔍 No papers found. Try different keywords."
            
        output = [
            f"## 📄 Search Results for '{result['query']}'",
            f"*Processed in {result['processing_time']}*",
            "---"
        ]
        
        for i, paper in enumerate(result["papers"], 1):
            output.append(f"""
### {i}. {paper['title']}
**Authors:** {', '.join(paper['authors'][:3])}  
**Published:** {paper['published']}  
**Downloaded in:** {paper['download_time']}  

**Abstract Summary:**  
{paper['summary']}  

[PDF]({paper['pdf_url']}) | [arXiv]({paper['arxiv_url']})
""")
        
        return "\n".join(output)

# Create interface
app = PaperApp()

interface = gr.Interface(
    fn=app.display_results,
    inputs=[
        gr.Textbox(label="Search Query", 
                  placeholder="e.g., computer vision transformer"),
        gr.Slider(1, 5, value=3, label="Number of Papers")
    ],
    outputs=gr.Markdown(),
    title="📚 Research Paper Summarizer",
    description="Search arXiv papers and get AI-generated summaries"
)

if __name__ == "__main__":
    interface.launch()