from backend.memory.long_memory import LongMemory
from backend.memory.short_memory import ShortMemory


class MemoryManager:
    def __init__(self) -> None:
        self.short_memory = ShortMemory()
        self.long_memory = LongMemory()

    def add_message(self, conversation_id: int, role: str, content: str) -> None:
        self.short_memory.add_message(conversation_id, role, content)

    def get_recent(self, conversation_id: int, limit: int = 20) -> list[dict[str, str]]:
        return self.short_memory.get_recent(conversation_id, limit)

    def store_long(self, conversation_id: int, content: str) -> None:
        self.long_memory.store(conversation_id, content)

    def recall(self, conversation_id: int) -> str:
        return self.long_memory.recall(conversation_id)
