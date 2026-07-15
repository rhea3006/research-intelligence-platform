from fastapi import APIRouter
from fastapi import HTTPException
from api.services.workspace_service import (analyze_workspace_service,summarize_paper_service,)
from api.models import(WorkspaceAnalysisRequest,WorkspaceAnalysisResponse,
                       PaperSummaryRequest,PaperSummaryResponse)

router = APIRouter()

@router.post("/workspace/analyze",response_model=WorkspaceAnalysisResponse,)
def analyze_workspace(request: WorkspaceAnalysisRequest,):
    return analyze_workspace_service(request)

@router.post( "/workspace/summarize",response_model=PaperSummaryResponse,)
def summarize_paper(request: PaperSummaryRequest):
    try:
        return summarize_paper_service(request.arxiv_id)

    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))