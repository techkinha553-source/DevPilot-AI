from pathlib import Path

from app.services.parser import (
    IGNORED_DIRECTORIES,
    SUPPORTED_EXTENSIONS,
)


def read_repository(root_path: str):
    """
    Read all supported source files from a repository.
    Returns a list of dictionaries:
    {
        "path": "...",
        "content": "..."
    }
    """
    root = Path(root_path)
    documents = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(part in IGNORED_DIRECTORIES for part in path.parts):
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")

            documents.append(
                {
                    "path": str(path.relative_to(root)),
                    "content": text,
                }
            )
        except Exception:
            # Skip unreadable files
            continue

    return documents
