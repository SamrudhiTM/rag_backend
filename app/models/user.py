from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime, timezone
from pymongo import IndexModel, ASCENDING


class User(Document):
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"
        indexes = [
            IndexModel([("email", ASCENDING)], unique=True),
        ]