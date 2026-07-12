from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Chat request received from the client.
    """
    conversation_id: str | None = None

    question: str = Field(
        ...,
        min_length=1,
        description="User question"
    )


class ChatResponse(BaseModel):
    """
    Chat response returned to the client.
    """
    conversation_id: str

    answer: str

    grounded_score: float | None = None

    relevance_score: float | None = None

    grounding_reason: str | None = None

    request_id: str | None = None