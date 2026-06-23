from pydantic import BaseModel


class IngestRequest(BaseModel):
    file_path: str


class IngestResponse(BaseModel):
    document_id: str
    title: str
    raw_markdown: str