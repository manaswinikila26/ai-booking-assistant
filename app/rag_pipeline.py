from pypdf import PdfReader

def extract_text_from_pdfs(pdfs):
    """
    Extracts text from uploaded PDF files.
    Lightweight and Streamlit Cloud safe.
    """
    text = ""
    for pdf in pdfs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text
