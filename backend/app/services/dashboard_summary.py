from app.services.language_stats import (
    detect_languages
)


def generate_dashboard_summary(repo):

    documents = repo["documents"]

    total_files = len(documents)

    total_lines = sum(
        len(
            doc.get(
                "content",
                ""
            ).splitlines()
        )
        for doc in documents
    )

    languages = detect_languages(
        documents
    )

    total_bugs = 0
    total_smells = 0

    for doc in documents:

        content = doc.get(
            "content",
            ""
        )

        if "except:" in content:
            total_bugs += 1

        if "password=" in content.lower():
            total_bugs += 1

        if len(
            content.splitlines()
        ) > 500:
            total_smells += 1

        if (
            "TODO" in content
            or
            "FIXME" in content
        ):
            total_smells += 1

    quality_score = max(
        0,
        100
        - total_bugs * 5
        - total_smells * 2
    )

    return {
        "total_files": total_files,
        "total_lines": total_lines,
        "languages": languages,
        "quality_score": quality_score,
        "total_bugs": total_bugs,
        "total_code_smells": total_smells
    }