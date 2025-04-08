from transformers import pipeline
import math

# Load the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def chunk_text(text, max_chunk_tokens=1024):
    # Split text into smaller chunks based on token limit
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
