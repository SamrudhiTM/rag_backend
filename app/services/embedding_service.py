from sentence_transformers import SentenceTransformer
from typing import List

_model = SentenceTransformer("all-MiniLM-L6-v2")

EMBEDDING_DIM = 384


def embed_text(text: str) -> List[float]:
    vector = _model.encode(text, normalize_embeddings=True)
    return vector.tolist()


def embed_texts(texts: List[str]) -> List[List[float]]:
    vectors = _model.encode(texts, normalize_embeddings=True)
    return [v.tolist() for v in vectors]