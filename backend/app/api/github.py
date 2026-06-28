from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from pathlib import Path
from git import Repo
import requests
import time

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

# Simple in-memory cache for branch lists with TTL
CACHE_TTL_SECONDS = 300
branch_cache: dict[tuple[str, str], tuple[float, list[str]]] = {}


class GithubRequest(BaseModel):
    repository: str
    username: str | None = None
    branch: str = "main"



@router.post("/github/import")
async def import_github_repo(request: GithubRequest):

    repo_id = str(uuid.uuid4())

    github_username = request.username or "github_user"

    github_url = (
        f"https://github.com/"
        f"{github_username}/"
        f"{request.repository}.git"
    )

    logger.info(
        f"Starting GitHub import for repository {repo_id}: {github_url}"
    )

    repo_folder = UPLOAD_ROOT / repo_id

    try:
        Repo.clone_from(
            github_url,
            repo_folder,
            branch=request.branch,
            single_branch=True,
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
        owner=github_username,
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

    logger.info(
        f"Imported branch '{request.branch}' for repository {request.repository}"
    )

    return {
        "repository_id": repo_id,
        "repository_name": request.repository,
        "repository_url": github_url,
        "branch": request.branch,
        "total_files": len(files),
        "documents_loaded": len(documents)
    }

@router.get("/github/branches")
def get_branches(username: str, repository: str, refresh: bool = False):

    github_url = (
        f"https://api.github.com/repos/"
        f"{username}/{repository}/branches"
    )

    logger.info(
        f"Fetching branches for {username}/{repository}"
    )

    cache_key = (username, repository)

    if not refresh and cache_key in branch_cache:
        cached_at, cached_branches = branch_cache[cache_key]
        if time.time() - cached_at < CACHE_TTL_SECONDS:
            logger.info(
                f"Using cached branches for {username}/{repository}"
            )
            return {"branches": cached_branches}
        logger.info(
            f"Branch cache expired for {username}/{repository}; refreshing"
        )

    if refresh:
        logger.info(
            f"Force refreshing branches for {username}/{repository}"
        )

    response = requests.get(
        github_url,
        headers={"Accept": "application/vnd.github+json"},
        timeout=15,
    )

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="Repository not found."
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Unable to fetch branches from GitHub."
        )

    branches = [
        branch["name"]
        for branch in response.json()
    ]

    branch_cache[cache_key] = (time.time(), branches)
    logger.info(
        f"Branch cache updated for {username}/{repository}"
    )
    logger.info(
        f"Fetched {len(branches)} branches for {username}/{repository}"
    )

    return {
        "branches": branches
    }