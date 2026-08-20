from fastapi import APIRouter
from app.api.routes import auth, health, learners

api_router = APIRouter()
for r in [health.router, auth.router, learners.router]:
    api_router.include_router(r)