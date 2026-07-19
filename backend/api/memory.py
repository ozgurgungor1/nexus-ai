from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.middleware.auth import get_current_user
from backend.services.memory_service import MemoryService

router = APIRouter()
memory_service = MemoryService()


@router.get("/memory")
def get_memory(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)) -> list[dict[str, object]]:
    conversations = memory_service.get_history(db, current_user["user_id"])
    return [
        {
            "conversation_id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at.isoformat(),
            "messages": [
                {
                    "id": message.id,
                    "role": message.role,
                    "content": message.content,
                    "created_at": message.created_at.isoformat(),
                }
                for message in conversation.messages
            ],
        }
        for conversation in conversations
    ]
