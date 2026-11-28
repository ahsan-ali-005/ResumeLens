from io import BytesIO
from pypdf import PdfReader


def extract_pdf_text(pdf_bytes: bytes) -> str:

    pdf_file = BytesIO(pdf_bytes)
    reader = PdfReader(pdf_file)
    extracted_text = []

    for page in reader.pages:
        text = page.extract_text() or ""
        extracted_text.append(text)

    full_text = "\n".join(extracted_text)
    full_text = full_text.replace("\x00", "")

    return full_text.strip()