from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from rag_interview.core.telemetry.telemetry_models import (
    TelemetryMetrics,
)


class RetrievedDocument(BaseModel):

    id: str

    content: str

    document_id: Optional[str] = None

    parent_id: Optional[str] = None

    source_file: Optional[str] = None

    page_number: Optional[int] = None

    metadata: Dict[str, Any] = {}


class GraphSchema(BaseModel):

    # -----------------------------------------------------
    # Request
    # -----------------------------------------------------

    request_id: str
    user_id: str
    conversation_id: Optional[str] = None

    # -----------------------------------------------------
    # Input
    # -----------------------------------------------------

    question: str

    chat_history: List[Dict[str, str]] = Field(
        default_factory=list
    )

    # -----------------------------------------------------
    # Retrieval
    # -----------------------------------------------------

    documents: List[RetrievedDocument] = Field(
        default_factory=list
    )

    context: str = ""

    citation_map: Dict[int, Dict[str, Any]] = Field(
        default_factory=dict
    )

    # -----------------------------------------------------
    # Generation
    # -----------------------------------------------------

    answer: str = ""

    # -----------------------------------------------------
    # Security
    # -----------------------------------------------------

    is_safe: bool = True
    risk_score: float = 0.0
    attack_detected: bool = False
    blocked_reason: Optional[str] = None

    # -----------------------------------------------------
    # Evaluation
    # -----------------------------------------------------

    grounded_score: float = 0.0
    relevance_score: float = 0.0

    # -----------------------------------------------------
    # Telemetry
    # -----------------------------------------------------

    telemetry: TelemetryMetrics = Field(
        default_factory=TelemetryMetrics
    )