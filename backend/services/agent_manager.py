from typing import Optional

from backend.agents.assistant import AssistantAgent
from backend.agents.coder import CoderAgent
from backend.agents.planner import PlannerAgent
from backend.agents.researcher import ResearchAgent
from backend.services.ai_service import AIService
from backend.services.research_service import ResearchService


class AgentManager:
    def __init__(self, ai_service: AIService, research_service: ResearchService | None = None) -> None:
        self.ai_service = ai_service
        self.research_service = research_service
        self.agent_map = {
            "assistant": AssistantAgent(),
            "coder": CoderAgent(),
            "researcher": ResearchAgent(),
            "planner": PlannerAgent(),
        }

    async def handle_message(
        self,
        message: str,
        provider_name: str = "openai",
        preferred_agent: str | None = None,
        use_research: bool = False,
        model: str | None = None,
    ) -> str:
        selected_agent = preferred_agent if preferred_agent in self.agent_map else self._select_agent(message)
        prompt_message = message
        if use_research and self.research_service:
            research_data = await self.research_service.search(message)
            prompt_message = f"{message}\n\nUse the following external findings to improve your answer:\n{research_data}"

        agent = self.agent_map.get(selected_agent, self.agent_map["assistant"])
        prompt = agent.create_prompt(prompt_message)
        return await self.ai_service.generate(prompt, provider_name=provider_name, model=model)

    def _select_agent(self, message: str) -> str:
        key = message.lower()
        if any(term in key for term in ["kod", "hata", "script", "api", "code"]):
            return "coder"
        if any(term in key for term in ["araştır", "web", "internet", "kaynak", "research"]):
            return "researcher"
        if any(term in key for term in ["plan", "yol haritası", "adım", "task", "planlama"]):
            return "planner"
        return "assistant"
