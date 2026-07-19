from fastapi import APIRouter

from backend.api.agents import router as agents_router
from backend.api.chat import router as chat_router
from backend.api.health import router as health_router
from backend.api.history import router as history_router
from backend.api.memory import router as memory_router
from backend.api.settings import router as settings_router
from backend.api.upload import router as upload_router
from backend.api.users import router as users_router

router = APIRouter()
router.include_router(health_router, prefix="", tags=["Health"])
router.include_router(users_router, prefix="", tags=["Authentication"])
router.include_router(chat_router, prefix="", tags=["Chat"])
router.include_router(history_router, prefix="", tags=["History"])
router.include_router(upload_router, prefix="", tags=["Upload"])
router.include_router(agents_router, prefix="", tags=["Agents"])
router.include_router(settings_router, prefix="", tags=["Settings"])
router.include_router(memory_router, prefix="", tags=["Memory"])
