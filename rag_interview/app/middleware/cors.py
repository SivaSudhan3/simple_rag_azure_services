from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware




def register_cors(app: FastAPI) -> None:
    """
    Register Cross-Origin Resource Sharing (CORS) middleware.

    Allows trusted frontend applications to communicate
    with the backend.
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=[
            "X-Request-ID",
            "X-Process-Time",
        ],
    )