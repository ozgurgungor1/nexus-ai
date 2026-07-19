from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """Health probe for external uptime and load balancers."""
    return {"status": "ok", "project": "NEXUS AI"}
