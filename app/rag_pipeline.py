from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def extract_text_from_pdfs(pdf_files):
    text = ""
    for pdf in pdf_files:
        reader = PdfReader(pdf)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def chunk_text(text, chunk_size=400):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

def create_embeddings(chunks):
    vectorizer = TfidfVectorizer(stop_words="english")
    embeddings = vectorizer.fit_transform(chunks)
    return vectorizer, embeddings

def rag_query(query, chunks, vectorizer, embeddings):
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, embeddings)[0]
    best_idx = np.argmax(scores)
    return chunks[best_idx]