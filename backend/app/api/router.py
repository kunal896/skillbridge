from fastapi import APIRouter
from app.api.routes import auth, health, learners, roadmaps

api_router = APIRouter()
for r in [health.router, auth.router, learners.router, roadmaps.router]:
    api_router.include_router(r)