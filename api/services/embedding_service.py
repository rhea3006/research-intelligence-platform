from sentence_transformers import SentenceTransformer
from api.database import (get_papers_for_embedding,update_embedding, get_all_embeddings)
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

if __name__ == "__main__":
    results = semantic_search("fake news detection")
    for result in results:
        print(result["title"],result["similarity"])