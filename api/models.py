from pydantic import BaseModel
from typing import Literal, List 
from datetime import (date, datetime)

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
    hybrid_score: float

class HybridSearchResponse(BaseModel):
    results: list[HybridSearchResult]
    page: int
    limit: int
    total: int
    total_pages: int

class WorkspaceAnalysisRequest(BaseModel):
    paper_ids: list[str]
    analysis_type: Literal[ "methodology", "literature_review", "critical_evaluation", 
                           "applications",]

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


# Analysis Management

class AnalysisCreateRequest(BaseModel):
    title: str | None = None

    paper_arxiv_ids: list[str]

    analysis_type: str

    analysis_depth: str

    writing_style: str

    output_format: str

    additional_instructions: str = ""

    generated_markdown: str | None = None

class AnalysisSummary(BaseModel):
    id: int

    title: str

    analysis_type: str

    created_at: datetime

class AnalysisResponse(BaseModel):
    id: int

    title: str

    paper_arxiv_ids: list[str]

    analysis_type: str

    analysis_depth: str

    writing_style: str

    output_format: str

    additional_instructions: str

    generated_markdown: str

    created_at: datetime


class DeleteAnalysisResponse(BaseModel):
    deleted: bool


class CreateAnalysisResponse(BaseModel):
    analysis_id: int
    message: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    user: UserResponse