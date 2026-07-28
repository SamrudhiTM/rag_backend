from beanie import Document
from pydantic import Field
from datetime import datetime, timezone
from typing import Optional


class ErrorLog(Document):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    endpoint: str
    method: str
    error_message: str
    stack_trace: str
    user_id: Optional[str] = None

    class Settings:
        name = "error_logs"
        indexes = ["timestamp"]