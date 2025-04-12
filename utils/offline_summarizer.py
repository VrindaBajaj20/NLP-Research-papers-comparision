from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt', quiet=True)

class PaperSummarizer:
    def __init__(self, model_name: str = "t5-small"):
        self.summarizer = pipeline(
            "summarization",
            model=model_name,
            tokenizer=model_name,
            device=-1
        )
    
    def generate_summary(self, text: str) -> str:
        """Safe summarization with fallback"""
        if not text.strip():
            return ""
            
        try:
            # Simple chunking for short texts
            if len(text.split()) < 500:
                result = self.summarizer(
                    "summarize: " + text,
                    max_length=150,
                    min_length=30,
                    do_sample=False
                )
                return result[0]['summary_text']
            
            # For longer texts, summarize first 500 words
            chunks = sent_tokenize(text)
            first_chunk = " ".join(chunks[:20])[:2000]
            result = self.summarizer(
                "summarize: " + first_chunk,
                max_length=150,
                min_length=30,
                do_sample=False
            )
            return result[0]['summary_text']
            
        except Exception as e:
            print(f"Summarization failed: {e}")
            return ""