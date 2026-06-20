from git import Repo
from pathlib import Path
import uuid


def clone_repository(
    github_url: str
):
    repo_id = str(uuid.uuid4())

    target_dir = (
        Path("uploads")
        / repo_id
    )

    Repo.clone_from(
        github_url,
        target_dir
    )

    return repo_id, target_dir