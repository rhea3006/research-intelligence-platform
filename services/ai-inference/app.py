from fastapi import FastAPI
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from model import get_model, generate_embedding
from fastapi import FastAPI, HTTPException
import logging
import os
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading embedding model...")
    get_model()
    logger.info("Embedding model loaded.")
    yield
    

app = FastAPI(title="Project Alpha AI Inference Service")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
SERVICE_NAME = "ai-inference"
SERVICE_VERSION = "1.0.0"

class EmbeddingRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Input text for embedding generation."
    )


class EmbeddingResponse(BaseModel):
    embedding: list[float]
    dimensions: int
    model: str

@app.get("/")
def root():

    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "description": "Embedding inference microservice",
        "documentation": "/docs",
        "health": "/health",
    }

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "model": MODEL_NAME,
    }

@app.post("/api/v1/embed", response_model=EmbeddingResponse)
def embed(request: EmbeddingRequest):
    try:
        embedding = generate_embedding(request.text)

        logger.info(
            "Successfully generated embedding (%d dimensions).",
            len(embedding),
        )

        return EmbeddingResponse(
            embedding=embedding.tolist(),
            dimensions=len(embedding),
            model=MODEL_NAME,
        )

    except Exception:
        logger.exception("Embedding generation failed.")

        raise HTTPException(
            status_code=500,
            detail="Failed to generate embedding."
        )