from pydantic import BaseModel


class AgentSelection(BaseModel):
    agent_name: str


class AgentInfo(BaseModel):
    name: str
    description: str
