import os
import requests

EMBEDDING_SERVICE_URL = os.getenv(
    "EMBEDDING_SERVICE_URL",
    "http://localhost:8080",
)

TIMEOUT = 30


def generate_embedding(text: str) -> list[float]:
    """
    Generate an embedding using the AI inference service.
    """

    response = requests.post(
        f"{EMBEDDING_SERVICE_URL}/api/v1/embed",
        json={"text": text},
        timeout=TIMEOUT,
    )

    response.raise_for_status()

    data = response.json()

    return data["embedding"]