import json
from pathlib import Path
from datetime import datetime


def save_metadata(
    repository_id: str,
    name: str,
    total_files: int,
    upload_path: Path,
):
    metadata = {
        "repository_id": repository_id,
        "repository_name": name,
        "uploaded_at": datetime.utcnow().isoformat(),
        "total_files": total_files,
    }

    metadata_file = upload_path / "metadata.json"

    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)


def load_metadata(upload_path: Path):
    metadata_file = upload_path / "metadata.json"

    if not metadata_file.exists():
        return None

    with open(metadata_file, "r", encoding="utf-8") as f:
        return json.load(f)