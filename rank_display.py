from typing import List, Dict

class PaperSummary:
    def __init__(self, paper: Dict):
        self.title = paper.get("title", "Untitled")
        self.keywords = paper.get("keywords", [])
        self.summary = paper.get("summary", "")
        self.arxiv_url = paper.get("arxiv_url", "#")
        self.pdf_url = paper.get("pdf_url", "#")
        self.authors = paper.get("authors", ["Unknown"])
        self.published = paper.get("published", "Unknown date")
        self.categories = paper.get("categories", ["Unknown"])
        self.score = self.compute_score()

    def compute_score(self) -> float:
        keyword_score = len(self.keywords) * 1.0
        summary_score = min(len(self.summary.split()) / 50.0, 10.0)  # Cap at 10
        return round(keyword_score + summary_score, 2)

    def to_display_dict(self, rank: int) -> Dict:
        return {
            "Rank": rank,
            "Score": self.score,
            "Title": self.title,
            "Keywords": ', '.join(self.keywords),
            "Summary": self.summary,
            "arxiv_url": self.arxiv_url,
            "pdf_url": self.pdf_url,
            "authors": self.authors,
            "published": self.published,
            "categories": self.categories
        }

def rank_and_display(papers: List[Dict], return_ranked: bool = False):
    summaries = [PaperSummary(p) for p in papers]
    sorted_summaries = sorted(summaries, key=lambda x: x.score, reverse=True)

    if return_ranked:
        return [s.to_display_dict(i + 1) for i, s in enumerate(sorted_summaries)]
    
    for i, s in enumerate(sorted_summaries, 1):
        print(f"Rank {i}: {s.title} (Score: {s.score})")