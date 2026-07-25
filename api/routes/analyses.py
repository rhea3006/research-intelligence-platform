from fastapi import APIRouter
from api.models import (AnalysisCreateRequest,CreateAnalysisResponse,AnalysisSummary,
                        AnalysisResponse,DeleteAnalysisResponse)
from api.services.analysis_service import (create_analysis,fetch_all_analyses,
    fetch_analysis,remove_analysis,)

router = APIRouter(
    prefix="/analyses",
    tags=["Analyses"],
)


@router.post("", response_model= CreateAnalysisResponse)
def save_analysis(request: AnalysisCreateRequest):
    """
    Save a generated AI analysis.
    """
    return create_analysis(request)

@router.get("",response_model= list[AnalysisSummary])
def get_analyses():
    return fetch_all_analyses()


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(analysis_id: int):
    return fetch_analysis(analysis_id)


@router.delete("/{analysis_id}", response_model=DeleteAnalysisResponse)
def delete_analysis(analysis_id: int):
    return remove_analysis(analysis_id)