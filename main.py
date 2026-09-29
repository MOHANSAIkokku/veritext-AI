import os
import uuid

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from text_extractor import extract_text

from analyzer import analyze_document


# --------------------------------------------------
# APP
# --------------------------------------------------

app = FastAPI(
    title="VeriText AI",
    description=(
        "AI-generated content detection "
        "and document analysis API"
    ),
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# --------------------------------------------------
# UPLOAD DIRECTORY
# --------------------------------------------------

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# --------------------------------------------------
# TEXT REQUEST
# --------------------------------------------------

class TextRequest(BaseModel):

    text: str


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "application": "VeriText AI",
        "status": "running",
        "message": (
            "AI-generated content "
            "detection API is running."
        )
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# --------------------------------------------------
# TEXT DETECTION
# --------------------------------------------------

@app.post("/detect")
def detect_text(
    request: TextRequest
):

    if not request.text.strip():

        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty."
        )

    try:

        result = analyze_document(
            request.text
        )

        return {
            "success": True,
            "source": "text",
            "result": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

@app.post("/analyze-file")
async def analyze_file(
    file: UploadFile = File(...)
):

    allowed_extensions = [
        ".pdf",
        ".docx",
        ".txt"
    ]

    filename = file.filename or ""

    extension = os.path.splitext(
        filename
    )[1].lower()

    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Upload PDF, DOCX, or TXT."
            )
        )

    # Generate unique filename
    unique_name = (
        f"{uuid.uuid4()}{extension}"
    )

    file_path = os.path.join(
        UPLOAD_FOLDER,
        unique_name
    )

    try:

        # Save file
        content = await file.read()

        with open(
            file_path,
            "wb"
        ) as output_file:

            output_file.write(content)

        # Extract text
        extracted_text = extract_text(
            file_path
        )

        if not extracted_text.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text found. "
                    "The PDF may be scanned/image-only."
                )
            )

        # Analyze
        result = analyze_document(
            extracted_text
        )

        return {
            "success": True,
            "source": "file",
            "filename": filename,
            "result": result
        }

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:

        # Delete uploaded file after processing
        if os.path.exists(file_path):

            os.remove(file_path)