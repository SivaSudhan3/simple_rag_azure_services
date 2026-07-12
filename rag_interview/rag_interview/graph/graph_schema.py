from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class RetrievedDocument(BaseModel):

    id: str

    content: str

    document_id: Optional[str] = None

    parent_id: Optional[str] = None

    source_file: Optional[str] = None

    page_number: Optional[int] = None

    metadata: Dict[str, Any] = {}


from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class GraphSchema(BaseModel):

    # Request
    request_id: str
    user_id: str
    conversation_id: Optional[str] = None

    # Input
    question: str

    chat_history: List[Dict[str, str]] = Field(default_factory=list)

    # Retrieval
    documents: List[RetrievedDocument] = Field(default_factory=list)

    context: str = ""

    # Generation
    answer: str = ""

    # Security
    is_safe: bool = True
    risk_score: float = 0.0
    attack_detected: bool = False
    blocked_reason: Optional[str] = None

    # Evaluation
    grounded_score: float = 0.0
    relevance_score: float = 0.0

    # Observability
    metrics: Dict[str, Any] = Field(default_factory=dict)

    citation_map: Dict[int, Dict[str, Any]] = Field(default_factory=dict)