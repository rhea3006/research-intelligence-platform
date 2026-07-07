from io import BytesIO
import requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from api.database import get_paper_by_id
from api.models import (PaperSummary,PaperWithRelated,RelatedPaper,)
from api.services.paper_service import (get_all_papers_service, get_paper_with_related_service,
                                        get_related_papers_service,)

router = APIRouter()

@router.get("/papers", response_model=list[PaperSummary])
def get_papers(page: int = 1, limit: int = 10):
    return get_all_papers_service(page, limit)

@router.get("/papers/{arxiv_id}", response_model=PaperWithRelated)
def get_paper(arxiv_id: str):
    return get_paper_with_related_service(arxiv_id)

@router.get("/papers/{arxiv_id}/related", response_model=list[RelatedPaper])
def related_papers(arxiv_id: str):
    return get_related_papers_service(arxiv_id)

@router.get("/papers/{arxiv_id}/download")
def download_paper(arxiv_id: str):
    paper = get_paper_by_id(arxiv_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    pdf_url = paper[7]
    if not pdf_url.endswith(".pdf"):
        pdf_url += ".pdf"

    response = requests.get(pdf_url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="PDF not found")

    return StreamingResponse( BytesIO(response.content),media_type="application/pdf",
                             headers={"Content-Disposition":f'attachment; filename="{arxiv_id}.pdf"'},)