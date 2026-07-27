import numpy as np
from app.models.chunk import Chunk
from app.services.embedding_service import embed_text
from app.config import settings
from groq import Groq

groq_client = Groq(api_key=settings.groq_api_key)


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a_arr = np.array(a)
    b_arr = np.array(b)
    return float(np.dot(a_arr, b_arr) / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr)))


async def retrieve_relevant_chunks(owner_id: str, query: str, top_k: int = 3) -> list[Chunk]:
    query_vector = embed_text(query)

    all_chunks = await Chunk.find(Chunk.owner_id == owner_id).to_list()
    if not all_chunks:
        return []

    scored_chunks = [
        (chunk, cosine_similarity(query_vector, chunk.embedding))
        for chunk in all_chunks
    ]
    scored_chunks.sort(key=lambda x: x[1], reverse=True)

    return [chunk for chunk, score in scored_chunks[:top_k]]


async def generate_answer(query: str, context_chunks: list[Chunk]) -> str:
    if not context_chunks:
        context_text = "No relevant documents found."
    else:
        context_text = "\n\n".join(f"- {c.content}" for c in context_chunks)

    prompt = f"""Answer the question using only the context below. If the context doesn't contain the answer, say so honestly.

Context:
{context_text}

Question: {query}

Answer:"""

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )

    return response.choices[0].message.content