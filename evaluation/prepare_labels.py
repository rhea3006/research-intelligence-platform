import json
from pathlib import Path


INPUT_FILE = Path("evaluation/candidates.json")
OUTPUT_FILE = Path("evaluation/relevance_labels.json")


def prepare_labels():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    relevance_data = {}

    for item in candidates:
        query = item["query"]

        papers = {}

        # Collect lexical candidates
        for paper in item.get("lexical", []):
            papers[paper["arxiv_id"]] = {
                "arxiv_id": paper["arxiv_id"],
                "title": paper["title"],
                "abstract": paper.get("abstract"),
                "relevance": None,
            }

        # Collect semantic candidates
        for paper in item.get("semantic", []):
            arxiv_id = paper["arxiv_id"]

            if arxiv_id not in papers:
                papers[arxiv_id] = {
                    "arxiv_id": arxiv_id,
                    "title": paper["title"],
                    "abstract": None,
                    "relevance": None,
                }

        # Collect hybrid candidates
        for paper in item.get("hybrid", []):
            arxiv_id = paper["arxiv_id"]

            if arxiv_id not in papers:
                papers[arxiv_id] = {
                    "arxiv_id": arxiv_id,
                    "title": paper["title"],
                    "abstract": None,
                    "relevance": None,
                }

        relevance_data[query] = list(papers.values())

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(relevance_data, f, indent=2, ensure_ascii=False)

    print("=" * 60)
    print("Prepared relevance labeling file")
    print("=" * 60)

    for query, papers in relevance_data.items():
        print(f"{query}: {len(papers)} unique candidates")

    print()
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    prepare_labels()