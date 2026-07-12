from fastapi import APIRouter, status

from app.schemas.common import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Liveness Probe",
)
async def health() -> HealthResponse:
    """
    Liveness endpoint.

    Used by orchestrators to verify that the application
    process is running.
    """

    return HealthResponse(status="healthy")


@router.get(
    "/ready",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness Probe",
)
async def readiness() -> HealthResponse:
    """
    Readiness endpoint.

    Currently verifies that the application has started
    successfully.

    Future:
    - Azure OpenAI
    - Azure AI Search
    - Blob Storage
    - PostgreSQL
    - Redis
    """

    return HealthResponse(status="ready")