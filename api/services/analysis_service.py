from api.database import (save_analysis,get_all_analyses, get_analysis_by_id,
delete_analysis,)
from api.services.auth_service import get_current_user
from fastapi import Depends


def create_analysis(request,current_user=Depends(get_current_user)):
    """
    Save a generated AI analysis.
    """

    analysis_id = save_analysis(
        user_id=current_user,
        title=request.title,
        paper_arxiv_ids=request.paper_arxiv_ids,
        analysis_type=request.analysis_type,
        analysis_depth=request.analysis_depth,
        writing_style=request.writing_style,
        output_format=request.output_format,
        additional_instructions=request.additional_instructions,
        generated_markdown=request.generated_markdown,
    )

    return {
        "analysis_id": analysis_id,
        "message": "Analysis saved successfully."
    }

def fetch_all_analyses(user_id):
    return get_all_analyses(user_id)


def fetch_analysis(analysis_id,user_id):
    return get_analysis_by_id(analysis_id, user_id)


def remove_analysis(analysis_id,user_id):
    deleted = delete_analysis(analysis_id,user_id)

    return {
        "deleted": deleted
    }