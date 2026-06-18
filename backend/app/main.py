from fastapi import FastAPI

from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.repository import router as repository_router
from app.api.github import router as github_router
from app.api.repository import router as repository_router

app = FastAPI(title="DevPilot AI")

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(repository_router)
app.include_router(github_router)
app.include_router(repository_router)

@app.get("/")
def root():
    return {
        "message": "DevPilot AI backend is running"
    }
