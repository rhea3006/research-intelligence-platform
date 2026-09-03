import os
import random
import time

import requests


EMBEDDING_SERVICE_URL = os.getenv(
    "EMBEDDING_SERVICE_URL",
    "http://localhost:8080",
).rstrip("/")

EMBEDDING_ENDPOINT = f"{EMBEDDING_SERVICE_URL}/api/v1/embed"

TIMEOUT = 30
MAX_RETRIES = 3


class EmbeddingServiceError(Exception):
    """Raised when the embedding service cannot generate an embedding."""
    pass


def generate_embedding(text: str) -> list[float]:
    """
    Generate an embedding using the AI inference service.

    Retries temporary failures such as:
    - 429 Too Many Requests
    - 502 Bad Gateway
    - 503 Service Unavailable
    - 504 Gateway Timeout
    - network timeouts

    Permanent HTTP errors fail immediately.
    """

    for attempt in range(1, MAX_RETRIES + 1):

        try:
            print(
                f"Calling embedding service "
                f"(attempt {attempt}/{MAX_RETRIES}): "
                f"{EMBEDDING_ENDPOINT}"
            )

            response = requests.post(
                EMBEDDING_ENDPOINT,
                json={"text": text},
                timeout=TIMEOUT,
            )

            # --------------------------------------------------
            # Rate limited
            # --------------------------------------------------

            if response.status_code == 429:

                retry_after = response.headers.get("Retry-After")

                if retry_after:
                    try:
                        wait_time = float(retry_after)
                    except ValueError:
                        wait_time = 5
                else:
                    wait_time = min(2 ** (attempt - 1), 10)

                # Small random jitter
                wait_time += random.uniform(0, 1)

                print(
                    f"Embedding service rate limited request "
                    f"(429). Waiting {wait_time:.2f}s."
                )

                if attempt < MAX_RETRIES:
                    time.sleep(wait_time)
                    continue

                raise EmbeddingServiceError(
                    "Embedding service rate limited the request "
                    "after multiple retries."
                )

            # --------------------------------------------------
            # Temporary server-side failures
            # --------------------------------------------------

            if response.status_code in {502, 503, 504}:

                wait_time = min(2 ** (attempt - 1), 10)
                wait_time += random.uniform(0, 1)

                print(
                    f"Embedding service returned "
                    f"{response.status_code}. "
                    f"Waiting {wait_time:.2f}s."
                )

                if attempt < MAX_RETRIES:
                    time.sleep(wait_time)
                    continue

                raise EmbeddingServiceError(
                    f"Embedding service unavailable "
                    f"(HTTP {response.status_code})."
                )

            # --------------------------------------------------
            # Other HTTP errors
            # --------------------------------------------------

            response.raise_for_status()

            data = response.json()

            # --------------------------------------------------
            # Validate response
            # --------------------------------------------------

            if "embedding" not in data:
                raise EmbeddingServiceError(
                    "Embedding service response does not contain "
                    "'embedding'."
                )

            embedding = data["embedding"]

            if not isinstance(embedding, list):
                raise EmbeddingServiceError(
                    "Embedding returned by service is not a list."
                )

            if len(embedding) == 0:
                raise EmbeddingServiceError(
                    "Embedding service returned an empty embedding."
                )

            print(
                f"Embedding generated successfully "
                f"(dimensions={len(embedding)})"
            )

            return embedding

        # ------------------------------------------------------
        # Network timeout
        # ------------------------------------------------------

        except requests.Timeout:

            print(
                f"Embedding request timed out "
                f"(attempt {attempt}/{MAX_RETRIES})."
            )

            if attempt < MAX_RETRIES:
                wait_time = min(2 ** (attempt - 1), 10)
                wait_time += random.uniform(0, 1)
                time.sleep(wait_time)
                continue

            raise EmbeddingServiceError(
                "Embedding service request timed out."
            )

        # ------------------------------------------------------
        # Network-level request failure
        # ------------------------------------------------------

        except requests.RequestException as e:

            print(
                f"Embedding request failed "
                f"(attempt {attempt}/{MAX_RETRIES}): {e}"
            )

            if attempt < MAX_RETRIES:
                wait_time = min(2 ** (attempt - 1), 10)
                wait_time += random.uniform(0, 1)
                time.sleep(wait_time)
                continue

            raise EmbeddingServiceError(
                f"Embedding request failed: {e}"
            ) from e