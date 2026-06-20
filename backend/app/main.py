from fastapi import FastAPI

from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.repository import router as repository_router
from app.api.github import router as github_router
from app.api.repository import router as repository_router
from app.api.summary import (
    router as summary_router
)
from app.api.search import (
    router as search_router
)
from app.api.insights import (
    router as insights_router
)
from app.api.architecture import (
    router as architecture_router
)

app = FastAPI(title="DevPilot AI")

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(repository_router)
app.include_router(github_router)
app.include_router(summary_router)
app.include_router(
    search_router
)
app.include_router(
    insights_router
)
app.include_router(
    architecture_router
)

@app.get("/")
def root():
    return {
        "message": "DevPilot AI backend is running"
    }
