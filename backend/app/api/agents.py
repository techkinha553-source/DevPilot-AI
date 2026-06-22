from fastapi import APIRouter

from app.services.planner import route_task
from app.services.repository_store import get_repository

from app.services.reviewer_agent import review_repository
from app.services.security_agent import security_review
from app.services.architect_agent import architecture_review
from app.services.test_agent import generate_tests
from app.services.agent_memory import save_memory

router = APIRouter()

@router.post("/repository/{repository_id}/agents")
def run_agent(
    repository_id: str,
    request: dict
):

    repo = get_repository(repository_id)

    if not repo:
        return {
            "error": "Repository not found"
        }

    question = request["question"]
    agent = route_task(question)

    if agent == "security":
        result = security_review(repo)
        save_memory(repository_id, question, result)
        return result

    if agent == "reviewer":
        result = review_repository(repo)
        save_memory(repository_id, question, result)
        return result

    if agent == "architect":
        result = architecture_review(repo)
        save_memory(repository_id, question, result)
        return result

    if agent == "tester":
        result = generate_tests(repo)
        save_memory(repository_id, question, result)
        return result

    result = {
        "agent": "assistant",
        "message": "No specialized agent matched."
    }

    save_memory(repository_id, question, result)

    return result



# New endpoint for team review
from app.services.agent_memory import save_memory3

@router.post("/repository/{repository_id}/team-review")
def team_review(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {
            "error": "Repository not found"
        }

    reviewer_result = review_repository(repo)
    security_result = security_review(repo)
    architect_result = architecture_review(repo)
    tester_result = generate_tests(repo)

    result = {
        "repository_id": repository_id,
        "reviewer": reviewer_result,
        "security": security_result,
        "architect": architect_result,
        "tester": tester_result
    }

    save_memory(
        repository_id,
        "team-review",
        result
    )

    return result