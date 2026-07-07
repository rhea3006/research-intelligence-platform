from fastapi import APIRouter
from api.models import SearchResponse
from api.services.search_service import search_papers_service

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
def search(q: str, category: str | None = None, author: str | None = None ,year: int | None = None,
           sort: str = "relevance",page: int=1, limit: int=10):
    
    return search_papers_service(q=q, page=page, limit=limit, category=category,
                                  author=author,year=year, sort=sort)