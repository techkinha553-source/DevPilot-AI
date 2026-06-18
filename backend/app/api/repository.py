from pathlib import Path
import shutil

from fastapi import APIRouter, HTTPException

from app.services.repository_metadata import load_metadata
from app.services.repository_stats import calculate_repository_stats

router = APIRouter()

UPLOAD_DIR = Path("app/uploads")


@router.get("/repositories")
def list_repositories():
    repositories = []

    if not UPLOAD_DIR.exists():
        return {"repositories": repositories}

    for repo_folder in UPLOAD_DIR.iterdir():
        if repo_folder.is_dir():
            try:
                metadata = load_metadata(repo_folder)
                repositories.append(metadata)
            except Exception:
                pass

    return {"repositories": repositories}


@router.get("/repository/{repository_id}")
def repository_info(repository_id: str):
    repo_path = UPLOAD_DIR / repository_id

    if not repo_path.exists():
        raise HTTPException(status_code=404, detail="Repository not found.")

    metadata = load_metadata(repo_path)
    stats = calculate_repository_stats(str(repo_path))

    return {
        "metadata": metadata,
        "stats": stats,
    }


@router.delete("/repository/{repository_id}")
def delete_repository(repository_id: str):
    repo_path = UPLOAD_DIR / repository_id

    if not repo_path.exists():
        raise HTTPException(status_code=404, detail="Repository not found.")

    shutil.rmtree(repo_path)

    zip_file = UPLOAD_DIR / f"{repository_id}.zip"
    if zip_file.exists():
        zip_file.unlink()

    return {
        "message": "Repository deleted successfully"
    }