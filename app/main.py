from fastapi import FastAPI
from app.database import init_db
from app.routers import auth,documents,chat
from app.middleware.error_logging import ErrorLoggingMiddleware

app = FastAPI(title="RAG Backend Assignment")
app.add_middleware(ErrorLoggingMiddleware)


@app.on_event("startup")
async def startup_event():
    await init_db()


app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(chat.router)

@app.get("/test-error")
async def test_error():
    raise ValueError("This is a deliberate test error")
@app.get("/")
async def root():
    return {"message": "RAG Backend is running"}