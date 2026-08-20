import sys
from pathlib import Path

# backend/app/main.py -> parents[2] is the repo root (skillbridge/), which is
# where the sibling `agents/` and `shared/` packages live. Without this, the
# app only imports them correctly if PYTHONPATH happens to include the repo
# root already (true for `uvicorn app.main:app` run from backend/ with
# PYTHONPATH set, false for a lot of one-off deploy start commands).
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings
@asynccontextmanager
async def lifespan(_:FastAPI): yield
app=FastAPI(title=settings.app_name,version="0.2.0",description="Backend API for SkillBridge.",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=[settings.frontend_url],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(api_router,prefix=settings.api_v1_prefix)
