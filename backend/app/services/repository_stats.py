from pathlib import Path


def calculate_repository_stats(root: str):
    root_path = Path(root)

    total_size = 0
    file_count = 0

    for path in root_path.rglob("*"):
        if path.is_file():
            file_count += 1
            total_size += path.stat().st_size

    return {
        "total_files": file_count,
        "total_size_bytes": total_size,
    }