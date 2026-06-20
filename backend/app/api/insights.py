from collections import Counter
from fastapi import APIRouter

from app.services.repository_store import (
    get_repository
)

router = APIRouter(
    prefix="/insights",
    tags=["Insights"]
)


@router.get("/{repository_id}")
def get_insights(repository_id: str):

    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error":
            "Repository not found"
        }

    documents = repo["documents"]

    file_types = Counter()

    for doc in documents:

        path = doc["path"]

        if "." in path:

            extension = (
                path.split(".")[-1]
                .lower()
            )

            file_types[
                extension
            ] += 1

    return {
        "repository_id":
            repository_id,
        "total_files":
            len(documents),
        "file_types":
            dict(file_types)
    }
