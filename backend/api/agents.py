from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.middleware.auth import get_current_user
from backend.schemas.agents import AgentInfo, AgentSelection
from backend.services.settings_service import SettingsService

router = APIRouter()


tag_definitions = [
    AgentInfo(name="assistant", description="General assistant for conversational and productivity tasks."),
    AgentInfo(name="coder", description="Software engineering expert for code generation and debugging."),
    AgentInfo(name="researcher", description="Research-focused agent for summarization, analysis, and web research."),
    AgentInfo(name="planner", description="Planning agent for roadmaps, breakdowns, and execution guidance."),
]


@router.get("/agents", response_model=list[AgentInfo])
def get_agents() -> list[AgentInfo]:
    return tag_definitions


@router.post("/agents/select")
def select_agent(
    selection: AgentSelection,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict[str, str]:
    if selection.agent_name not in {agent.name for agent in tag_definitions}:
        raise HTTPException(status_code=400, detail="Unknown agent")

    service = SettingsService(db)
    service.update_settings(current_user["user_id"], preferred_agent=selection.agent_name)
    return {"selected_agent": selection.agent_name}
