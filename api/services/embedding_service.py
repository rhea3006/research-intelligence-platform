from sentence_transformers import SentenceTransformer
from api.database import (get_papers_for_embedding,update_embedding, get_all_embeddings, 
                          search_papers)
from api.services.paper_service import search_papers_service
import numpy as np
import json

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text):
    return model.encode(text)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) *np.linalg.norm(b))

embedding = model.encode("machine learning")

def create_paper_embedding(title, abstract):

    text = f"{title} {abstract}"

    embedding = generate_embedding(text)

    return json.dumps(
        embedding.tolist()
    )

def backfill_embeddings():

    papers = get_papers_for_embedding()
    print(f"Found {len(papers)} papers")

    for paper in papers:
        arxiv_id = paper[0]
        title = paper[1]
        abstract = paper[2]
        embedding = create_paper_embedding(title,abstract)
        update_embedding(arxiv_id,embedding)
        print(f"Embedded {arxiv_id}")

def semantic_search(query):
    query_embedding = generate_embedding(query)
    papers = get_all_embeddings()
    results = []

    for paper in papers:
        arxiv_id = paper[0]
        title = paper[1]
        authors = paper[2]
        published_date = paper[3]
        paper_embedding = json.loads(paper[4])
        similarity = cosine_similarity( query_embedding, paper_embedding)

        results.append({"arxiv_id": arxiv_id,"title": title,"authors": authors,
                        "published_date": str(published_date),"similarity": float(similarity)})

    results.sort( key=lambda x: x["similarity"],reverse=True)
    return results[:10]

def hybrid_search(query):
    keyword_results = search_papers_service(q=query,page=1,limit=50)
    semantic_results = semantic_search(query)

    semantic_lookup = {}
    for paper in semantic_results:
        semantic_lookup[paper["arxiv_id"]] = paper["similarity"]

    results = []
    for paper in keyword_results:
        normalized_keyword = (paper["relevance_score"] / 8)
        semantic_score = semantic_lookup.get( paper["arxiv_id"],0)
        hybrid_score = (0.5 * normalized_keyword + 0.5 * semantic_score)

        paper["semantic_score"] = semantic_score
        paper["hybrid_score"] = hybrid_score

        results.append(paper)

    results.sort(key=lambda x: x["hybrid_score"], reverse=True)

    return results[:10]

if __name__ == "__main__":
    results = semantic_search("fake news detection")
    for result in results:
        print(result["title"],result["similarity"])