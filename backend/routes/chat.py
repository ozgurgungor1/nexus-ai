from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.api.chat import router as chat_router
from backend.database.database import get_db
from backend.models.chat import ChatRequest
from backend.schemas.chat import ChatResponse
from backend.services.agent_manager import AgentManager
from backend.services.ai_service import AIService
from backend.services.memory_service import MemoryService
from backend.middleware.auth import get_current_user

router = APIRouter()
ai_service = AIService()
memory_service = MemoryService()
agent_manager = AgentManager(ai_service)


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> ChatResponse:
    conversation = memory_service.ensure_conversation(db, current_user["user_id"], request.conversation_id)
    user_message = request.message.strip()
    memory_service.save_message(db, conversation.id, "user", user_message)

    provider_name = ai_service.select_provider(request.model)
    response_text = await agent_manager.handle_message(user_message, provider_name=provider_name)
    memory_service.save_message(db, conversation.id, "assistant", response_text)

    return ChatResponse(response=response_text, conversation_id=conversation.id)
