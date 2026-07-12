import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs request and response metadata.

    This middleware relies on:
        - RequestIdMiddleware
        - TimingMiddleware
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:

        request_id = getattr(request.state, "request_id", "-")

        logger.info(
            "Incoming request",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
            },
        )

        try:
            response = await call_next(request)

        except Exception:

            logger.exception(
                "Unhandled exception",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                },
            )

            raise

        duration_ms = getattr(
            request.state,
            "process_time",
            0.0,
        ) * 1000

        logger.info(
            "Request completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
            },
        )

        return response