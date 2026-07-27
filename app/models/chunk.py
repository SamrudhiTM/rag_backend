from beanie import Document as BeanieDocument
from pydantic import Field
from datetime import datetime, timezone
from typing import List


class Chunk(BeanieDocument):
    document_id: str
    owner_id: str
    content: str
    embedding: List[float]
    chunk_index: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "chunks"
        indexes = ["document_id", "owner_id"]