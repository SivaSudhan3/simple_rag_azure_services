from enum import Enum

from pydantic import BaseModel


class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class UploadResponse(BaseModel):
    job_id: str
    blob_name: str
    filename: str
    status: JobStatus