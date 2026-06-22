def security_review(repo):
    documents = repo["documents"]

    issues = []

    patterns = [
        "sk-",
        "ghp_",
        "AKIA",
        "password=",
        "secret=",
        "api_key"
    ]

    for doc in documents:

        content = doc.get("content", "")
        path = doc.get("path", "")

        for pattern in patterns:

            if pattern.lower() in content.lower():

                issues.append({
                    "file": path,
                    "pattern": pattern
                })

    return {
        "agent": "security",
        "risk":
            "high" if issues else "low",
        "issues": issues
    }
