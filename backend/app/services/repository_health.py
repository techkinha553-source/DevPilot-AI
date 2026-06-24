from app.services.engineering_score import (
    calculate_engineering_score
)


def generate_repository_health(repo):

    documents = repo["documents"]

    quality_score = 100
    bugs = 0
    code_smells = 0
    security_issues = 0

    paths = [
        doc.get("path", "").lower()
        for doc in documents
    ]

    has_readme = any(
        "readme" in p
        for p in paths
    )

    has_tests = any(
        "test" in p
        for p in paths
    )

    for doc in documents:

        content = doc.get(
            "content",
            ""
        )

        if len(content.splitlines()) > 500:
            code_smells += 1

        if "TODO" in content:
            code_smells += 1

        if "FIXME" in content:
            code_smells += 1

        if "except:" in content:
            bugs += 1

        if "password=" in content.lower():
            security_issues += 1

        if "api_key" in content.lower():
            security_issues += 1

    quality_score -= (
        bugs * 5
    )

    quality_score -= (
        code_smells * 2
    )

    quality_score -= (
        security_issues * 10
    )

    quality_score = max(
        0,
        min(100, quality_score)
    )

    engineering_score = (
        calculate_engineering_score(
            repo
        )
    )

    health_status = "Excellent"

    if quality_score < 90:
        health_status = "Good"

    if quality_score < 75:
        health_status = "Average"

    if quality_score < 60:
        health_status = "Poor"

    return {
        "health_status": health_status,
        "quality_score": quality_score,
        "engineering_score":
            engineering_score,
        "bugs": bugs,
        "code_smells": code_smells,
        "security_issues":
            security_issues,
        "has_readme": has_readme,
        "has_tests": has_tests
    }