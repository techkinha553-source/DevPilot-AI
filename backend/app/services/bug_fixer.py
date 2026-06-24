from app.services.openai_service import ask_llm


def fix_repository_bug(
    repo,
    file_path: str,
    issue: str
):

    target_file = None

    for doc in repo["documents"]:

        if doc["path"] == file_path:
            target_file = doc
            break

    if not target_file:
        return {
            "error": "File not found"
        }

    code = target_file["content"]

    prompt = f"""
You are a senior software engineer.

Bug Description:
{issue}

File:
{file_path}

Code:
{code}

Provide:

1. Root cause
2. Fixed code
3. Explanation
4. Additional improvements
"""

    response = ask_llm(prompt)

    return {
        "agent": "bug-fixer",
        "file": file_path,
        "issue": issue,
        "fix": response
    }


def generate_fixes(repo):
    """
    Compatibility function used by repository.py.
    Scans repository files and returns simple fix suggestions.
    """

    fixes = []

    documents = repo.get("documents", [])

    for doc in documents:

        path = doc.get("path", "")
        content = doc.get("content", "")

        if "TODO" in content:
            fixes.append({
                "file": path,
                "issue": "TODO found",
                "suggestion": "Complete pending implementation"
            })

        if "password" in content.lower():
            fixes.append({
                "file": path,
                "issue": "Possible hardcoded password",
                "suggestion": "Move secrets to environment variables"
            })

    return {
        "agent": "bug-fixer",
        "total_suggestions": len(fixes),
        "fixes": fixes
    }
