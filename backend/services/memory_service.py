from sqlalchemy.orm import Session

from backend.database.models import Conversation, Message


class MemoryService:
    def ensure_conversation(self, db: Session, user_id: int, conversation_id: int | None) -> Conversation:
        if conversation_id is not None:
            conversation = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == user_id).first()
            if conversation:
                return conversation

        conversation = Conversation(user_id=user_id, title="New Conversation")
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    def save_message(self, db: Session, conversation_id: int, role: str, content: str) -> Message:
        message = Message(conversation_id=conversation_id, role=role, content=content)
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    def get_history(self, db: Session, user_id: int) -> list[Conversation]:
        return db.query(Conversation).filter(Conversation.user_id == user_id).all()

    def delete_conversation(self, db: Session, conversation_id: int, user_id: int) -> None:
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == user_id).first()
        if conversation:
            db.delete(conversation)
            db.commit()
