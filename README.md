# RAG Backend Assignment

FastAPI backend with JWT authentication and a Retrieval-Augmented Generation (RAG) pipeline: document ingestion with chunking + embeddings, a `/chat` endpoint that retrieves relevant context and generates answers via an LLM, and middleware that logs unhandled errors to MongoDB.

## Tech Stack

- FastAPI (async), MongoDB via Motor + Beanie ODM
- JWT auth (python-jose) + bcrypt password hashing (passlib)
- Embeddings: sentence-transformers (`all-MiniLM-L6-v2`), run locally
- LLM: Groq API (`llama-3.1-8b-instant`)
- Retrieval: in-memory cosine similarity over stored chunk embeddings

## Setup

1. Clone and create a virtual environment:

```bash
   git clone https://github.com/SamrudhiTM/rag_backend.git
   cd rag_backend
   python -m venv venv
   venv\Scripts\activate   # Windows
```

2. Install dependencies:

```bash
   pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in real values (MongoDB URI, JWT secret, Groq API key). Generate a secure JWT secret with:

```bash
   python -c "import secrets; print(secrets.token_hex(32))"
```

4. Run the server:

```bash
   uvicorn app.main:app --reload
```

5. Open `http://127.0.0.1:8000/docs` for interactive Swagger docs.

## API Endpoints

| Method | Endpoint       | Auth | Description                                                 |
| ------ | -------------- | ---- | ----------------------------------------------------------- |
| POST   | `/auth/signup` | No   | Create account, returns JWT                                 |
| POST   | `/auth/login`  | No   | Authenticate, returns JWT                                   |
| POST   | `/documents/`  | Yes  | Ingest text — chunks it, generates + stores embeddings      |
| POST   | `/chat/`       | Yes  | Retrieves relevant chunks, generates an answer via Groq LLM |

**Example — Chat:**

```json
POST /chat/
Authorization: Bearer <token>
{ "query": "What is FastAPI?" }
```

```json
{
  "answer": "FastAPI is a modern web framework...",
  "sources": ["FastAPI is a modern, fast web framework for building APIs..."]
}
```

## Indexing Choices

- `users.email` — unique index; prevents duplicate signups, speeds up login lookups
- `documents.owner_id` — speeds up fetching a user's documents
- `chunks.document_id` — speeds up fetching all chunks for a document
- `chunks.owner_id` — denormalized onto chunks (not just documents) so `/chat` can query a user's chunks directly, without joining through documents
- `error_logs.timestamp` — speeds up querying recent errors

## Retrieval Approach

Query and chunk text are embedded with the same local model, and matched via in-memory cosine similarity (NumPy), scoped to the authenticated user's own chunks. This was a deliberate choice to keep the pipeline simple and reliable within the time limit — at production scale, this would move to MongoDB Atlas Vector Search or a dedicated vector DB (Qdrant, Pinecone) for indexed similarity search.

## Error Handling

A custom `BaseHTTPMiddleware` catches unhandled exceptions, logs timestamp, endpoint, method, error message, stack trace, and authenticated user ID (if present) to the `error_logs` collection, and returns a generic JSON 500 response — never a raw traceback. Expected rejections (401, 400, etc.) are handled by FastAPI's own `HTTPException` and aren't logged as errors, since they're normal application behavior, not bugs.

## Testing Performed

All endpoints manually tested via Swagger UI and curl: signup/login (including duplicate email and wrong password), document ingestion (short text, long multi-chunk text, empty content), chat (with context and with no ingested documents), unauthenticated access rejection, and middleware verified against a real failure (invalid Groq API key) confirming all required log fields are captured correctly.

## Notes

- Used in-memory cosine similarity for retrieval instead of MongoDB Atlas Vector Search, to keep scope reliable within the time limit. At production scale, this would move to Atlas Vector Search or a dedicated vector DB.
- `owner_id` is deliberately duplicated on the `Chunk` model (not just `Document`) so `/chat` retrieval can query a user's chunks directly in one step, without joining through documents — a denormalization tradeoff for read performance.
- Good-to-have items (Redis, Kafka, Docker, background jobs, streaming responses, automated unit tests) were not implemented due to the 24-hour timeline. Instead, all endpoints were manually tested end-to-end via Swagger UI and curl, including edge cases (empty content, long multi-chunk documents, wrong password, duplicate signup, unauthenticated access) and a real failure scenario (invalid Groq API key) to verify the error-logging middleware captures all required fields correctly.
