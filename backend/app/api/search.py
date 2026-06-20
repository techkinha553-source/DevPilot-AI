from fastapi import APIRouter

from app.services.repository_store import (
    get_repository
)

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("/{repository_id}")
def search_files(
    repository_id: str,
    query: str
):
    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error":
            "Repository not found"
        }

    results = []

    for doc in repo["documents"]:
        if query.lower() in (
            doc["path"].lower()
            + doc["content"].lower()
        ):
            results.append(
                doc["path"]
            )

    return {
        "matches": results[:20]
    }