from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.services.repository_metadata import load_metadata
from app.services.repository_stats import calculate_repository_stats

router = APIRouter()


@router.get("/repository/{repository_id}")
def repository_info(repository_id: str):
    repo_path = Path("app/uploads") / repository_id

    if not repo_path.exists():
        raise HTTPException(status_code=404, detail="Repository not found.")

    metadata = load_metadata(repo_path)
    stats = calculate_repository_stats(str(repo_path))

    return {
        "metadata": metadata,
        "stats": stats,
    }