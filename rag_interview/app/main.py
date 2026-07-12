import app.logging
from fastapi import FastAPI

from app.lifespan import lifespan

from app.setup import configure_application


def create_application() -> FastAPI:
    app = FastAPI(
        title="RAG Interview API",
        version="1.0.0",
        lifespan=lifespan,
    )

    configure_application(app)

    return app


app = create_application()