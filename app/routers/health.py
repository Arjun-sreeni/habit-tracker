from fastapi import APIRouter
from app.config import settings


router = APIRouter(
    tags=["health"]
)

@router.get("/health")
def health():
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "debug": settings.debug
    }

