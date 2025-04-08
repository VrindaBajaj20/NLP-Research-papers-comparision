import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extracts full text from a given PDF file using PyMuPDF."""
    text = ""

    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    
    except Exception as e:
        print(f"❌ Failed to extract text from {pdf_path}: {e}")
        return None
