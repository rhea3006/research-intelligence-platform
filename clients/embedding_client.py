import os
import requests

EMBEDDING_SERVICE_URL = os.getenv(
    "EMBEDDING_SERVICE_URL",
    "http://localhost:8080",
)

TIMEOUT = 300


def generate_embedding(text: str) -> list[float]:
    """
    Generate an embedding using the AI inference service.
    """
    print("Calling:", f"{EMBEDDING_SERVICE_URL}/api/v1/embed")
    response = requests.post(
    f"{EMBEDDING_SERVICE_URL}/api/v1/embed",
    json={"text": text},
    timeout=TIMEOUT,
    )

    print("Status:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text[:500])

    response.raise_for_status()

    data = response.json()

    return data["embedding"]