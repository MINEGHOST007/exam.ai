from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import pandas as pd
import os

product_df = pd.read_csv('data/shl_product_details.csv')
irt_df = pd.read_csv('data/adaptive_irt.csv')

merged_df = product_df.merge(irt_df, on=['name', 'url'], how='left')

documents = []
for filename in os.listdir('downloads'):
    if filename.endswith('.pdf'):
        loader = UnstructuredPDFLoader(os.path.join('downloads', filename), strategy="hi_res")
        pages = loader.load()
        full_text = " ".join([page.page_content for page in pages])
        # Get metadata from CSV using filename (assuming name matches)
        assessment_name = os.path.splitext(filename)[0]
        meta_row = merged_df[merged_df['name'] == assessment_name]
        if not meta_row.empty:
            metadata = {
                'name': meta_row['name'].iloc[0],
                'url': meta_row['url'].iloc[0],
                'remote_testing': meta_row['remote_testing'].iloc[0],
                'adaptive_irt': meta_row['adaptive_irt'].iloc[0],
                'duration': meta_row['assessment_length'].iloc[0],
                'test_type': meta_row['test_types'].iloc[0]
            }
            doc = Document(page_content=full_text, metadata=metadata)
            documents.append(doc)

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(texts, embeddings, persist_directory="chroma_db")
vectorstore.persist()