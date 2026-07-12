from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.schemas.document import (
    UploadResponse,
    JobStatus,
)

from rag_interview.services.azure_blob import BlobStorageService





class DocumentService:

    def __init__(
        self,
        blob_storage: BlobStorageService,
    ):
        self.blob_storage = blob_storage

    async def upload(
        self,
        file: UploadFile,
    ) -> UploadResponse:

        if file.filename is None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename missing.",
            )

        allowed_extensions = {
            ".pdf",
            ".docx",
            ".txt",
        }

        extension = (
            Path(file.filename)
            .suffix
            .lower()
        )

        if extension not in allowed_extensions:

            raise HTTPException(
                status_code=400,
                detail="Unsupported document type.",
            )

        job_id = str(uuid4())

        blob_name = (
            f"{job_id}{extension}"
        )

        data = await file.read()

        self.blob_storage.upload(
            blob_name=blob_name,
            data=data,
            content_type=file.content_type,
        )

        return UploadResponse(
        job_id=job_id,
        blob_name=blob_name,
        filename=file.filename,
        status=JobStatus.QUEUED,
        )

        
