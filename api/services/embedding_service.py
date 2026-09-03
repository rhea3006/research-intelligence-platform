from api.database import (get_papers_for_embedding,update_embedding_vector,
                          semantic_search_db)
from api.services.search_service import search_papers_service
from clients.embedding_client import generate_embedding

model = None

def create_paper_embedding(title, abstract):
    text = f"{title} {abstract}"
    print(f"Length: {len(text)}")
    return generate_embedding(text)

def backfill_embeddings():
    """
    Generate embeddings for papers that do not yet have one.

    Embeddings are generated sequentially to avoid overwhelming
    the inference service.
    """

    papers = get_papers_for_embedding()

    print(f"Found {len(papers)} papers requiring embeddings")

    if not papers:
        print("No papers require embedding.")
        return

    successful = 0
    failed = 0

    for index, paper in enumerate(papers, start=1):

        arxiv_id, title, abstract = paper

        print(
            f"[{index}/{len(papers)}] "
            f"Processing {arxiv_id}"
        )

        try:

            embedding = create_paper_embedding(
                title,
                abstract or "",
            )

            update_embedding_vector(
                arxiv_id,
                embedding,
            )

            successful += 1

            print(
                f"✅ Embedded {arxiv_id} "
                f"({len(embedding)} dimensions)"
            )

        except Exception as e:

            failed += 1

            print(
                f"❌ Failed {arxiv_id}: {e}"
            )

    print(
        f"Embedding backfill complete: "
        f"{successful} successful, "
        f"{failed} failed."
    )

def semantic_search(
    query,
    limit=10,
    category=None,
    author=None,
    year=None,
):
    """
    Perform semantic search using pgvector.
    """

    try:
        query_embedding = generate_embedding(query)

    except Exception as e:
        print(f"Semantic embedding generation failed: {e}")
        raise RuntimeError(
            "Semantic search is temporarily unavailable."
        ) from e

    results = semantic_search_db(
        query_embedding=query_embedding,
        limit=limit,
        category=category,
        author=author,
        year=year,
    )

    return [
        {
            "arxiv_id": row[0],
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
        semantic_results = semantic_search(q,limit=CANDIDATE_POOL_SIZE,category=category,
                                           author=author,year=year,)
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