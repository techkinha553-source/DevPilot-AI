from app.services.openai_service import ask_llm

def refactor_repository_file(repo,file_path: str):

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
You are a senior software architect.

Refactor the following code.

Improve:
1. Readability
2. Maintainability
3. Separation of concerns
4. Performance
5. Best practices

Code:

{code}

Provide:
1. Problems found
2. Refactored code
3. Explanation
"""

    result = ask_llm(prompt)
    return {
        "agent": "refactor-agent",
        "file": file_path,
        "refactor": result,
    }