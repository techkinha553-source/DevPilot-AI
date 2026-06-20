from collections import Counter
import os


def generate_repository_summary(documents):
    languages = Counter()

    total_lines = 0

    important_files = []

    for doc in documents:

        path = doc["path"]

        content = doc["content"]

        total_lines += len(
            content.splitlines()
        )

        extension = os.path.splitext(path)[1]

        if extension:
            languages[extension] += 1

        filename = os.path.basename(path)

        if filename.lower() in [
            "readme.md",
            "package.json",
            "requirements.txt",
            "main.py",
            "app.py",
            "index.js"
        ]:
            important_files.append(path)

    return {
        "total_files": len(documents),
        "total_lines": total_lines,
        "languages": dict(languages),
        "important_files": important_files[:10]
    }