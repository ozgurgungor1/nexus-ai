class AssistantAgent:
    """Professional assistant agent for general inquiries."""

    def create_prompt(self, message: str) -> str:
        return (
            "You are a professional AI assistant. Answer the user's request in a clear, accurate, "
            "and concise manner. If the user asks for code, include an appropriate example. "
            f"User request: {message}"
        )
