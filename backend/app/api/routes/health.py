from fastapi import APIRouter
from app.core.config import settings
from app.schemas.common import HealthResponse
router=APIRouter(tags=["health"])
@router.get("/health",response_model=HealthResponse)
def health():return HealthResponse(status="ok",service=settings.app_name,environment=settings.environment)
