def generate_commit_messages(repo):

    documents = repo["documents"]

    suggestions = []

    total_files = len(documents)

    suggestions.append(
        f"feat: analyze repository containing {total_files} files"
    )

    paths = [
        doc.get("path", "").lower()
        for doc in documents
    ]

    if any("readme" in p for p in paths):
        suggestions.append(
            "docs: update project documentation"
        )

    if any("test" in p for p in paths):
        suggestions.append(
            "test: add automated test coverage"
        )

    if any("api" in p for p in paths):
        suggestions.append(
            "feat: improve API endpoints"
        )

    suggestions.append(
        "refactor: improve code maintainability"
    )

    return suggestions