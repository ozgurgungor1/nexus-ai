from sqlalchemy.orm import Session

from backend.database.models import UserSettings


class SettingsService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_settings(self, user_id: int) -> UserSettings | None:
        return self.db.query(UserSettings).filter(UserSettings.user_id == user_id).first()

    def update_settings(
        self,
        user_id: int,
        preferred_model: str | None = None,
        preferred_agent: str | None = None,
        voice_enabled: bool | None = None,
        external_research_enabled: bool | None = None,
    ) -> UserSettings:
        settings = self.get_settings(user_id)
        if settings is None:
            settings = UserSettings(user_id=user_id)
            self.db.add(settings)

        if preferred_model is not None:
            settings.preferred_model = preferred_model
        if preferred_agent is not None:
            settings.preferred_agent = preferred_agent
        if voice_enabled is not None:
            settings.voice_enabled = voice_enabled
        if external_research_enabled is not None:
            settings.external_research_enabled = external_research_enabled

        self.db.commit()
        self.db.refresh(settings)
        return settings
