from pathlib import Path

from pypdf import PdfReader
from docx import Document


def extract_pdf_text(file_path: str) -> str:
    """
    Extract text from a PDF file.
    """

    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        try:
            page_text = page.extract_text()

            if page_text:
                pages.append(
                    f"\n--- Page {page_number} ---\n"
                    + page_text
                )

        except Exception as error:
            print(
                f"Error reading PDF page {page_number}: {error}"
            )

    return "\n".join(pages)


def extract_docx_text(file_path: str) -> str:
    """
    Extract paragraphs from DOCX.
    """

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)


def extract_txt_text(file_path: str) -> str:
    """
    Extract text from TXT.
    """

    path = Path(file_path)

    return path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def extract_text(file_path: str) -> str:
    """
    Automatically select the correct extractor.
    """

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    elif extension == ".docx":
        return extract_docx_text(file_path)

    elif extension == ".txt":
        return extract_txt_text(file_path)

    else:
        raise ValueError(
            "Unsupported file type. "
            "Use PDF, DOCX, or TXT."
        )