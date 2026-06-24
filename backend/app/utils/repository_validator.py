from fastapi import HTTPException


def validate_repository(repo):

    if not repo:

        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    return repo