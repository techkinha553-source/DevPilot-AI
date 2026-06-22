def review_repository(repo):
    documents = repo["documents"]

    smells = 0
    bugs = 0

    for doc in documents:

        content = doc.get("content", "")

        if len(content.splitlines()) > 500:
            smells += 1

        if "TODO" in content or "FIXME" in content:
            smells += 1

        if "except:" in content:
            bugs += 1

    return {
        "agent": "reviewer",
        "code_smells": smells,
        "bugs": bugs,
        "summary":
            f"Found {smells} code smells and {bugs} potential bugs."
    }
