from fastapi import FastAPI

from .health import router as health_router
from .chat_router import router as chat_router
from .documents import router as document_router


def register_routers(app: FastAPI) -> None:
    app.include_router(
        health_router,
        prefix="/api/v1",
    )
    app.include_router(
    chat_router,
    prefix="/api/v1",
   )
    app.include_router(
        document_router,
        prefix="api/v1"

    )

