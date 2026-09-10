from api.database import semantic_chunk_search
from clients.embedding_client import generate_embedding


def retrieve_chunks(
    query: str,
    limit: int = 5,
    arxiv_id: str | None = None,
):
    """
    Retrieve the most semantically relevant paper chunks
    for a natural-language query.

    If arxiv_id is provided:
        Search only within that paper.

    Otherwise:
        Search across all embedded paper chunks.
    """

    query_embedding = generate_embedding(query)

    results = semantic_chunk_search(
        query_embedding=query_embedding,
        limit=limit,
        arxiv_id=arxiv_id,
    )

    return [
        {
            "chunk_id": row[0],
            "arxiv_id": row[1],
            "chunk_index": row[2],
            "section_chunk_index": row[3],
            "section": row[4],
            "text": row[5],
            "similarity": float(row[6]),
        }
        for row in results
    ]