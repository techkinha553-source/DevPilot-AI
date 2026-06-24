def generate_pr_summary(repo):

    documents = repo["documents"]

    total_files = len(documents)

    changes = []

    risks = []

    reviewer_notes = []

    paths = [
        doc.get("path", "").lower()
        for doc in documents
    ]

    overview = (
        f"This repository contains "
        f"{total_files} indexed files."
    )

    if any("api" in p for p in paths):
        changes.append(
            "API-related files detected."
        )

    if any("auth" in p for p in paths):
        changes.append(
            "Authentication logic present."
        )

    if any("database" in p for p in paths):
        changes.append(
            "Database integration detected."
        )

    if any("test" in p for p in paths):
        reviewer_notes.append(
            "Test files available."
        )
    else:
        risks.append(
            "No automated tests detected."
        )

    if not any("readme" in p for p in paths):
        risks.append(
            "Missing README documentation."
        )

    reviewer_notes.append(
        "Review security-sensitive files carefully."
    )

    reviewer_notes.append(
        "Verify error handling and edge cases."
    )

    return {
        "overview": overview,
        "changes": changes,
        "risks": risks,
        "reviewer_notes": reviewer_notes
    }