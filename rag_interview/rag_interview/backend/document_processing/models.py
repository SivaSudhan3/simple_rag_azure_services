from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from uuid import uuid4

from pydantic import BaseModel, Field

from uuid import uuid4
from datetime import datetime


class DocumentContext(BaseModel):

    document_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    source_file: str

    file_type: str

    # NEW
    page_offset: int = 0

    created_at: str = Field(
        default_factory=lambda:
            datetime.utcnow().isoformat()
    )

    metadata: dict = {}
class AnalyzedDocument(BaseModel):

    context: DocumentContext

    result: object


class BoundingBox(BaseModel):

    page_number: int

    polygon: Optional[List[float]] = None



class DocumentBlock(BaseModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    document_id: str


    content: str


    content_type: str
    # text/table/image


    page_number: int


    order: int


    bounding_box: Optional[BoundingBox] = None


    metadata: Dict = {}
class Chunk(BaseModel):


    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    document_id: str


    content: str


    chunk_type: str
    # parent / child / semantic / table


    embedding_content: str


    parent_id: Optional[str] = None


    metadata: Dict = {}