from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import retrieve_relevant_chunks, generate_answer
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    relevant_chunks = await retrieve_relevant_chunks(
        owner_id=str(current_user.id),
        query=payload.query,
    )

    answer = await generate_answer(payload.query, relevant_chunks)

    sources = [chunk.content[:150] for chunk in relevant_chunks]

    return ChatResponse(answer=answer, sources=sources)