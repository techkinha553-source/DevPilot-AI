def architecture_review(repo):
    documents = repo["documents"]

    tech_stack = []

    for doc in documents:

        path = doc.get("path", "").lower()

        if "fastapi" in doc.get("content", "").lower():
            tech_stack.append("FastAPI")

        if "react" in doc.get("content", "").lower():
            tech_stack.append("React")

        if "next" in path:
            tech_stack.append("Next.js")

    tech_stack = list(set(tech_stack))

    return {
        "agent": "architect",
        "architecture": tech_stack,
        "recommendation":
            "Split large modules into domain services."
    }