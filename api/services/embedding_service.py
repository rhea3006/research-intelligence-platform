from api.database import (get_papers_for_embedding,update_embedding_vector,semantic_search_db,)
from api.services.search_service import search_papers_service
from clients.embedding_client import generate_embedding
import numpy as np
import json
import os

model = None


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) *np.linalg.norm(b))

def create_paper_embedding(title, abstract):
    text = f"{title} {abstract}"
    print(f"Length: {len(text)}")
    return generate_embedding(text)

def backfill_embeddings():

    papers = get_papers_for_embedding()
    print(f"Found {len(papers)} papers")

    for paper in papers:
        arxiv_id, title, abstract = paper

        try:
            embedding = create_paper_embedding(title, abstract)
            update_embedding_vector(arxiv_id, embedding)
            print(f"Embedded {arxiv_id}")

        except Exception as e:
            print(f"Failed {arxiv_id}: {e}")


def semantic_search(query,limit=10):
    """
    Perform semantic search using pgvector cosine similarity.
    Returns the top matching papers.

    """
    query_embedding = generate_embedding(query)
    results = semantic_search_db(query_embedding,limit)


    return [
        {"arxiv_id": row[0],
         "title": row[1],
         "authors": row[2],
         "categories": row[3],
         "published_date": str(row[4]),
         "relevance_score": row[5],
         "similarity": float(row[6]),
         }
        for row in results
    ]

def hybrid_search(q,page=1,limit=10,category=None,author=None,year=None,sort="relevance",):

    from api.services.search_service import search_papers_service

    """
    Combine keyword and semantic search results
    using weighted score fusion.
    """

    CANDIDATE_POOL_SIZE = 50

    # Fetch a larger keyword candidate pool
    keyword_response = search_papers_service(
        q=q,
        page=1,
        limit=CANDIDATE_POOL_SIZE,
        category=category,
        author=author,
        year=year,
        sort=sort,
    )

    keyword_results = keyword_response["results"]

    # Top semantic matches
    try:
        semantic_results = semantic_search(
            q,
            limit=CANDIDATE_POOL_SIZE,
        )
    except Exception as e:
        print(f"Semantic search unavailable: {e}")
        semantic_results = []

    combined = {}
    
    RRF_K = 60
    for rank, paper in enumerate(keyword_results, start=1):
        combined[paper["arxiv_id"]] = {**paper,"rrf_score": 1 / (RRF_K + rank),}

    
    best_similarity = max((paper["similarity"] for paper in semantic_results),
                           default=0,)

    SEMANTIC_THRESHOLD = 0.70 * best_similarity

    for rank, paper in enumerate(semantic_results, start=1):

        if paper["similarity"] < SEMANTIC_THRESHOLD:
            continue

        arxiv_id = paper["arxiv_id"]

        if arxiv_id in combined:

            combined[arxiv_id]["rrf_score"] += 1 / (RRF_K + rank)

        else:

            combined[arxiv_id] = {
                **paper,
                "rrf_score": 1 / (RRF_K + rank),
            }

    for paper in combined.values():

        paper["hybrid_score"] = paper["rrf_score"]

        paper.pop("rrf_score", None)
        paper.pop("similarity", None)
        paper.pop("embedding", None)

    # Sort by hybrid relevance
    results = sorted(
        combined.values(),
        key=lambda x: x["hybrid_score"],
        reverse=True,
    )

    # Pagination
    start = (page - 1) * limit
    end = start + limit

    return {
        "results": results[start:end],
        "page": page,
        "limit": limit,
        "total": len(results),
        "total_pages": (len(results) + limit - 1) // limit,
    }


if __name__ == "__main__":
    print("Starting embedding backfill...")
    backfill_embeddings()
    print("Backfill complete.")