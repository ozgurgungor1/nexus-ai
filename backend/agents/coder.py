class CoderAgent:
    """Expert coding agent that provides code solutions and debugging assistance."""

    def create_prompt(self, message: str) -> str:
        return (
            "You are a senior software engineer. Analyze the user's request and return a professional "
            "solution with code examples, implementation details, and explanations. "
            f"User request: {message}"
        )
