import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    Adds a correlation ID to every request.

    If the client already provides an X-Request-ID header,
    it is reused. Otherwise, a new UUID is generated.

    The request ID is stored in request.state and returned
    in the response header.
    """

    HEADER_NAME = "X-Request-ID"

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:

        request_id = request.headers.get(
            self.HEADER_NAME,
            str(uuid.uuid4())
        )

        request.state.request_id = request_id

        response = await call_next(request)

        response.headers[self.HEADER_NAME] = request_id

        print(">>> RequestIdMiddleware")

        return response