from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.repository_store import repositories

router = APIRouter()

class ExplainRequest(BaseModel):
    file_name: str

@router.post("/repository/{repository_id}/explain-file")
def explain_file(
    repository_id: str,
    request: ExplainRequest
):
    repo = repositories.get(repository_id)

    if not repo:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    documents = repo.get("documents", [])

    for doc in documents:

        source = doc.metadata.get(
            "source",
            ""
        )

        if source == request.file_name:

            content = doc.page_content[:4000]

            explanation = f"""
File: {request.file_name}

Purpose:
This file is part of the repository and contains application logic.

Statistics:
- Characters: {len(content)}
- Lines: {len(content.splitlines())}

Quick Review:
- Check naming consistency
- Add comments where necessary
- Review exception handling
- Verify code reuse opportunities

Preview:
{content[:500]}
"""

            return {
                "explanation": explanation
            }

    raise HTTPException(
        status_code=404,
        detail="File not found"
    )