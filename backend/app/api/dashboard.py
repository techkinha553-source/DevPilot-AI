from fastapi import APIRouter
from app.services.repository_store import get_repository
from app.services.repo_intelligence import (
    generate_ai_summary,
    classify_issues,
    calculate_health_score
)
from app.services.user_store import user_stats

router = APIRouter()


@router.get("/repository/{repository_id}/dashboard")
def get_dashboard(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    documents = repo["documents"]

    issues = classify_issues(documents)

    return {
        "repository_id": repository_id,
        "total_files": len(documents),
        "engineering_score": 80,
        "health_score": calculate_health_score(issues),
        "languages": ["Python", "JavaScript"],
        "issues": issues,
        "ai_summary": generate_ai_summary(documents)
    }

@router.get("/dashboard/{email}")

def dashboard(email: str):

    return user_stats.get(

        email,

        {}

    )