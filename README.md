# RAG Backend Assignment

A FastAPI backend implementing JWT authentication and a Retrieval-Augmented Generation (RAG) pipeline. Users can securely authenticate, ingest text documents, and ask questions based on their uploaded documents. The application retrieves relevant document chunks using semantic search and generates answers using an LLM.

## Live Demo

**GitHub Repository:**  
https://github.com/SamrudhiTM/rag_backend

**Live API:**  
https://rag-backend-v03r.onrender.com

**Swagger Documentation:**  
https://rag-backend-v03r.onrender.com/docs

> **Note:** The application is deployed on Render's free tier. If the service has been idle, the first request may take 30–60 seconds to start.

---

## Tech Stack

- FastAPI
- MongoDB (Motor + Beanie ODM)
- JWT Authentication (python-jose)
- Password Hashing (Passlib + bcrypt)
- Google Gemini Embeddings API (`gemini-embedding-001`)
- Groq (`llama-3.1-8b-instant`)
- NumPy (Cosine Similarity)

---

## Features

- JWT-based Signup & Login
- Secure password hashing
- Text document ingestion
- Automatic document chunking
- Semantic embeddings using Gemini Embeddings
- Context retrieval using cosine similarity
- RAG-powered chat endpoint
- Global exception logging middleware
- Interactive Swagger API documentation

---

## Setup

```bash
git clone https://github.com/SamrudhiTM/rag_backend.git
cd rag_backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Create a `.env` file from `.env.example` and configure:

```env
MONGO_URI=
MONGO_DB_NAME=

JWT_SECRET=
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

GROQ_API_KEY=
GEMINI_API_KEY=
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Register a new user |
| POST | `/auth/login` | Login and receive JWT |
| POST | `/documents/` | Ingest a text document |
| POST | `/chat/` | Ask questions about uploaded documents |

### Using the Hosted API

1. Register using `/auth/signup`
2. Login using `/auth/login`
3. Copy the JWT token.
4. Click **Authorize** in Swagger and enter:

```
Bearer <your_jwt_token>
```

5. Upload a document using `/documents/`
6. Ask questions using `/chat/`

---

## RAG Pipeline

```
Document
    │
    ▼
Chunking
    │
    ▼
Gemini Embeddings
    │
    ▼
MongoDB

User Query
    │
    ▼
Gemini Embedding
    │
    ▼
Cosine Similarity
    │
    ▼
Top Relevant Chunks
    │
    ▼
Groq LLM
    │
    ▼
Final Response
```

---

## Database Indexes

| Collection | Index | Purpose |
|------------|-------|---------|
| users | `email` (unique) | Fast login & prevents duplicate accounts |
| documents | `owner_id` | Retrieve a user's documents |
| chunks | `owner_id` | Retrieve authenticated user's chunks |
| chunks | `document_id` | Retrieve document chunks |
| error_logs | `timestamp` | Query recent errors efficiently |

---

## Retrieval Strategy

Documents are split into smaller chunks and embedded using **Google Gemini Embeddings API**. During chat, the user's query is embedded using the same model, cosine similarity is calculated against the authenticated user's stored chunk embeddings, and the most relevant chunks are provided as context to the Groq LLM.

For this assignment, cosine similarity is computed within the application because the dataset is small. For larger datasets, MongoDB Atlas Vector Search or a dedicated vector database (such as Pinecone, Qdrant, or Weaviate) would provide better scalability.

---

## Error Handling

A custom FastAPI middleware catches unhandled exceptions and stores them in the `error_logs` collection with:

- Timestamp
- Endpoint
- HTTP Method
- Error Message
- Stack Trace
- Authenticated User ID (if available)

The API returns a generic HTTP 500 response without exposing internal implementation details.

---

## Future Improvements

- MongoDB Atlas Vector Search
- Redis caching
- Background document ingestion
- Docker & Docker Compose
- Streaming LLM responses
- Unit tests

---

## Design Decision

Google Gemini Embeddings API was chosen for semantic embedding generation instead of a locally hosted embedding model. This keeps the application lightweight, reduces server memory usage, and makes deployment on Render's free tier reliable while maintaining high-quality semantic retrieval.
