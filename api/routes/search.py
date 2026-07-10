from fastapi import APIRouter
from api.models import ( SearchResponse,SemanticSearchResult,HybridSearchResponse)
from api.services.search_service import search_papers_service
from api.services.embedding_service import (semantic_search,hybrid_search,)
router = APIRouter()

@router.get("/search", response_model=SearchResponse)
def search(q: str, category: str | None = None, author: str | None = None ,year: int | None = None,
           sort: str = "relevance",page: int=1, limit: int=10):
    
    return hybrid_search(
        q=q,
        page=page,
        limit=limit,
        category=category,
        author=author,
        year=year,
        sort=sort,
    )

@router.get("/semantic-search")
def semantic_search_endpoint(q: str,response_model=list[SemanticSearchResult]):

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