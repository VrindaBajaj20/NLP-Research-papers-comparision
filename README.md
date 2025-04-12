
# **NLP Research Papers Comparison**  

A Natural Language Processing (NLP) project that compares research papers using text similarity techniques, helping researchers find related work efficiently.  

---

## **Table of Contents**  
- [Features](#-features)  
- [Installation](#-installation)  
- [Methods](#-methods--techniques)  
- [Dataset](#-dataset)    
- [Contributing](#-contributing)  
- [Acknowledgements](#-acknowledgements)  

---

##  Features
- **Text Preprocessing**: Cleans and normalizes research paper text (tokenization, stopword removal, stemming).  
- **Similarity Comparison**: Uses **TF-IDF, Word2Vec, and BERT/T-5 embeddings** to compare papers.  
- **Visualization**: Generates similarity matrices and interactive plots.  
- **User-Friendly**: CLI and/or Jupyter notebook for easy experimentation.  

---

## Installation  

### Prerequisites
- Python 3.8+  
- pip / conda  

### Steps 
1. Clone the repository:  
   ```bash
   git clone https://github.com/VrindaBajaj20/NLP-Research-papers-comparison.git
   cd NLP-Research-papers-comparison
   ```  

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  

3. Download NLTK data (if required):  
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```  



---

## Methods

TF-IDF   
Word2Vec   
T-5   
Cosine Similarity

---

## Dataset 
- The project can process:  
  - PDFs (using `PyPDF2` or `pdfplumber`).  
  - Text files (`.txt`).  
  - Pre-processed CSV datasets (example: [arXiv NLP Papers](https://www.kaggle.com/datasets)).  

---


## Contributing
Contributions are welcome!  
1. Fork the repo.  
2. Create a branch (`git checkout -b feature/new-method`).  
3. Commit changes (`git commit -m "Add XLNet comparison"`).  
4. Push to the branch (`git push origin feature/new-method`).  
5. Open a **Pull Request**.  

---

## License
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.  

---

## Acknowledgements 
- [HuggingFace Transformers](https://huggingface.co/) for BERT.  
- [NLTK](https://www.nltk.org/) for text preprocessing.  
- Inspired by [arXiv](https://arxiv.org/) and related NLP research.  

---

