from pathlib import Path

from fastapi import FastAPI, HTTPException

from app.schemas import (
    IngestRequest,
    IngestResponse,
)

from app.pdf_ingestor import PDFIngestor

app = FastAPI(
    title="Regulatory PDF Ingestion API",
    version="1.0.0"
)

REGULATORY_VAULT = Path("regulatory_vault")


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post(
    "/api/v1/ingest",
    response_model=IngestResponse
)
async def ingest_document(
    request: IngestRequest
):

    pdf_path = Path(request.file_path)

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if pdf_path.suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    ingestor = PDFIngestor(
        str(pdf_path)
    )

    result = ingestor.process()

    return result