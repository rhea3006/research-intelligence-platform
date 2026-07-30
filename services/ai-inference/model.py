import os
from pathlib import Path
import logging
import numpy as np
import onnxruntime as ort
from huggingface_hub import snapshot_download
from transformers import AutoTokenizer

logger = logging.getLogger(__name__)


MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "sentence-transformers/all-MiniLM-L6-v2",
)


MAX_SEQUENCE_LENGTH = 256
ONNX_MODEL_PATH = Path("onnx") / "model.onnx"

tokenizer = None
session = None
model_path = None


def download_model():
    """
    Downloads only the files required for ONNX inference.
    """

    return snapshot_download(
        repo_id=MODEL_NAME,
        allow_patterns=[
            "config.json",
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "vocab.txt",
            "onnx/model.onnx",
        ],
    )


def load_tokenizer(model_path):
    """
    Loads the tokenizer.
    """
    return AutoTokenizer.from_pretrained(model_path)


def load_onnx_session(model_path):
    """
    Loads the ONNX Runtime session.
    """
    onnx_path = Path(model_path) / ONNX_MODEL_PATH

    return ort.InferenceSession(
        str(onnx_path),
        providers=["CPUExecutionProvider"],
    )


def initialize():
    """
    Loads everything once during startup.
    """
    global tokenizer
    global session
    global model_path

    if tokenizer is not None and session is not None:
        return

    logger.info("Downloading ONNX model...")

    if model_path is None:
        model_path = download_model()

    
    logger.info("Loading tokenizer...")
    tokenizer = load_tokenizer(model_path)
    logger.info("Loading ONNX Runtime session...")
    session = load_onnx_session(model_path)
    logger.info("ONNX embedding model initialized successfully.")

def tokenize(text: str) -> dict[str, np.ndarray]:
    """
    Tokenizes the input text for the ONNX model.
    """

    initialize()

    encoded = tokenizer(
        text,
        return_tensors="np",
        padding=True,
        truncation=True,
        max_length=MAX_SEQUENCE_LENGTH,
    )

    inputs = {
        "input_ids": encoded["input_ids"].astype(np.int64),
        "attention_mask": encoded["attention_mask"].astype(np.int64),
    }

    if "token_type_ids" in encoded:
        inputs["token_type_ids"] = encoded["token_type_ids"].astype(np.int64)

    return inputs

def run_inference(
    inputs: dict[str, np.ndarray],
) -> np.ndarray:
    """
    Runs the ONNX model and returns token embeddings.
    """

    initialize()

    outputs = session.run(
        None,
        inputs,
    )

    return outputs[0]

def mean_pool(
    token_embeddings: np.ndarray,
    attention_mask: np.ndarray,
) -> np.ndarray:
    """
    Applies attention-mask-aware mean pooling to obtain a sentence embedding.
    """

    mask = np.expand_dims(attention_mask, axis=-1)

    masked_embeddings = token_embeddings * mask

    summed = np.sum(masked_embeddings, axis=1)

    counts = np.clip(np.sum(mask, axis=1), a_min=1e-9, a_max=None)

    return summed / counts

def normalize(
    embedding: np.ndarray,
) -> np.ndarray:
    """
    Applies L2 normalization to the sentence embedding.
    """

    norm = np.linalg.norm(
        embedding,
        axis=1,
        keepdims=True,
    )

    norm = np.clip(norm, a_min=1e-12, a_max=None)

    return embedding / norm

def generate_embedding(text: str) -> np.ndarray:
    """
    Generates a normalized sentence embedding.
    """

    if not text or not text.strip():
        raise ValueError("Input text cannot be empty.")

    inputs = tokenize(text)

    token_embeddings = run_inference(inputs)

    sentence_embedding = mean_pool(
        token_embeddings,
        inputs["attention_mask"],
    )

    sentence_embedding = normalize(sentence_embedding)

    return sentence_embedding[0]