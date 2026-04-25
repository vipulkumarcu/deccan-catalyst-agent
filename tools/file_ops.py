"""
Core utility for document text extraction.
Handles multi-format ingestion for PDF, DOCX, and TXT files.
"""

import PyPDF2
from docx import Document
from typing import Any

def extract_text(uploaded_file: Any) -> str:
    """
    Identifies the file extension and executes the appropriate extraction logic.
    Supports: .pdf, .docx, .txt

    Args:
        uploaded_file: The Streamlit UploadedFile object.

    Returns:
        str: The extracted text or a formatted error message.
    """
    if uploaded_file is None:
        return "No file provided."

    file_name = uploaded_file.name.lower()

    try:
        # Important: Streamlit file buffers can sometimes be at the end of the file
        # if read elsewhere. We ensure we start from the beginning.
        uploaded_file.seek(0)

        # 1. PDF Extraction
        if file_name.endswith('.pdf'):
            reader = PyPDF2.PdfReader(uploaded_file)
            # Using a list comprehension for faster, cleaner string joining
            text = [page.extract_text() for page in reader.pages if page.extract_text()]
            return "\n".join(text) if text else "Error: PDF contains no extractable text."

        # 2. Word (.docx) Extraction
        elif file_name.endswith('.docx'):
            doc = Document(uploaded_file)
            # Join paragraphs with double newlines for better structural preservation
            text = [para.text for para in doc.paragraphs if para.text.strip()]
            return "\n\n".join(text) if text else "Error: Word document is empty."

        # 3. Plain Text (.txt) Extraction
        elif file_name.endswith('.txt'):
            # Standardizing to utf-8; handles most modern professional documents
            return uploaded_file.read().decode("utf-8")

        else:
            return "Unsupported Format: Please provide a PDF, DOCX, or TXT file."

    except Exception as e:
        # Professional error reporting for the UI
        return f"File Ingestion Error [{file_name}]: {str(e)}"