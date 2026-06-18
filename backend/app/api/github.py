from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from pathlib import Path
from git import Repo

from app.services.code_reader import read_repository
from app.services.parser import scan_repository
from app.services.rag_builder import build_vector_store
from app.services.repository_store import save_repository

router = APIRouter()

UPLOAD_ROOT = Path("app/uploads")
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)


class GithubRequest(BaseModel):
    github_url: str


@router.post("/github")
async def import_github_repo(request: GithubRequest):

    repo_id = str(uuid.uuid4())

    repo_folder = UPLOAD_ROOT / repo_id

    try:
        Repo.clone_from(
            request.github_url,
            repo_folder
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Git clone failed: {str(e)}"
        )

    files = scan_repository(str(repo_folder))

    documents = read_repository(str(repo_folder))

    store = build_vector_store(documents)

    save_repository(
        repository_id=repo_id,
        vector_store=store,
        documents=documents
    )

    return {
        "repository_id": repo_id,
        "repository_url": request.github_url,
        "total_files": len(files),
        "documents_loaded": len(documents)
    }
