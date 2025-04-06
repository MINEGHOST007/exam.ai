# Import necessary modules for text splitting, PDF loading, vectorstore, and embeddings.
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain.schema import Document
import pandas as pd
import os

# Load metadata from CSV
combined_df = pd.read_csv('data/combined_product_data.csv')

documents = []
# Loop through all files in the downloads folder
for filename in os.listdir('downloads'):
    if filename.endswith('.pdf'):
        print(f"Processing {filename}...")
        try:
            # Load the PDF using OCR only
            loader = UnstructuredPDFLoader(os.path.join('downloads', filename), strategy="ocr_only")
            pages = loader.load()
            full_text = " ".join([page.page_content for page in pages])
            
            # Get the PDF name without extension and any extra whitespace.
            pdf_name = os.path.splitext(filename)[0].strip()
            
            # Find rows in the combined CSV where the PDF name starts with the CSV 'name' value.
            meta_matches = combined_df[combined_df['name'].apply(lambda x: pdf_name.startswith(x.strip()))]
            print(f"Trying {filename} (parsed as '{pdf_name}'): metadata found? {not meta_matches.empty}")
            
            if not meta_matches.empty:
                # Use the first matching row if multiple are found
                meta_row = meta_matches.iloc[0]
                metadata = {
                    'name': meta_row['name'],
                    'url': meta_row['url'],
                    'remote_testing': meta_row['remote_testing_x'],
                    'adaptive_irt': meta_row['adaptive_irt'],
                    'duration': meta_row['assessment_length'],
                    'test_type': meta_row['test_types']
                }
                print(f"Loaded {filename} with metadata: {metadata}")
                doc = Document(page_content=full_text, metadata=metadata)
                documents.append(doc)
            else:
                print(f"⚠️ No matching metadata found for PDF '{pdf_name}'.")
        except Exception as e:
            print(f"❌ Error processing {filename}: {str(e)}")

# Split and clean metadata
if documents:
    print(f"Total documents loaded: {len(documents)}")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    filtered_texts = filter_complex_metadata(texts)  # Critical fix
    
    # Create Chroma vectorstore with cleaned metadata
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    vectorstore = Chroma.from_documents(filtered_texts, embeddings, persist_directory="chroma_db")
    vectorstore.persist()
    
    print(f"✅ Ingestion successful! Processed {len(documents)} PDFs into {len(filtered_texts)} text chunks.")
else:
    print("⚠️ No documents were processed. Check your file paths and metadata matching logic.")