from fastapi import APIRouter

from app.services.repository_store import (
    get_repository
)

from app.services.repository_stats import (
    detect_stack
)

router = APIRouter(
    prefix="/architecture",
    tags=["Architecture"]
)


@router.get("/{repository_id}")
def architecture(
    repository_id: str
):

    repo = get_repository(
        repository_id
    )

    if not repo:

        return {
            "error":
            "Repository not found"
        }

    return detect_stack(
        repo["documents"]
    )