class PlannerAgent:
    """Planning agent for roadmaps, task breakdowns, and execution strategy."""

    def create_prompt(self, message: str) -> str:
        return (
            "You are a planning agent. Create a practical, step-by-step plan for the user's objective, "
            "with milestones and risks where appropriate. "
            f"User request: {message}"
        )
