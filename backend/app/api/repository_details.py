from fastapi import APIRouter, HTTPException

from app.services.repository_store import repositories

router = APIRouter()

@router.get("/repository/{repository_id}")

def get_repository(repository_id: str):

    repo = repositories.get(repository_id)
    if not repo:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )
    return {
        "repository_id": repository_id,
        "summary": repo.get("summary", ""),
        "total_files": len(
            repo.get("documents", [])
        ),
        "files": [
            doc.metadata.get(
                "source",
                "Unknown File"
            )
            for doc in repo.get(
                "documents",
                []
            )
        ],
        "health_score": 85
    }
