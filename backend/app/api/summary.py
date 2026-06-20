from fastapi import APIRouter

from app.services.repository_store import (
    get_repository
)

router = APIRouter()


@router.get("/summary/{repository_id}")
def repository_summary(
    repository_id: str
):
    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error": "Repository not found"
        }

    return repo["summary"]