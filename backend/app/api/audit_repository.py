from fastapi import APIRouter, HTTPException

from app.services.repository_store import repositories

router = APIRouter()

@router.get("/repository/{repository_id}/audit")
def audit_repository(repository_id: str):

    repo = repositories.get(repository_id)
    if not repo:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )
    documents = repo.get("documents", [])
    total_files = len(documents)
    total_lines = 0
    warnings = 0
    risky_files = []
    for doc in documents:
        content = doc.page_content
        lines = len(
            content.splitlines()
        )
        total_lines += lines
        file_warnings = 0
        if "TODO" in content:
            file_warnings += 1
        if "FIXME" in content:
            file_warnings += 1
        if lines > 200:
            file_warnings += 1
        if file_warnings > 0:
            risky_files.append({
                "file": doc.metadata.get(
                    "source",
                    "Unknown"
                ),
                "issues": file_warnings
            })
        warnings += file_warnings
    health_score = max(
        0,
        100 - (warnings * 5)
    )
    return {
        "total_files": total_files,
        "total_lines": total_lines,
        "warnings": warnings,
        "health_score": health_score,
        "risky_files": risky_files[:10],
        "summary":
            f"Repository contains {total_files} files "
            f"with {warnings} warning signals."
    }