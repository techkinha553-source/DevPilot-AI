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


def security_audit(repo):
    documents = repo["documents"]

    findings = []

    for doc in documents:
        content = doc.get("content", "")
        path = doc.get("path", "")

        if "password" in content.lower():
            findings.append(f"Possible hardcoded password in {path}")

        if "secret" in content.lower():
            findings.append(f"Possible secret detected in {path}")

        if "api_key" in content.lower():
            findings.append(f"Possible API key usage in {path}")

    return {
        "agent": "security-auditor",
        "issues_found": len(findings),
        "findings": findings
    }


def performance_review(repo):
    documents = repo["documents"]

    findings = []

    for doc in documents:
        content = doc.get("content", "")
        path = doc.get("path", "")

        if "for " in content and "for " in content[content.find("for ") + 1:]:
            findings.append(f"Possible nested loops in {path}")

        if ".read()" in content:
            findings.append(f"Large file read detected in {path}")

    return {
        "agent": "performance-engineer",
        "issues_found": len(findings),
        "findings": findings
    }


def test_review(repo):
    documents = repo["documents"]

    test_files = 0

    for doc in documents:
        path = doc.get("path", "").lower()

        if "test" in path:
            test_files += 1

    return {
        "agent": "test-engineer",
        "test_files": test_files,
        "coverage_estimate": f"{test_files} test-related files detected"
    }
