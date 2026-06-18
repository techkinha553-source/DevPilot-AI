import shutil
import uuid
import zipfile
from pathlib import Path

from app.services.code_reader import read_repository
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.services.rag_builder import build_vector_store
from app.services.repository_metadata import save_metadata
from app.services.repository_store import save_repository

from app.services.parser import scan_repository

router = APIRouter()

UPLOAD_ROOT = Path("app/uploads")
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_repository(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Please upload a ZIP file.")

    repo_id = str(uuid.uuid4())

    zip_path = UPLOAD_ROOT / f"{repo_id}.zip"
    extract_path = UPLOAD_ROOT / repo_id

    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    files = scan_repository(str(extract_path))

    documents = read_repository(str(extract_path))

    store = build_vector_store(documents)

    save_repository(
        repository_id=repo_id,
        vector_store=store,
        documents=documents
    )

    vector_folder = extract_path / ".vector_index"
    # store.save(str(vector_folder))
    

    save_metadata(

        repository_id=repo_id,

        name=file.filename,

        total_files=len(files),

        upload_path=extract_path,

    )

    return {
        "repository_id": repo_id,
        "total_files": len(files),
        "files": files,
        "documents_loaded": len(documents),
        "preview": documents[:2],
    }
