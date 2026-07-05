from pydantic import BaseModel
from datetime import date

class PaperSummary(BaseModel):
    arxiv_id : str
    title : str

class PaperDetail(BaseModel):
    arxiv_id : str
    title: str
    abstract: str | None= None
    authors: str | None = None
    categories: str | None = None
    arxiv_url: str | None = None
    published_date: str | None = None
    updated_date: date | None = None

class SearchResult(BaseModel):
    arxiv_id: str
    title: str
    authors: str | None = None
    published_date: str | None = None
    relevance_score: int

class RelatedPaper(BaseModel):
    arxiv_id: str
    title: str
    authors: str | None = None
    published_date: date | None = None
    similarity_score: int

class PaperWithRelated(BaseModel):
    paper : PaperDetail
    related_papers: list[RelatedPaper]

class SemanticSearchResult(BaseModel):
    arxiv_id: str
    title: str
    authors: str
    published_date: str | None
    similarity: float

class SearchResponse(BaseModel):
    results: list[SearchResult]
    page: int
    limit: int
    total: int
    total_pages: int