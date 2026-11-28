from io import BytesIO
from pypdf import PdfReader
from fastapi import File, UploadFile, HTTPException, status


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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PDF file is empty."
        )

    if len(pdf_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PDF file must not exceed 5 MB."
        )

    if not pdf_bytes.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not a valid PDF."
        )

    return pdf_bytes



def extract_and_validate_pdf(pdf_bytes: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(pdf_bytes))

        if reader.is_encrypted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password-protected PDFs are not supported."
            )

        if len(reader.pages) > 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PDF must not contain more than 10 pages."
            )

        texts = []

        for page in reader.pages:
            texts.append(page.extract_text() or "")

        full_text = "\n".join(texts)
        full_text = full_text.replace("\x00", "").strip()

        if len(full_text) < 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This PDF contains no selectable text. Scanned PDFs are not supported."
            )

        return full_text

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or corrupted PDF file."
        ) from e