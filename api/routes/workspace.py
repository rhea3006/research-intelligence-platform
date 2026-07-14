from fastapi import APIRouter
from api.services.workspace_service import (analyze_workspace_service,)
from api.models import(  WorkspaceAnalysisRequest,WorkspaceAnalysisResponse)

router = APIRouter()

@router.post("/workspace/analyze",response_model=WorkspaceAnalysisResponse,)
def analyze_workspace(request: WorkspaceAnalysisRequest,):
    return analyze_workspace_service(request)