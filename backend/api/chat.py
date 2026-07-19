from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.schemas.chat import ChatRequest, ChatResponse
from backend.services.ai_service import AIService
from backend.services.conversation_service import ConversationService
from backend.services.memory_service import MemoryService
from backend.services.research_service import ResearchService
from backend.services.settings_service import SettingsService
from backend.middleware.auth import get_current_user

router = APIRouter()
ai_service = AIService()
memory_service = MemoryService()
research_service = ResearchService()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> ChatResponse:
    settings_service = SettingsService(db)
    user_settings = settings_service.get_settings(current_user["user_id"]) or settings_service.update_settings(current_user["user_id"])
    provider_name = ai_service.select_provider(request.model or user_settings.preferred_model)

    conversation_service = ConversationService(db, ai_service, memory_service, research_service)
    try:
        response_text, conversation_id = await conversation_service.process_message(
            current_user["user_id"],
            request.message.strip(),
            conversation_id=request.conversation_id,
            provider_name=provider_name,
            use_research=user_settings.external_research_enabled,
            model=request.model,
            preferred_agent=user_settings.preferred_agent,
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    return ChatResponse(response=response_text, conversation_id=conversation_id)
