from fastapi import APIRouter, Depends

from app.security.current_user import get_current_user
from app.security.models import CurrentUser

from rag_interview.core.dependencies import get_conversation_service
from rag_interview.services.conversation_services import ConversationService

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)

@router.get("")
async def list_conversations(
    current_user: CurrentUser = Depends(get_current_user),
    
    conversation_service: ConversationService = Depends(
        get_conversation_service
    ),
):
    return await conversation_service.list_conversations()
@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    
    conversation_service: ConversationService = Depends(
        get_conversation_service
    ),
):
    conversation = await conversation_service.get_conversation(
        conversation_id
    )

    if conversation is None:
        return {
            "message": "Conversation not found"
        }

    return conversation
@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    
    conversation_service: ConversationService = Depends(
        get_conversation_service
    ),
):
    await conversation_service.delete(conversation_id)

    return {
        "message": "Conversation deleted"
    }
@router.delete("")
async def delete_conversation_all(
    
    
    conversation_service: ConversationService = Depends(
        get_conversation_service
    ),
):
    await conversation_service.delete_all()

    return {
        "message": "Conversation deleted"
    }