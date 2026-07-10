from api.database import (get_papers_for_embedding,update_embedding_vector,semantic_search_db,)
from api.services.search_service import search_papers_service
import numpy as np
import json

model = None

def get_model():
    global model
    if model is None:
        from sentence_transformers import SentenceTransformer
        print("Loading embedding model...")
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return model

def generate_embedding(text):
    """Generate a sentence embedding for the given text."""
    return get_model().encode(text)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) *np.linalg.norm(b))

def create_paper_embedding(title, abstract):
    text = f"{title} {abstract}"
    return generate_embedding(text).tolist()

def backfill_embeddings():

    papers = get_papers_for_embedding()
    print(f"Found {len(papers)} papers")

    for paper in papers:
        arxiv_id = paper[0]
        title = paper[1]
        abstract = paper[2]
        embedding = create_paper_embedding(title,abstract)
        update_embedding_vector(arxiv_id, embedding)
        print(f"Embedded {arxiv_id}")


def semantic_search(query,limit=10):
    """
    Perform semantic search using pgvector cosine similarity.
    Returns the top matching papers.

    """
    query_embedding = generate_embedding(query).tolist()

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
    semantic_results = semantic_search(q, limit=30)

    combined = {}

    # Add keyword results
    for paper in keyword_results:
        combined[paper["arxiv_id"]] = {
            **paper,
            "keyword_score": paper["relevance_score"] / 8,
            "semantic_score": 0,
        }

    # Merge semantic results
    for paper in semantic_results:
        arxiv_id = paper["arxiv_id"]

        if arxiv_id in combined:
            combined[arxiv_id]["semantic_score"] = paper["similarity"]

        else:
            combined[arxiv_id] = {
                **paper,
                "keyword_score": 0,
                "semantic_score": paper["similarity"],
            }

    KEYWORD_WEIGHT = 0.5
    SEMANTIC_WEIGHT = 0.5
    
    # Compute hybrid score
    for paper in combined.values():

        paper["hybrid_score"] = (
            KEYWORD_WEIGHT * paper["keyword_score"]
            + SEMANTIC_WEIGHT * paper["semantic_score"]
        )

        paper.pop("embedding", None)


        # Remove internal fields
        paper.pop("embedding", None)
        paper.pop("keyword_score", None)
        paper.pop("similarity", None)

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