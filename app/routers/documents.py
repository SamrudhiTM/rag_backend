from fastapi import APIRouter, Depends
from app.schemas.document import DocumentCreate, DocumentResponse
from app.services.document_service import ingest_document
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/", response_model=DocumentResponse)
async def create_document(
    payload: DocumentCreate,
    current_user: User = Depends(get_current_user),
):
    result = await ingest_document(
        owner_id=str(current_user.id),
        title=payload.title,
        content=payload.content,
    )
    return DocumentResponse(
        message="Document ingested successfully",
        document_id=result["document_id"],
        chunks_created=result["chunk_count"],
    )