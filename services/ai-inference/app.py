from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from model import get_model, generate_embedding
import os
import psutil

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading embedding model...")
    get_model()
    print("Embedding model loaded.")
    yield
    process = psutil.Process(os.getpid())
    print(f"Memory after model load: {process.memory_info().rss / 1024 / 1024:.1f} MB")

app = FastAPI(title="Project Alpha AI Inference Service")


class EmbeddingRequest(BaseModel):
    text: str


class EmbeddingResponse(BaseModel):
    embedding: list[float]


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/embed", response_model=EmbeddingResponse)
def embed(request: EmbeddingRequest):
    embedding = generate_embedding(request.text)

    return EmbeddingResponse(
        embedding=embedding.tolist()
    )