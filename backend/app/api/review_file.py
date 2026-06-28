from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.repository_store import repositories

router = APIRouter()

class ReviewRequest(BaseModel):
    file_name: str

@router.post("/repository/{repository_id}/review-file")
def review_file(
    repository_id: str,
    request: ReviewRequest
):
    repo = repositories.get(repository_id)

    if not repo:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    for doc in repo.get("documents", []):

        source = doc.metadata.get(
            "source",
            ""
        )

        if source == request.file_name:

            content = doc.page_content

            warnings = []

            if "TODO" in content:
                warnings.append(
                    "- TODO comments found"
                )

            if "FIXME" in content:
                warnings.append(
                    "- FIXME comments found"
                )

            if len(content.splitlines()) > 200:
                warnings.append(
                    "- Large file (>200 lines)"
                )

            if content.count("try:") == 0:
                warnings.append(
                    "- No exception handling detected"
                )

            review = f"""
AI Code Review

File:
{request.file_name}

Statistics:
- Lines: {len(content.splitlines())}
- Characters: {len(content)}

Potential Issues:
{chr(10).join(warnings) if warnings else '- No major issues detected'}

Suggestions:
- Improve documentation
- Add unit tests
- Reduce function complexity
- Improve code reuse
"""

            return {
                "review": review
            }

    raise HTTPException(
        status_code=404,
        detail="File not found"
    )