from fastapi import APIRouter
from app.core.logger import logger

from app.services.planner import route_task
from app.services.repository_store import get_repository

from app.services.reviewer_agent import review_repository
from app.services.security_agent import security_review
from app.services.architect_agent import architecture_review
from app.services.test_agent import generate_tests
from app.services.agent_memory import save_memory
from app.services.architect_agent import (
    architecture_review
)
from app.models.architect_request import (
    ArchitectRequest
)
from app.services.reviewer_agent import (
    review_repository
)
from app.services.reviewer_agent import (
    security_audit,
    performance_review,
    test_review
)
from app.models.pr_review import (
    PRReviewRequest
)

from app.services.pr_reviewer import (
    review_pull_request
)

from app.models.bug_fix_request import (
    BugFixRequest
)

from app.services.bug_fixer import (
    fix_repository_bug
)
from app.models.refactor_request import (
    RefactorRequest
)

from app.services.refactor_agent import (
    refactor_repository_file
)

from app.services.repository_qa import (
    answer_repository_question
)

from app.services.agent_memory import (
    get_memory
)
from app.services.architecture_diagram import (
    generate_architecture_diagram
)

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


@router.post("/repository/{repository_id}/team-review")
def team_review(repository_id: str):

    repo = get_repository(repository_id)

    logger.info(
        f"Team review started for repository {repository_id}"
    )   

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

    logger.info(
        f"Team review completed for repository {repository_id}"
    )

    return result

@router.post("/repository/{repository_id}/architect")
def architect_agent(repository_id: str,request: ArchitectRequest):
    repo = get_repository(
    repository_id
    )

    if not repo:
        return {
            "error":
            "Repository not found"
        }

    return architecture_review(repo)

@router.post(
    "/repository/{repository_id}/reviewer"
)
def reviewer_agent(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {
            "error": "Repository not found"
        }

    return review_repository(repo)

@router.post(
    "/repository/{repository_id}/security-auditor"
)
def security_auditor(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    return security_audit(repo)

@router.post(
    "/repository/{repository_id}/performance-engineer"
)
def performance_engineer(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    return performance_review(repo)

@router.post(
    "/repository/{repository_id}/test-engineer"
)
def test_engineer(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    return test_review(repo)

@router.post(
    "/repository/{repository_id}/pr-review"
)
def pr_review(
    repository_id: str,
    request: PRReviewRequest
):

    logger.info(
        f"PR review started for repository {repository_id}"
    )

    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error":
            "Repository not found"
        }

    logger.info(
        f"PR review completed for repository {repository_id}"
    )

    return review_pull_request(
        repo,
        request.changed_files
    )


@router.post(
    "/repository/{repository_id}/fix-bug"
)
def fix_bug(
    repository_id: str,
    request: BugFixRequest
):

    logger.info(
        f"Bug fix agent started for repository {repository_id}"
    )

    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error": "Repository not found"
        }

    logger.info(
        f"Bug fix generated for file {request.file_path}"
    )

    return fix_repository_bug(
        repo,
        request.file_path,
        request.issue
    )

@router.post(
    "/repository/{repository_id}/refactor-agent"
)
def refactor_agent(repository_id: str,request: RefactorRequest):

    logger.info(
        f"Refactor agent started for repository {repository_id}"
    )

    repo = get_repository(
    repository_id
    )

    if not repo:
        return {
            "error": "Repository not found"
        }

    logger.info(
        f"Refactor suggestions generated for {request.file_path}"
    )

    return refactor_repository_file(
        repo,
        request.file_path
    )


# Repository chat endpoint
@router.post(
    "/repository/{repository_id}/chat"
)
def repository_chat(
    repository_id: str,
    request: dict
):

    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error": "Repository not found"
        }

    question = request.get(
        "question",
        ""
    )

    logger.info(
        f"Repository chat question received for {repository_id}"
    )

    previous_memory = get_memory(
        repository_id
    )

    answer = answer_repository_question(
        repo,
        question
    )

    save_memory(
        repository_id,
        question,
        answer
    )

    logger.info(
        f"Repository chat completed for {repository_id}"
    )

    return {
        "question": question,
        "memory_items": len(previous_memory),
        "answer": answer
    }

@router.post(
    "/repository/{repository_id}/architecture-diagram"
)
def architecture_diagram(
    repository_id: str
):

    logger.info(
        f"Architecture diagram generation started for {repository_id}"
    )

    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error": "Repository not found"
        }

    logger.info(
        f"Architecture diagram generated for {repository_id}"
    )

    return generate_architecture_diagram(
        repo
    )