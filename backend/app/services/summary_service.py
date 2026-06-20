from collections import Counter


def generate_repository_summary(documents):
    total_files = len(documents)

    extensions = []

    for doc in documents:
        path = doc["path"]

        if "." in path:
            extensions.append(
                path.split(".")[-1]
            )

    languages = Counter(
        extensions
    ).most_common(5)

    return {
        "project_name": "Imported Repository",
        "description":
            f"Repository contains {total_files} files.",
        "total_files": total_files,
        "top_languages":
            [lang for lang, _ in languages]
    }