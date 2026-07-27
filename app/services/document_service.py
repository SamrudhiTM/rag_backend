from app.models.document import Document
from app.models.chunk import Chunk
from app.services.chunking import chunk_text
from app.services.embedding_service import embed_texts


async def ingest_document(owner_id: str, title: str, content: str) -> dict:
    # 1. Save the original document
    document = Document(owner_id=owner_id, title=title, content=content)
    await document.insert()

    # 2. Split into chunks
    pieces = chunk_text(content)
    if not pieces:
        return {"document_id": str(document.id), "chunk_count": 0}

    # 3. Embed all chunks in one batch
    vectors = embed_texts(pieces)

    # 4. Create Chunk documents
    chunk_objects = [
        Chunk(
            document_id=str(document.id),
            owner_id=owner_id,
            content=piece,
            embedding=vector,
            chunk_index=idx,
        )
        for idx, (piece, vector) in enumerate(zip(pieces, vectors))
    ]

    # 5. Insert all chunks in one batch
    await Chunk.insert_many(chunk_objects)

    return {"document_id": str(document.id), "chunk_count": len(chunk_objects)}