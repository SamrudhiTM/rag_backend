from beanie import Document as BeanieDocument
from pydantic import Field
from datetime import datetime, timezone


class Document(BeanieDocument):
    owner_id: str
    title: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "documents"
        indexes = ["owner_id"]