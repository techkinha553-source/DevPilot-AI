from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from pathlib import Path
from git import Repo

from app.services.code_reader import read_repository
from app.services.parser import scan_repository
from app.services.rag_builder import build_vector_store
from app.services.repository_store import save_repository
from app.services.summary_service import (
    generate_repository_summary
)
from app.core.logger import logger

router = APIRouter(tags=["GitHub"])

UPLOAD_ROOT = Path("app/uploads")
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)


class GithubRequest(BaseModel):
    github_url: str



@router.post("/github")
async def import_github_repo(request: GithubRequest):

    repo_id = str(uuid.uuid4())
    logger.info(
        f"Starting GitHub import for repository {repo_id}: {request.github_url}"
    )

    repo_folder = UPLOAD_ROOT / repo_id

    try:
        Repo.clone_from(
            request.github_url,
            repo_folder
        )

        logger.info(
            f"Repository {repo_id} cloned successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Git clone failed: {str(e)}"
        )

    files = scan_repository(str(repo_folder))

    documents = read_repository(str(repo_folder))

    logger.info(
        f"Repository {repo_id} scanned: {len(files)} files, {len(documents)} documents"
    )

    store = build_vector_store(documents)

    summary = generate_repository_summary(
        documents
    )

    save_repository(
        repository_id=repo_id,
        vector_store=store,
        documents=documents,
        summary=summary
    )

    logger.info(
        f"Repository {repo_id} indexed and stored successfully"
    )

    logger.info(
        f"GitHub import completed for repository {repo_id}"
    )

    return {
        "repository_id": repo_id,
        "repository_url": request.github_url,
        "total_files": len(files),
        "documents_loaded": len(documents)
    }
