FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

ENV SERVICE_NAME=ai-inference
ENV SERVICE_VERSION=1.0.0
ENV MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2

WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install Python dependencies
RUN pip install \
    --no-cache-dir \
    --upgrade pip \
    -r requirements.txt

# Pre-download the ONNX model during image build
RUN python -c "\
import os; \
from huggingface_hub import snapshot_download; \
snapshot_download( \
    repo_id=os.environ['MODEL_NAME'], \
    allow_patterns=[ \
        'config.json', \
        'tokenizer.json', \
        'tokenizer_config.json', \
        'special_tokens_map.json', \
        'vocab.txt', \
        'onnx/model.onnx' \
    ] \
)"

# Copy the rest of the application
COPY . .

# Cloud Run injects the PORT environment variable
ENV PORT=8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]