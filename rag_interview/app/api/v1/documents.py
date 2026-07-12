from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)

from app.schemas.document import UploadResponse

from app.security.current_user import get_current_user
from app.security.models import CurrentUser

from rag_interview.core.dependencies import (
    get_document_service,
    get_ingestion_service,
)

from app.services.document_service import DocumentService
from rag_interview.services.ingestion_service import IngestionService

from rag_interview.services.delete_index import delete_documents


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=202,
)
async def upload_document(
    file: UploadFile = File(...),
    current_user: CurrentUser = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service),
    ingestion_service: IngestionService = Depends(get_ingestion_service),
):
    response = await service.upload(file)

    await ingestion_service.ingest(
        response.job_id,
        response.blob_name,
        response.filename,
    )

    return response


@router.delete("/delete")
async def delete_all_documents(
    
):
    deleted_count = await delete_documents()

    return {
        "message": "Documents deleted successfully",
        "deleted_documents": deleted_count,}
