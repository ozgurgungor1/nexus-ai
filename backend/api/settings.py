from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.middleware.auth import get_current_user
from backend.schemas.settings import SettingsRead, SettingsUpdate
from backend.services.settings_service import SettingsService

router = APIRouter()


@router.get("/settings", response_model=SettingsRead)
def get_settings(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)) -> SettingsRead:
    service = SettingsService(db)
    settings = service.get_settings(current_user["user_id"])
    if settings is None:
        settings = service.update_settings(current_user["user_id"])
    return settings


@router.post("/settings", response_model=SettingsRead)
def update_settings(
    payload: SettingsUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> SettingsRead:
    service = SettingsService(db)
    settings = service.update_settings(
        current_user["user_id"],
        preferred_model=payload.preferred_model,
        preferred_agent=payload.preferred_agent,
        voice_enabled=payload.voice_enabled,
        external_research_enabled=payload.external_research_enabled,
    )
    return settings
