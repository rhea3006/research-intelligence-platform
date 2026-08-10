import os
import time
import requests

EMBEDDING_SERVICE_URL = os.getenv(
    "EMBEDDING_SERVICE_URL",
    "http://localhost:8080",
)

TIMEOUT = 60   # 60 seconds is enough


def generate_embedding(text: str) -> list[float]:
    """
    Generate an embedding using the AI inference service.
    """
    print(f"Calling: {EMBEDDING_SERVICE_URL}/api/v1/embed")

    for attempt in range(3):
        try:
            response = requests.post(
                f"{EMBEDDING_SERVICE_URL}/api/v1/embed",
                json={"text": text},
                timeout=TIMEOUT,
            )

            response.raise_for_status()

            return response.json()["embedding"]

        except requests.RequestException as e:
            print(f"Embedding request failed (attempt {attempt + 1}/3): {e}")

            if hasattr(e, "response") and e.response is not None:
                print("Status:", e.response.status_code)
                print("Body:", e.response.text[:500])

            if attempt == 2:
                raise

            time.sleep(2 ** attempt)