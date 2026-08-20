from fastapi import APIRouter
from app.api.routes import auth,diagnosis,employers,health,jobs,learners,matches,roadmaps,verification
api_router=APIRouter()
for r in [health.router,auth.router,learners.router,diagnosis.router,jobs.router,roadmaps.router,verification.router,employers.router,matches.router]: api_router.include_router(r)