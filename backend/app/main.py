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
