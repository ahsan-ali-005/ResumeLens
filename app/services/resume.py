from io import BytesIO
from pypdf import PdfReader
from fastapi import File, UploadFile, HTTPException


MAX_FILE_SIZE = 5 * 1024 * 1024

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



async def validate_pdf_upload(file: UploadFile) -> bytes:
    pdf_bytes = await file.read(MAX_FILE_SIZE + 1)

    if not pdf_bytes:
        raise HTTPException(
            status_code=400,
            detail="PDF file is empty."
        )

    if len(pdf_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="PDF file must not exceed 5 MB."
        )

    if not pdf_bytes.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is not a valid PDF."
        )

    return pdf_bytes