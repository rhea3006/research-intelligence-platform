from fastapi import APIRouter, HTTPException, Depends

from api.services.workspace_service import (
    analyze_workspace_service,
    summarize_paper_service,
)

from api.services.auth_service import get_current_user

from api.models import (
    WorkspaceAnalysisRequest,
    WorkspaceAnalysisResponse,
    PaperSummaryRequest,
    PaperSummaryResponse,
)

router = APIRouter()


@router.post(
    "/workspace/analyze",
    response_model=WorkspaceAnalysisResponse,
)
def analyze_workspace(
    request: WorkspaceAnalysisRequest,
    current_user: int = Depends(get_current_user),
):
    return analyze_workspace_service(request, current_user)


@router.post(
    "/workspace/summarize",
    response_model=PaperSummaryResponse,
)
def summarize_paper(
    request: PaperSummaryRequest,
    current_user: int = Depends(get_current_user),
):
    try:
        return summarize_paper_service(
            request.arxiv_id,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )