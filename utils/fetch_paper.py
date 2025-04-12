import arxiv
from typing import List, Dict
import requests
import os

class PaperFetcher:
    def __init__(self, save_dir: str = "papers"):
        os.makedirs(save_dir, exist_ok=True)
        self.save_dir = save_dir
        
    def fetch_papers(self, query: str, max_results: int = 3) -> List[Dict]:
        """Fetch papers with automatic query optimization"""
        try:
            search = arxiv.Search(
                query=self._optimize_query(query),
                max_results=max_results + 2,  # Get extras in case of failures
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            papers = []
            for result in search.results():
                if len(papers) >= max_results:
                    break
                    
                papers.append(self._process_result(result))
            
            return papers
            
        except Exception as e:
            print(f"Search failed: {e}")
            return []
    
    def _optimize_query(self, query: str) -> str:
        """Improve query success rate"""
        query = query.lower()
        if "computer vision" in query and "transformer" in query:
            return "(computer vision) AND (transformer OR vision transformer)"
        return query
    
    def _process_result(self, result) -> Dict:
        """Process a single search result"""
        paper_id = result.entry_id.split('/')[-1]
        pdf_path = os.path.join(self.save_dir, f"{paper_id}.pdf")
        
        # Download PDF if needed
        if not os.path.exists(pdf_path):
            try:
                response = requests.get(result.pdf_url, timeout=10)
                if response.status_code == 200:
                    with open(pdf_path, 'wb') as f:
                        f.write(response.content)
            except:
                pass
        
        return {
            "id": paper_id,
            "title": result.title,
            "authors": [a.name for a in result.authors],
            "published": result.published.strftime("%Y-%m-%d"),
            "summary": result.summary,
            "pdf_url": result.pdf_url,
            "arxiv_url": f"https://arxiv.org/abs/{paper_id}",
            "path": pdf_path
        }