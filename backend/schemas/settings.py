from pydantic import BaseModel


class SettingsUpdate(BaseModel):
    preferred_model: str | None = None
    preferred_agent: str | None = None
    voice_enabled: bool | None = None
    external_research_enabled: bool | None = None


class SettingsRead(BaseModel):
    preferred_model: str
    preferred_agent: str | None = None
    voice_enabled: bool
    external_research_enabled: bool

    class Config:
        orm_mode = True
