from pydantic import BaseModel
from typing import Literal
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
    abstract: str | None = None
    authors: str | None = None
    categories: str
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

class HybridSearchResult(BaseModel):
    arxiv_id: str
    title: str
    abstract: str | None = None
    authors: str | None = None
    categories: str
    published_date: str | None = None

    relevance_score: int
    semantic_score: float
    hybrid_score: float

class HybridSearchResponse(BaseModel):
    results: list[HybridSearchResult]
    page: int
    limit: int
    total: int
    total_pages: int

class WorkspaceAnalysisRequest(BaseModel):
    paper_ids: list[str]
    analysis_type: Literal[ "compare", "literature_review", "research_gap", 
                           "beginner",]

    additional_prompt: str = ""

    analysis_depth: str

    writing_style: str

    output_format: str

class WorkspaceAnalysisResponse(BaseModel):
     analysis: str


class WorkspacePaper(BaseModel):
    arxiv_id: str
    title: str
    abstract: str
    authors: str
    categories: str
    published_date: str | None = None

class PaperSummaryRequest(BaseModel):
    arxiv_id: str

class PaperSummaryResponse(BaseModel):
    arxiv_id: str
    title: str
    summary: str

