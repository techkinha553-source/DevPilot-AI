from collections import Counter


def detect_tech_stack(documents):
    stack = Counter()

    for doc in documents:

        path = doc.get("path", "").lower()

        if path.endswith(".py"):
            stack["Python"] += 1

        elif path.endswith(".js"):
            stack["JavaScript"] += 1

        elif path.endswith(".ts"):
            stack["TypeScript"] += 1

        elif path.endswith(".tsx"):
            stack["React"] += 1

        elif path.endswith(".jsx"):
            stack["React"] += 1

        elif path.endswith(".java"):
            stack["Java"] += 1

        elif path.endswith(".cpp"):
            stack["C++"] += 1

        elif path.endswith(".html"):
            stack["HTML"] += 1

        elif path.endswith(".css"):
            stack["CSS"] += 1

    return dict(stack)