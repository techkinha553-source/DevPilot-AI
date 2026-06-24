from app.services.openai_service import ask_llm


def review_pull_request(
    repo,
    changed_files
):

    selected_files = []

    for doc in repo["documents"]:

        if doc["path"] in changed_files:

            selected_files.append(
                f"""
File: {doc['path']}

{doc['content'][:2000]}
"""
            )

    context = "\n\n".join(
        selected_files
    )

    prompt = f"""
You are a senior software engineer.

Review the following modified files.

Provide:

1. Potential bugs
2. Security concerns
3. Code smells
4. Refactoring suggestions
5. Overall PR approval recommendation

Files:

{context}
"""

    review = ask_llm(prompt)

    return {
        "agent": "pr-reviewer",
        "files_reviewed": changed_files,
        "review": review
    }