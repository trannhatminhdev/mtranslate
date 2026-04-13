"""
MTrans Backend API - AI Voice Translation Service

Main entry point for the FastAPI application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common.config import settings
from gateway.ws_gateway import router as ws_router
from modules.health.router import router as health_router
from modules.languages.router import router as languages_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events."""
    # Startup
    print(f"🚀 MTrans Backend starting on {settings.HOST}:{settings.PORT}")
    print(f"📡 STT Provider: {settings.STT_PROVIDER}")
    print(f"🌐 Translation Provider: {settings.TRANSLATION_PROVIDER}")
    print(f"🔈 TTS Provider: {settings.TTS_PROVIDER}")
    yield
    # Shutdown
    print("👋 MTrans Backend shutting down")


app = FastAPI(
    title="MTrans API",
    description="AI-powered real-time voice translation service",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(languages_router, prefix="/api", tags=["Languages"])
app.include_router(ws_router, tags=["WebSocket"])
