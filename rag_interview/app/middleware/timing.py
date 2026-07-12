import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Measures request processing time.

    Stores the elapsed duration in request.state.process_time
    and returns it to the client using the X-Process-Time
    response header.
    """

    HEADER_NAME = "X-Process-Time"

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:

        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        request.state.process_time = process_time* 1000

        response.headers[self.HEADER_NAME] = f"{process_time:.6f}s"

        return response