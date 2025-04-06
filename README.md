### Key Points
- It seems likely that the database ingestion issues prevented the completion of your SHL Assessment Recommender Chatbot project.
- Research suggests that metadata matching and PDF processing errors were major challenges, affecting the vector database setup.
- The evidence leans toward improving matching logic and OCR configuration for future attempts, but the project couldn't be finished within the timeline.

### Project Overview
Your project aimed to build a chatbot that recommends SHL assessments using natural language queries, processing over 500 PDFs with OCR and storing them in a vector database like Pinecone or Chroma. However, due to database issues, it couldn't be completed.

### Challenges Faced
The main problems were:
- Difficulty matching PDF filenames with CSV metadata, leading to many skipped files.
- Errors in processing PDFs, especially those with images or complex layouts, due to OCR limitations.
- Potential configuration issues with the vector database, impacting storage and retrieval.

### Next Steps
To move forward, consider enhancing metadata matching, improving PDF parsing with tools like PyMuPDF, and adding detailed logging for debugging. This can help in future attempts to complete the project.

---

### Comprehensive Guide to Creating and Documenting the SHL Assessment Recommender Chatbot Project

This note provides a detailed analysis and documentation of the SHL Assessment Recommender Chatbot project, which aimed to build a Retrieval-Augmented Generation (RAG) LLM chatbot for recommending SHL assessments based on natural language queries, job descriptions, or URLs. The project leveraged a collection of over 500 PDFs and CSV files for metadata, but faced significant challenges during the database ingestion phase, preventing its completion. Given the current date (03:30 PM PDT on Sunday, April 6, 2025), this documentation reflects the state of the project and provides insights for future development.

#### Project Description and Goals

The SHL Assessment Recommender Chatbot was designed to assist users in finding relevant SHL assessments by processing PDF documents containing assessment details and enriching them with metadata from CSV files. The system intended to use natural language processing and retrieval-augmented generation to provide tailored recommendations based on user queries, such as job descriptions or specific requirements. Key components included:

- **PDF Processing:** Extraction of text from PDFs using OCR to handle both text and image-based content, ensuring comprehensive document parsing.
- **Vector Database:** Storage of document embeddings in a vector database (e.g., Pinecone or Chroma) for efficient semantic search, enabling the chatbot to retrieve relevant assessments.
- **LLM Integration:** Utilization of an open-source large language model via LangChain to generate context-aware responses based on retrieved documents.
- **Web Interface:** A user-friendly frontend built with HTML, CSS, and JavaScript, connected to a Flask backend for handling queries and displaying results in a tabular format.

The project's goal was to process over 500 PDFs, each representing an SHL assessment, and integrate with CSV files containing additional details like URLs, remote testing support, and test types, to provide accurate and diverse recommendations.

#### Technologies and Tools Used

The project utilized the following technologies and tools, selected for their free availability and suitability for rapid development:

- **Programming Language:** Python, for backend logic and data processing.
- **Web Framework:** Flask, for creating a REST endpoint to handle user queries.
- **RAG Framework:** LangChain, for integrating PDF processing, vector storage, and LLM interactions.
- **Vector Databases:** Pinecone and Chroma, for storing and searching document embeddings, with Pinecone requiring API keys for cloud hosting.
- **Embeddings:** HuggingFace Embeddings, specifically the "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2" model, for generating vector representations.
- **PDF Processing:** Unstructured PDF Loader with Tesseract OCR, configured for "hi_res" strategy to handle image-heavy PDFs.
- **Frontend Technologies:** HTML, CSS, and JavaScript, for a simple web interface.
- **Data Handling:** Pandas, for reading and manipulating CSV files.
- **Additional Libraries:** Requests and BeautifulSoup4 for web scraping, Python-dotenv for environment variable management.

The project required installation of Tesseract OCR separately, with instructions provided for Ubuntu, macOS, and Windows, ensuring cross-platform compatibility.

#### Installation and Setup Process

The setup process was documented to facilitate future development and potential contributions. The steps included:

1. **Cloning the Repository:**
   - Users were instructed to clone the repository using:
     ```bash
     git clone https://github.com/yourusername/shl-chatbot.git
     cd shl-chatbot
     ```

2. **Data Placement:**
   - Place the SHL assessment PDFs in the `downloads/` directory.
   - Ensure the `data/combined_product_data.csv` file is present, containing metadata like name, URL, remote testing, adaptive IRT, duration, and test types.

3. **Dependency Installation:**
   - Install required packages using:
     ```bash
     pip install -r requirements.txt
     ```
   - The `requirements.txt` file included specific versions like `flask==2.0.1`, `langchain==0.1.0`, and `pinecone-client==2.2.1`, ensuring compatibility.

4. **Tesseract OCR Installation:**
   - Instructions were provided for different operating systems:
     - Ubuntu: `sudo apt-get install tesseract-ocr`
     - macOS: `brew install tesseract`
     - Windows: Download from [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract/wiki)

5. **Environment Variables for Pinecone:**
   - For users opting for Pinecone, create a `.env` file with:
     ```
     PINECONE_API_KEY=your_api_key
     PINECONE_ENVIRONMENT=your_environment
     ```
   - Users were advised to sign up for a free Pinecone account at [Pinecone](https://www.pinecone.io/) to obtain the API key and environment.

#### Usage and Intended Workflow

The intended usage involved the following steps:

1. **Ingestion Process:**
   - Run the ingestion script:
     ```bash
     python ingest.py
     ```
   - This script processes each PDF, extracts text using OCR, matches with CSV metadata, splits documents into chunks, and stores them in the vector database. It includes logging to track successes, metadata mismatches, and errors.

2. **Backend Startup:**
   - Start the Flask backend:
     ```bash
     python app.py
     ```
   - The backend listens for POST requests at `/query`, processing user queries and returning JSON responses with relevant assessments.

3. **Frontend Interaction:**
   - Open the frontend in a browser at `[invalid url, do not cite]`.
   - Users enter a query or job description in a textarea and submit to receive recommendations, displayed in a table with columns for name, URL, remote testing, adaptive IRT, duration, and test type.

However, due to the incomplete database ingestion, the recommendations were not fully functional, as the vector database did not contain the expected number of documents.

#### Challenges and Limitations

The project faced significant challenges during the database ingestion phase, which ultimately prevented its completion. These challenges included:

- **Metadata Matching Issues:**
  - The script attempted to match PDF filenames with CSV entries using a `startswith` condition, which proved too strict. Many PDFs had additional prefixes (e.g., "Assessment - ") or suffixes, leading to mismatches. For example, a PDF named "Assessment - .NET Framework 4.5.pdf" might not match the CSV entry ".NET Framework 4.5".
  - This resulted in a high number of PDFs being skipped, with the script logging "⚠️ No matching metadata found for PDF 'pdf_name'."

- **PDF Processing Errors:**
  - Some PDFs contained images or complex layouts that the OCR tool (Tesseract with UnstructuredPDFLoader) struggled with, leading to incomplete or erroneous text extraction. The script logged errors like "❌ Error processing filename: error_message," indicating issues with loading or parsing.
  - The OCR strategy "hi_res" was used, but for certain PDFs, the extracted text was gibberish or empty, affecting document quality.

- **Vector Database Configuration:**
  - There might have been configuration errors or limitations with the free tier of the vector database service, such as Pinecone, affecting the storage and retrieval of document embeddings. The script included counters for successful processes, metadata mismatches, and errors, showing:
    - Processed: X success, Y no metadata, Z errors, where X, Y, and Z indicated the extent of the issue.

Due to these challenges, the database did not contain the expected number of documents, impacting the chatbot's ability to provide diverse and accurate recommendations. The frontend and backend were set up, but without a properly populated database, the system could not deliver the intended functionality.

#### Future Work and Recommendations

To complete the project, the following steps are recommended for future development:

1. **Enhance Metadata Matching:**
   - Implement a more robust matching algorithm, such as using regular expressions or natural language processing techniques to find similarities between PDF names and CSV entries. For example, use `x.strip().lower() in pdf_name.lower()` instead of `startswith` to capture partial matches.
   - Consider manual mapping for a subset of PDFs if the number is manageable, or use fuzzy matching libraries like `fuzzywuzzy` for automated matching.

2. **Improve PDF Parsing:**
   - Explore alternative PDF parsing libraries like PyMuPDF or pdfplumber, which might handle certain PDFs better, especially those with tables or images. PyMuPDF is known for its text and image extraction capabilities, while pdfplumber excels at table extraction.
   - Ensure Tesseract OCR is properly configured with appropriate language packs and test different OCR strategies (e.g., "hi_res" vs. "ocr_only") to optimize text extraction.

3. **Monitor Database Ingestion:**
   - Add detailed logging during the ingestion process to track which PDFs are successfully processed, which fail due to metadata mismatches, and which encounter errors. Print snippets of extracted text to verify quality, e.g., "Extracted text from filename: first 100 characters...".
   - Use counters to summarize the ingestion outcome, such as "Processed: 100 success, 200 no metadata, 50 errors," to identify patterns and focus on problematic files.

4. **Optimize Vector Database Usage:**
   - If using Pinecone, ensure the index is correctly set up with the appropriate dimensions (e.g., 384 for the chosen embedding model) and that embeddings are properly generated and uploaded. Check free tier limits at [Pinecone](https://www.pinecone.io/) for storage and query allowances.
   - For Chroma, verify local storage settings and ensure persistence is working, especially on hosting platforms like [Render](https://render.com/) with ephemeral file systems.

These steps would help in overcoming the current limitations and completing the chatbot, ensuring it can handle the full dataset and provide accurate recommendations.

#### Project Status and Contribution Guidelines

Given the incomplete state, the project is currently in a developmental phase, with the database ingestion being the primary bottleneck. The repository includes partial implementations of the backend, frontend, and ingestion scripts, but users should be aware that the system is not fully functional.

Contributions are welcome to address the identified challenges. Potential contributors can fork the repository and submit pull requests for improvements, particularly in the areas of metadata matching, PDF parsing, and database configuration. Please ensure to follow the installation instructions and test changes with a subset of PDFs before submitting.

#### Licensing Information

This project is licensed under the MIT License, allowing for free use, modification, and distribution, provided the original copyright notice and disclaimer are included.

#### Table of CSV and PDF Matching Examples

To illustrate the metadata matching issue, consider the following table of hypothetical examples, which highlights why many PDFs were skipped:

| PDF Filename                     | CSV Name                | Old Match (startswith) | New Match (contains, case-insensitive) |
|-----------------------------------|------------------------|-----------------------|---------------------------------------|
| Assessment - .NET Framework 4.5.pdf | .NET Framework 4.5     | False                 | True                                  |
| .NET Framework 4.5 - v2.pdf       | .NET Framework 4.5     | False                 | True                                  |
| Accounts Payable (New).pdf        | Accounts Payable (New) | True                  | True                                  |
| SHL Assessment - Adobe.pdf        | Adobe Experience Manager | False                 | False (may need further adjustment)   |

This table demonstrates how a more flexible matching approach could capture more PDFs, improving ingestion success rates.

#### Key Citations

- [How to Write a Good README File for Your GitHub Project](https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/)
- [Best Practices for Writing a README](https://bulldogjob.com/readme/how-to-write-a-good-readme-for-your-github-project)
- [Awesome README Examples](https://github.com/matiassingers/awesome-readme)
- [Pinecone Free Tier Details](https://www.pinecone.io/)
- [Render Free Web Hosting Platform](https://render.com/)
- [Tesseract OCR GitHub Wiki](https://github.com/tesseract-ocr/tesseract/wiki)
