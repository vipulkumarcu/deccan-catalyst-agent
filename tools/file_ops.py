# tools/file_ops.py
import PyPDF2
from docx import Document

def extract_text(uploaded_file):
    """
    Detects file type and extracts text accordingly.
    Supports: .pdf, .docx, .txt
    """
    file_name = uploaded_file.name.lower()

    try:
        # 1. Handle PDF
        if file_name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text

        # 2. Handle Word (.docx)
        elif file_name.endswith('.docx'):
            doc = Document(uploaded_file)
            return "\n".join([para.text for para in doc.paragraphs])

        # 3. Handle Plain Text (.txt)
        elif file_name.endswith('.txt'):
            # In Streamlit, uploaded files are 'bytes-like', so we decode them
            return uploaded_file.read().decode("utf-8")

        else:
            return "Unsupported file format. Please use PDF, DOCX, or TXT."

    except Exception as e:
        return f"Error processing {file_name}: {str(e)}"