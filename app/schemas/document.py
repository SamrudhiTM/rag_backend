from pydantic import BaseModel


class DocumentCreate(BaseModel):
    title: str
    content: str


class DocumentResponse(BaseModel):
    message: str
    document_id: str
    chunks_created: int