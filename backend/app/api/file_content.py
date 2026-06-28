from fastapi import APIRouter, HTTPException
from app.services.repository_store import repositories

router = APIRouter()

@router.get("/repository/{repository_id}/file")
def get_file_content(
    repository_id: str,
    path: str
):
    repo = repositories.get(repository_id)

    if not repo:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    documents = repo.get("documents", [])

    for doc in documents:

        source = doc.metadata.get(
            "source",
            ""
        )

        if source == path:
            return {
                "content": doc.page_content
            }

    raise HTTPException(
        status_code=404,
        detail="File not found"
    )