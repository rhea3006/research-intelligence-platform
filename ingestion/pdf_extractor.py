import re
import pymupdf


def clean_text(text: str) -> str:
    """
    Normalize extracted PDF text.

    - Collapse repeated whitespace
    - Normalize line breaks
    - Remove leading/trailing whitespace
    """
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


def extract_pdf_text(pdf_path: str) -> str:
    """
    Extract text from a PDF using PyMuPDF.
    """

    document = pymupdf.open(pdf_path)

    pages = []

    try:
        for page in document:
            text = page.get_text("text")

            if text.strip():
                pages.append(text)
    finally:
        document.close()

    return clean_text("\n\n".join(pages))