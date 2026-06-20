from fastapi import APIRouter
from pydantic import BaseModel

from app.services.repository_store import get_repository
from app.services.embedding_service import create_embedding
# from backend.app.services.openai_service import ask_codebase
from app.services.openai_service import ask_codebase

router = APIRouter()


class ChatRequest(BaseModel):
    repository_id: str
    question: str


@router.post("/chat")
async def chat(request: ChatRequest):

    repo = get_repository(
        request.repository_id
    )

    if not repo:
        return {
            "error": "Repository not found"
        }

    query_embedding = create_embedding(
        request.question
    )

    results = repo["vector_store"].search(
        query_embedding,
        k=5
    )

    documents = []

    for result in results:
        documents.append(
            {
                "path": result["path"],
                "content": result["content"]
            }
        )

    answer = ask_codebase(
        request.question,
        documents
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": [
            doc["path"]
            for doc in documents
        ]
    }


# from pathlib import Path

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel

# from app.services.code_reader import read_repository
# from app.services.openai_service import ask_codebase
# from app.services.embedding_service import create_embedding
# from app.services.vector_store import VectorStore

# router = APIRouter()

# class ChatRequest(BaseModel):
#     repository_id: str
#     question: str


# @router.post("/chat")
# async def chat_with_repository(request: ChatRequest):
#     repo_path = Path("app/uploads") / request.repository_id

#     if not repo_path.exists():
#         raise HTTPException(status_code=404, detail="Repository not found.")

#     query_embedding = create_embedding(request.question)

#     store = VectorStore.load(
#         f"app/uploads/{request.repository_id}/.vector_index"
#     )

#     matches = store.search(query_embedding, k=8)

#     documents = read_repository(str(repo_path))

#     answer = ask_codebase(
#         question=request.question,
#         documents=matches,
#     )

#     return {
#         "question": request.question,
#         "answer": answer,
#     }
