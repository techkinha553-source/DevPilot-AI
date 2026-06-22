from fastapi import APIRouter

from app.services.agent_memory import (
    get_memory
)

router = APIRouter()


@router.get(
    "/repository/{repository_id}/memory"
)
def repository_memory(
    repository_id: str
):
    return {
        "repository_id": repository_id,
        "memory":
        get_memory(repository_id)
    }