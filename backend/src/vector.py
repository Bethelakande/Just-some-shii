from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd
import io
from PyPDF2 import PdfReader



def vectorize(insert_document=True):
    upload_folder = 'uploads/'
    # Ensure the uploads directory exists
    if not os.path.exists(upload_folder):
        raise FileNotFoundError(f"Upload directory not found at: {os.path.abspath(upload_folder)}")
    
    files = os.listdir(upload_folder)
    if not files:
        raise ValueError("No files found in uploads directory")
    
    file_path = os.path.join(upload_folder, files[0])
    print(f"Processing file: {file_path}")
    print(f"File size: {os.path.getsize(file_path)} bytes")
    
    if os.path.getsize(file_path) == 0:
        raise ValueError(f"The file {files[0]} is empty")
    
    text = ""
    
    # Check file extension to determine how to read it
    if file_path.lower().endswith('.pdf'):
        with open(file_path, 'rb') as f:
            try:
                pdf = PdfReader(f)
                if not pdf.pages:
                    raise ValueError("PDF file contains no pages")
                    
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    else:
                        print(f"Warning: Page {pdf.pages.index(page) + 1} contains no extractable text")
                        
                if not text.strip():
                    raise ValueError("No text could be extracted from the PDF")
                    
            except Exception as e:
                raise ValueError(f"Error processing PDF: {str(e)}")
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    db_location = "./chroma_langchain_db"
    add_document = not os.path.exists(db_location) or insert_document

    if add_document:
        documents = []
        ids = []
        document = Document(
            page_content=text,
            id=str(1)
        )
        ids.append(str(1))
        documents.append(document)

    vector_store = Chroma(
        collection_name="restaurant_reviews",
        persist_directory=db_location,
        embedding_function=embeddings,
    )

    if add_document:
        vector_store.add_documents(documents=documents,ids=ids)


    retriever = vector_store.as_retriever(search_kwargs={"k":5})

    return retriever