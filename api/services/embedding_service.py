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


def semantic_search(query):

    query_embedding = generate_embedding(query).tolist()

    results = semantic_search_db(query_embedding)

    papers = []

    for row in results:

        papers.append(
            {
                "arxiv_id": row[0],
                "title": row[1],
                "authors": row[2],
                "published_date": str(row[3]),
                "similarity": float(row[4]),
            }
        )

    return papers

def hybrid_search(q,page=1,limit=10,category=None,author=None, year=None,
                  sort="relevance",):
   
    
    from api.services.search_service import search_papers_service

    keyword_response = search_papers_service(
        q=q,
        page=page,
        limit=limit,
        category=category,
        author=author,
        year=year,
        sort=sort,
    )

    keyword_results = keyword_response["results"]
    semantic_results = semantic_search(q)

    combined = {}
    for paper in keyword_results:
        combined[paper["arxiv_id"]] = {
            **paper,
            "keyword_score": paper["relevance_score"] / 8,
            "semantic_score": 0,
        }

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
    
    print(len(keyword_results))
    print(len(semantic_results))
    print(len(combined))

    for paper in combined.values():
        paper["hybrid_score"] = (
            0.5 * paper["keyword_score"]
            + 0.5 * paper["semantic_score"]
        )

    results = list(combined.values())
    results.sort(key=lambda x: x["hybrid_score"],reverse=True,)

    return {"results": results[:limit],"page": page,"limit": limit,
            "total": len(results),"total_pages": (len(results) + limit - 1) // limit,}




if __name__ == "__main__":
    print("Starting embedding backfill...")
    backfill_embeddings()
    print("Backfill complete.")