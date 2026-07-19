class ResearchAgent:
    """Research agent for generating summaries, references, and fact-based answers."""

    def create_prompt(self, message: str) -> str:
        return (
            "You are a research assistant. Collect relevant facts, summarize the most important findings, "
            "and present them clearly. When possible, include suggested next steps. "
            f"User request: {message}"
        )
