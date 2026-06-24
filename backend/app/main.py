from fastapi import FastAPI

from fastapi.responses import JSONResponse
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.repository import router as repository_router
from app.api.github import router as github_router
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
from app.api.generate import (
    router as generate_router
)
from app.api.assistant import (
    router as assistant_router
)
from app.api.agents import router as agents_router
from app.api.agent_memory import (
    router as agent_memory_router
)
from app.core.logger import logger

import time

app = FastAPI(title="DevPilot AI")

logger.info(
    "DevPilot AI backend started"
)

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
app.include_router(generate_router)
app.include_router(
    assistant_router
)
app.include_router(agents_router)
app.include_router(
    agent_memory_router
)

@app.get("/")
def root():
    return {
        "message": "DevPilot AI backend is running"
    }

@app.exception_handler(Exception)
async def global_exception_handler(
    request,
    exc
):

    logger.error(
        f"Unhandled exception: {str(exc)}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc)
        }
    )

@app.get("/health")
def health():

    logger.info(
        "Health endpoint called"
    )

    return {
        "status": "healthy"
    }

@app.middleware("http")

async def process_time(

    request,

    call_next

):

    start = time.time()

    response = await call_next(

        request

    )

    process_time = (

        time.time() - start

    )

    response.headers["X-Process-Time"] = f"{process_time:.4f}"

    return response