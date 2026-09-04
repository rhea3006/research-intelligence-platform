import json
import math
from pathlib import Path


CANDIDATES_FILE = Path("evaluation/candidates.json")
LABELS_FILE = Path("evaluation/relevance_labels.json")


def precision_at_k(ranked_ids, relevance, k):
    top_k = ranked_ids[:k]

    if not top_k:
        return 0.0

    relevant = sum(
        1 for arxiv_id in top_k
        if relevance.get(arxiv_id, 0) >= 2
    )

    return relevant / len(top_k)


def recall_at_k(ranked_ids, relevance, k):
    top_k = ranked_ids[:k]

    total_relevant = sum(
        1 for score in relevance.values()
        if score >= 2
    )

    if total_relevant == 0:
        return 0.0

    retrieved_relevant = sum(
        1 for arxiv_id in top_k
        if relevance.get(arxiv_id, 0) >= 2
    )

    return retrieved_relevant / total_relevant


def reciprocal_rank(ranked_ids, relevance):
    for rank, arxiv_id in enumerate(ranked_ids, start=1):
        if relevance.get(arxiv_id, 0) >= 2:
            return 1 / rank

    return 0.0


def dcg_at_k(ranked_ids, relevance, k):
    score = 0.0

    for rank, arxiv_id in enumerate(ranked_ids[:k], start=1):
        rel = relevance.get(arxiv_id, 0)

        score += (2**rel - 1) / math.log2(rank + 1)

    return score


def ndcg_at_k(ranked_ids, relevance, k):
    actual_dcg = dcg_at_k(ranked_ids, relevance, k)

    ideal_ids = sorted(
        relevance,
        key=lambda x: relevance[x],
        reverse=True,
    )

    ideal_dcg = dcg_at_k(ideal_ids, relevance, k)

    if ideal_dcg == 0:
        return 0.0

    return actual_dcg / ideal_dcg


def get_ids(results):
    return [paper["arxiv_id"] for paper in results]


def main():

    with open(CANDIDATES_FILE, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    with open(LABELS_FILE, "r", encoding="utf-8") as f:
        labels = json.load(f)

    methods = ["lexical", "semantic", "hybrid"]

    metrics = {
        method: {
            "precision@5": [],
            "precision@10": [],
            "recall@10": [],
            "mrr": [],
            "ndcg@10": [],
        }
        for method in methods
    }

    for item in candidates:

        query = item["query"]

        relevance = {
            paper["arxiv_id"]: paper["relevance"]
            for paper in labels[query]
            if paper["relevance"] is not None
        }

        print("\n" + "=" * 70)
        print(f"Query: {query}")
        print("=" * 70)

        for method in methods:

            ranked_ids = get_ids(item[method])

            p5 = precision_at_k(
                ranked_ids,
                relevance,
                5,
            )

            p10 = precision_at_k(
                ranked_ids,
                relevance,
                10,
            )

            r10 = recall_at_k(
                ranked_ids,
                relevance,
                10,
            )

            mrr = reciprocal_rank(
                ranked_ids,
                relevance,
            )

            ndcg = ndcg_at_k(
                ranked_ids,
                relevance,
                10,
            )

            metrics[method]["precision@5"].append(p5)
            metrics[method]["precision@10"].append(p10)
            metrics[method]["recall@10"].append(r10)
            metrics[method]["mrr"].append(mrr)
            metrics[method]["ndcg@10"].append(ndcg)

            print(
                f"{method.capitalize():<10} "
                f"P@5={p5:.3f} | "
                f"P@10={p10:.3f} | "
                f"R@10={r10:.3f} | "
                f"MRR={mrr:.3f} | "
                f"NDCG@10={ndcg:.3f}"
            )

    print("\n\n" + "=" * 70)
    print("FINAL RETRIEVAL EVALUATION")
    print("=" * 70)

    for method in methods:

        print(f"\n{method.upper()}")

        for metric, values in metrics[method].items():
            average = sum(values) / len(values)

            print(
                f"{metric:<15}: {average:.4f}"
            )


if __name__ == "__main__":
    main()