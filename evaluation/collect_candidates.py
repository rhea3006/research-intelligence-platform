import json
import requests
from pathlib import Path


BASE_URL = "http://localhost:8000"

OUTPUT_FILE = Path(__file__).parent / "candidates.json"


def get_lexical_results(query):
    response = requests.get(
        f"{BASE_URL}/search",
        params={
            "q": query,
            "limit": 10,
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json()["results"]


def get_semantic_results(query):
    response = requests.get(
        f"{BASE_URL}/semantic-search",
        params={
            "q": query,
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def get_hybrid_results(query):
    response = requests.get(
        f"{BASE_URL}/hybrid-search",
        params={
            "q": query,
            "limit": 10,
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json()["results"]


def main():
    with open(
        Path(__file__).parent / "queries.json",
        "r",
        encoding="utf-8",
    ) as f:
        queries = json.load(f)["queries"]

    evaluation_data = []

    for query in queries:
        print(f"\n{'=' * 60}")
        print(f"Query: {query}")
        print("=" * 60)

        lexical = get_lexical_results(query)
        semantic = get_semantic_results(query)
        hybrid = get_hybrid_results(query)

        print(f"Lexical results:  {len(lexical)}")
        print(f"Semantic results: {len(semantic)}")
        print(f"Hybrid results:   {len(hybrid)}")

        evaluation_data.append(
            {
                "query": query,
                "lexical": lexical,
                "semantic": semantic,
                "hybrid": hybrid,
            }
        )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            evaluation_data,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\n✅ Saved evaluation candidates to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()