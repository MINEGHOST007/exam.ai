from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup
# Updated imports from langchain_community
from langchain_community.vectorstores import Chroma  
from langchain_community.embeddings import HuggingFaceEmbeddings

app = Flask(__name__)

# -------------------------------------------------------------------
# Load vector store from the persisted directory "chroma_db"
# Use a multilingual embedding model for better support of non-English text.
# -------------------------------------------------------------------
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

# -------------------------------------------------------------------
# Helper function to fetch text content from a URL using BeautifulSoup.
# -------------------------------------------------------------------
def fetch_url_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except Exception as e:
        return str(e)

# -------------------------------------------------------------------
# Home route - renders the index.html template.
# -------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# -------------------------------------------------------------------
# Query route - accepts POST requests with a query (or URL).
# If the query is a URL, it fetches its text; otherwise, it uses the query directly.
# Performs a similarity search on the vectorstore and returns top results.
# -------------------------------------------------------------------
@app.route('/query', methods=['POST'])
def query():
    data = request.json
    query_input = data.get('query', '')
    
    # If the query starts with 'http', treat it as a URL and fetch its text.
    if query_input.startswith('http'):
        query_text = fetch_url_text(query_input)
    else:
        query_text = query_input

    # Retrieve more documents to ensure we have enough unique assessments after deduplication
    results = vectorstore.similarity_search_with_score(query_text, k=30)
    
    # Dictionary to store unique assessments by name
    unique_assessments = {}
    
    for doc, score in results:
        # Use a relevance threshold (e.g., score must be > 0.5)
        if score > 0.1:
            meta = doc.metadata
            name = meta.get('name', '')
            
            # Skip if we've already seen this assessment name or if name is empty
            if not name or name in unique_assessments:
                continue
                
            # Parse the duration if it contains '='; otherwise, use the original string.
            duration = meta.get('duration', '')
            if '=' in duration:
                duration = duration.split('=')[1].strip()
                
            # Format remote_testing and adaptive_irt to 'Yes' or 'No'
            remote_testing = 'Yes' if str(meta.get('remote_testing', '')).strip().lower() == 'true' else 'No'
            adaptive_irt = 'Yes' if str(meta.get('adaptive_irt', '')).strip().lower() == 'true' else 'No'
            
            # Build the assessment dictionary with metadata values.
            assessment = {
                'name': name,
                'url': meta.get('url', ''),
                'remote_testing': remote_testing,
                'adaptive_irt': adaptive_irt,
                'duration': duration,
                'test_type': meta.get('test_type', '')
            }
            
            print(f"Found unique assessment: {name}")
            unique_assessments[name] = assessment
    
    # Convert the dictionary values to a list
    assessment_list = list(unique_assessments.values())
    
    # Return at most 10 unique assessments as a JSON response
    return jsonify(assessment_list)

# -------------------------------------------------------------------
# Run the Flask app in debug mode if executed as the main module.
# -------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)