from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
from sklearn.metrics.pairwise import cosine_similarity

class SemanticSearch:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.paper_embeddings = {}
    
    def add_paper(self, paper_id: str, text: str):
        embedding = self.model.encode(text)
        self.paper_embeddings[paper_id] = embedding
    
    def find_similar(self, query: str, top_k: int = 3) -> List[str]:
        query_embed = self.model.encode(query)
        similarities = []
        
        for paper_id, embed in self.paper_embeddings.items():
            sim = cosine_similarity([query_embed], [embed])[0][0]
            similarities.append((paper_id, sim))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [paper_id for paper_id, _ in similarities[:top_k]]