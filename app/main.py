from fastapi import FastAPI
from app.database import create_indexes
from app.routers import auth

app = FastAPI(title="RAG Backend Assignment")


@app.on_event("startup")
async def startup_event():
    await create_indexes()


app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "RAG Backend is running"}