from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from app.models.user import User
from app.models.document import Document
from app.models.chunk import Chunk


async def init_db():
    client = AsyncIOMotorClient(settings.mongo_uri)
    database = client[settings.mongo_db_name]

    await init_beanie(
        database=database,
        document_models=[User, Document, Chunk],
    )