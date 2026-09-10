from fastapi import APIRouter, Query
from api.models import ( SearchResponse,SemanticSearchResult,HybridSearchResponse,
                        ChunkRetrievalResult)
from api.services.search_service import search_papers_service
from api.services.embedding_service import (semantic_search,hybrid_search,)
from api.services.retrieval_service import retrieve_chunks
router = APIRouter()

@router.get("/search", response_model=SearchResponse)
def search(
    q: str,
    category: str | None = None,
    author: str | None = None,
    year: int | None = None,
    sort: str = "relevance",
    page: int = 1,
    limit: int = 10,
):
    return search_papers_service(
        q=q,
        page=page,
        limit=limit,
        category=category,
        author=author,
        year=year,
        sort=sort,
    )

@router.get( "/semantic-search",response_model=list[SemanticSearchResult],)
def semantic_search_endpoint(q: str):
    return semantic_search(q)

@router.get("/hybrid-search",response_model=HybridSearchResponse)
def hybrid_search_endpoint(
    q: str,
    category: str | None = None,
    author: str | None = None,
    year: int | None = None,
    sort: str = "relevance",
    page: int = 1,
    limit: int = 10,
):
    return hybrid_search(
        q=q,
        page=page,
        limit=limit,
        category=category,
        author=author,
        year=year,
        sort=sort,
    )

@router.get(
    "/retrieval/chunks",
    response_model=list[ChunkRetrievalResult],
)
def retrieve_chunks_endpoint(
    q: str,
    limit: int = Query(default=5, ge=1, le=50),
    arxiv_id: str | None = None,
):
    return retrieve_chunks(
        query=q,
        limit=limit,
        arxiv_id=arxiv_id,
    )