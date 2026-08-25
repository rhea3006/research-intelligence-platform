from fastapi import APIRouter
from api.models import (AnalysisCreateRequest,CreateAnalysisResponse,AnalysisSummary,
                        AnalysisResponse,DeleteAnalysisResponse)
from api.services.analysis_service import (create_analysis,fetch_all_analyses,
    fetch_analysis,remove_analysis,)
from api.services.auth_service import get_current_user
from fastapi import Depends

router = APIRouter(
    prefix="/analyses",
    tags=["Analyses"],
)


@router.post("", response_model= CreateAnalysisResponse)
def save_analysis(request: AnalysisCreateRequest, 
                  current_user = Depends(get_current_user)):
    """
    Save a generated AI analysis.
    """
    return create_analysis(request,current_user)

@router.get("",response_model= list[AnalysisSummary])
def get_analyses(current_user_id: int = Depends(get_current_user)):
    return fetch_all_analyses(current_user_id)


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(analysis_id: int,current_user = Depends(get_current_user)):
    return fetch_analysis(analysis_id,current_user)


@router.delete("/{analysis_id}", response_model=DeleteAnalysisResponse)
def delete_analysis(analysis_id: int,current_user = Depends(get_current_user)):
    return remove_analysis(analysis_id, current_user)