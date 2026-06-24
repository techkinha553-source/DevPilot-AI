from fastapi import APIRouter
from app.services.repository_store import repositories

router = APIRouter()

@router.get("/repositories/{email}")
def get_repositories(email: str):

    result = []

    for repo_id, repo_data in repositories.items():

        if repo_data.get("owner") != email:
            continue

        result.append({
            "repository_id": repo_id,
            "summary": repo_data.get("summary", ""),
            "total_files": len(
                repo_data.get("documents", [])
            )
        })

    return result