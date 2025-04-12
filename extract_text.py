# extract_text.py
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file"""
    try:
        with fitz.open(pdf_path) as doc:
            return " ".join(page.get_text() for page in doc)
    except Exception as e:
<<<<<<< HEAD
        print(f"Text extraction failed: {e}")
        return ""
=======
        print(f" Failed to extract text from {pdf_path}: {e}")
        return None
>>>>>>> commit -hash
