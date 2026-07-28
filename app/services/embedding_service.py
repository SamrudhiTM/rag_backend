from typing import List
from google import genai
from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

EMBEDDING_DIM = 768


def embed_text(text: str) -> List[float]:
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )

    return response.embeddings[0].values


def embed_texts(texts: List[str]) -> List[List[float]]:
    vectors = []

    for text in texts:
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
        )

        vectors.append(response.embeddings[0].values)

    return vectors