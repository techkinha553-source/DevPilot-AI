from fastapi import APIRouter
from app.services.repository_store import (
    get_repository
)
from app.services.openai_service import (
    ask_codebase
)

router = APIRouter()

@router.post(
    "/repository/{repository_id}/assistant"
)
def repository_assistant(
    repository_id: str,
    request: dict
):

    repo = get_repository(repository_id)

    if not repo:
        return {
            "error": "Repository not found"
        }

    answer = ask_codebase(
        request["question"],
        repo["documents"]
    )

    return {
        "answer": answer
    }