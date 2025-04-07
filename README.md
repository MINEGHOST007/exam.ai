```markdown
# SHL Assessment Recommender Chatbot 🔍🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

A Retrieval-Augmented Generation (RAG) chatbot that recommends SHL assessments using natural language queries. Processes 500+ PDF documents with OCR and semantic search capabilities.

**Current Status**: 🚧 Work in Progress (Metadata matching & scaling challenges)

---

## Features ✨

- **PDF Intelligence**: OCR processing for text/image-based assessments
- **Dual Database Support**: Chroma (local) & Pinecone (cloud)
- **Contextual Search**: Multilingual embeddings for job description matching
- **Smart Deduplication**: Unique assessment filtering with relevance scoring
- **Web Integration**: Flask API with URL content analysis

---

## Tech Stack 💻

| Component              | Technologies Used                              |
|------------------------|-----------------------------------------------|
| **Backend**            | Python 3.9, Flask, LangChain                  |
| **Vector Databases**   | Chroma (Local), Pinecone (Cloud)              |
| **NLP**                | HuggingFace `paraphrase-multilingual-MiniLM`  |
| **PDF Processing**     | Unstructured.io + Tesseract OCR               |
| **Frontend**           | HTML5, CSS3, JavaScript                       |

---

## Installation 🛠️

1. **Clone Repository**
   ```bash
   git clone https://github.com/MINEGHOST007/exam.ai.git
   cd exam.ai
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Tesseract OCR**
   - **Windows**: [Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki)
   - **Mac**: `brew install tesseract`
   - **Linux**: `sudo apt install tesseract-ocr`

4. **Add Data**
   ```bash
   mkdir downloads
   # Add PDFs to downloads/ and CSV to data/
   ```

---

## Usage 🚀

### 1. Data Ingestion (Chroma)
```python
python ingest.py
```
**Expected Output:**
```bash
Processing Assessment-X.pdf...
✅ Ingestion successful! Processed 120 PDFs into 850 text chunks.
```

### 2. Start Flask Server
```python
python app.py
```

### 3. Web Interface
Visit `http://localhost:5000` and try:
- "Remote software engineering assessments"
- "https://example.com/job-post"

---

## Key Challenges 🧩

1. **Metadata Mismatch**
   ```python
   # Current matching logic
   meta_matches = combined_df[combined_df['name'].apply(lambda x: pdf_name.startswith(x.strip()))]
   ```
   - 40% PDFs skipped due to filename prefixes

2. **PDF Parsing Edge Cases**
   ```bash
   ❌ Error processing Assessment-32.pdf: OCR failed on image-heavy layout
   ```

3. **Pinecone Scaling**
   - Free tier limitations during bulk uploads
   - Cloud deployment timeouts

---

## Roadmap 🗺️

- [ ] Fuzzy Metadata Matching
- [ ] PDF Table Extraction
- [ ] Pinecone Batch Uploads
- [ ] Docker Deployment
- [ ] Assessment Preview Cards

---

## Contributing 🤝

1. Fork repository
2. Create feature branch
3. Submit PR with:
   - Test cases for new PDF types
   - Performance benchmarks
   - Improved metadata matching logic

---

## License 📄

MIT License - See [LICENSE](LICENSE) for details.

---

> "Assessment intelligence should be accessible to all" - GHOST
> 
> *Built with ❤️ using [LangChain](https://langchain.com/) and [Render](https://render.com/)*
```