from fastapi import APIRouter, Depends

from app.schemas.schema import (
    ChatRequest,
    ChatResponse,
)
from app.services.chat_service import ChatService
from rag_interview.core.dependencies import get_chat_service
from app.security.current_user import get_current_user
from app.security.models import CurrentUser
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    current_user: CurrentUser = Depends(get_current_user),
    
    chat_service: ChatService = Depends(get_chat_service),
):
    return await chat_service.chat(
        request=request,
        
    )
@router.post("/chat/stream")
async def stream_chat(
    request: ChatRequest,
    current_user: CurrentUser = Depends(get_current_user),
    
    chat_service: ChatService = Depends(get_chat_service),
):

    return StreamingResponse(
        chat_service.stream_chat(
            request=request,
            current_user=current_user
        ),
        media_type="text/event-stream",
    )