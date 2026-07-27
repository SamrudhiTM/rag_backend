from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.mongo_uri)
db = client[settings.mongo_db_name]

users_collection = db["users"]
documents_collection = db["documents"]
chunks_collection = db["chunks"]
error_logs_collection = db["error_logs"]


async def create_indexes():
    # Unique index on email so signup can't create duplicate accounts
    await users_collection.create_index("email", unique=True)

    # Speeds up "get all chunks for a document" during retrieval/deletion
    await chunks_collection.create_index("document_id")

    # Speeds up "get all documents owned by this user"
    await documents_collection.create_index("owner_id")

    # Useful for querying/filtering error logs by time in an admin view
    await error_logs_collection.create_index("timestamp")