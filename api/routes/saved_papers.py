from fastapi import APIRouter, Depends

from api.services.auth_service import get_current_user
from api.database import (
    get_saved_papers,
    save_paper_for_user,
    remove_saved_paper,
)

router = APIRouter(
    prefix="/saved-papers",
    tags=["Saved Papers"],
)


@router.get("")
def fetch_saved_papers(
    current_user: int = Depends(get_current_user),
):
    return get_saved_papers(current_user)


@router.post("/{arxiv_id}")
def save_paper(
    arxiv_id: str,
    current_user: int = Depends(get_current_user),
):
    save_paper_for_user(current_user, arxiv_id)

    return {
        "message": "Paper saved successfully"
    }


@router.delete("/{arxiv_id}")
def remove_paper(
    arxiv_id: str,
    current_user: int = Depends(get_current_user),
):
    remove_saved_paper(current_user, arxiv_id)

    return {
        "message": "Paper removed successfully"
    }