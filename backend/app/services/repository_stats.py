def detect_stack(documents):

    stack = {
        "frontend": [],
        "backend": [],
        "database": []
    }

    for doc in documents:

        path = doc["path"].lower()

        if "next.config" in path:
            stack["frontend"].append(
                "Next.js"
            )

        if path.endswith(".tsx"):
            stack["frontend"].append(
                "React"
            )

        if "fastapi" in doc["content"].lower():
            stack["backend"].append(
                "FastAPI"
            )

        if "mongodb" in doc["content"].lower():
            stack["database"].append(
                "MongoDB"
            )

    for key in stack:
        stack[key] = list(
            set(stack[key])
        )

    return stack


def calculate_repository_stats(documents):

    total_files = len(documents)

    total_lines = 0

    for doc in documents:

        total_lines += len(
            doc["content"].splitlines()
        )

    stack = detect_stack(
        documents
    )

    return {
        "total_files": total_files,
        "total_lines": total_lines,
        "stack": stack
    }