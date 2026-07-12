from fastapi import FastAPI

from app.middleware.cors import register_cors
from app.middleware.logging import LoggingMiddleware
from app.middleware.request_id import RequestIdMiddleware
from app.middleware.timing import TimingMiddleware


def register_middleware(app: FastAPI) -> None:
    """
    Register all application middleware.

    Note:
        Middleware executes in reverse order of registration.
    """

    register_cors(app)

    app.add_middleware(LoggingMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(RequestIdMiddleware)