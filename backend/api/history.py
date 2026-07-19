from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.middleware.auth import get_current_user
from backend.services.memory_service import MemoryService

router = APIRouter()
memory_service = MemoryService()


@router.get("/history")
def get_history(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)) -> list[dict[str, str | int]]:
    conversations = memory_service.get_history(db, current_user["user_id"])
    return [
        {"conversation_id": conversation.id, "title": conversation.title, "created_at": conversation.created_at.isoformat()}
        for conversation in conversations
    ]


@router.delete("/history")
def delete_history(
    conversation_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict[str, str]:
    memory_service.delete_conversation(db, conversation_id, current_user["user_id"])
    return {"status": "deleted", "conversation_id": str(conversation_id)}
