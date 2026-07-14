from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.chat_router import router as chat_router
from app.api.v1.documents import router as document_router
# from app.api.v1.auth import router as auth_router
from app.api.v1.conversation_router import router as conversation_router

from app.middleware import register_middleware
from app.exception_handler import register_exception_handlers


def register_routers(app: FastAPI) -> None:
    """
    Register all API routers.

    Keeping router registration centralized makes it easier to
    version APIs and maintain the application as it grows.
    """

    app.include_router(health_router)
    app.include_router(chat_router)

    # Register when implemented
    # app.include_router(auth_router)
    # app.include_router(chat_router)
    app.include_router(document_router)
    app.include_router(conversation_router)


def configure_application(app: FastAPI) -> None:
    """
    Configure the FastAPI application.

    Registers middleware, exception handlers,
    and API routers.
    """

    register_middleware(app)
    register_exception_handlers(app)
    register_routers(app)