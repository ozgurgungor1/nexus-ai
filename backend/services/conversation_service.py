from sqlalchemy.orm import Session

from backend.services.agent_manager import AgentManager
from backend.services.ai_service import AIService
from backend.services.memory_service import MemoryService
from backend.services.research_service import ResearchService


class ConversationService:
    def __init__(
        self,
        db: Session,
        ai_service: AIService,
        memory_service: MemoryService,
        research_service: ResearchService,
    ) -> None:
        self.db = db
        self.memory_service = memory_service
        self.ai_service = ai_service
        self.research_service = research_service
        self.agent_manager = AgentManager(ai_service, self.research_service)

    async def process_message(
        self,
        user_id: int,
        message: str,
        conversation_id: int | None = None,
        provider_name: str = "openai",
        use_research: bool = False,
        model: str | None = None,
        preferred_agent: str | None = None,
    ) -> tuple[str, int]:
        conversation = self.memory_service.ensure_conversation(self.db, user_id, conversation_id)
        self.memory_service.save_message(self.db, conversation.id, "user", message)
        response_text = await self.agent_manager.handle_message(
            message,
            provider_name=provider_name,
            use_research=use_research,
            model=model,
            preferred_agent=preferred_agent,
        )
        self.memory_service.save_message(self.db, conversation.id, "assistant", response_text)
        return response_text, conversation.id
