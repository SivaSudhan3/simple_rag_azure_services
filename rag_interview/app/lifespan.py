from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI application lifecycle.

    Responsibilities
    ----------------
    - Log application startup and shutdown.
    - Perform lightweight startup validation.
    - Warm application resources (future).
    - Release application resources during shutdown.

    NOTE:
    Heavy resources such as Azure SDK clients, LangGraph,
    LLM services, retrievers, and other singleton services
    are managed through dependency injection in
    core.dependencies and must NOT be created here.
    """

    logger.info("Starting RAG Interview Backend...")

    try:
        # ------------------------------------------------------------------
        # Future startup tasks
        # ------------------------------------------------------------------
        #
        # Validate application configuration
        #
        # await validate_configuration()
        #
        # Warm Azure SDK clients
        #
        # await warmup_services()
        #
        # Check Azure AI Search connectivity
        #
        # await search_service.health_check()
        #
        # Check Blob Storage connectivity
        #
        # await blob_service.health_check()
        #
        # Check Database connection
        #
        # await db.health_check()
        #
        # ------------------------------------------------------------------

        logger.info("Application started successfully.")

        yield

    finally:
        logger.info("Shutting down RAG Interview Backend...")

        # ------------------------------------------------------------------
        # Future cleanup
        # ------------------------------------------------------------------
        #
        # await close_database()
        # await close_http_clients()
        #
        # ------------------------------------------------------------------

        logger.info("Application shutdown completed.")