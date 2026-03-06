"""
Main FastAPI application entry point.
This app serves both the ADK agent API and the background worker endpoints.
"""

from contextlib import asynccontextmanager

import structlog
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from variants_coordinator.core.config import settings
from variants_coordinator.core.initialization import initialize_clients_and_runner
from variants_coordinator.routes.agent_router import router as agent_api_router
from variants_coordinator.routes.auth_router import router as auth_api_router
from variants_coordinator.routes.worker_router import router as worker_api_router

logger = structlog.get_logger(__name__)


# Application Lifespan Manager
@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Handles application startup and shutdown events.
    This is the ideal place to initialize resources like database clients.
    The underscore '_' indicates that we are intentionally not using the 'app'
    parameter passed by FastAPI.
    """
    logger.info("Application startup: Initializing Google Cloud clients...")
    initialize_clients_and_runner()
    logger.info("Cloud clients initialized successfully.")

    yield

    logger.info("Application shutdown.")


# --- Create FastAPI app with the lifespan manager ---
app = FastAPI(
    title="Genomic Variant Analysis Agent API",
    description="A multi-agent system for genomic analysis.",
    version="1.0.0",
    lifespan=lifespan,
)

# Middleware
# Configure CORS based on environment
if settings.demo_mode or settings.log_level == "DEBUG":
    # Development mode - allow all origins
    cors_origins = ["*"]
else:
    # Production mode - restrict to specific origins
    cors_origins = [
        origin.strip() for origin in settings.cors_production_origins.split(",")
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# API Routers
if settings.public_api_prefix:
    api_router = APIRouter(prefix=settings.public_api_prefix)
    api_router.include_router(auth_api_router, tags=["Auth"])
    api_router.include_router(agent_api_router, tags=["Agent"])
    api_router.include_router(worker_api_router, tags=["Worker"])
    app.include_router(api_router)
else:
    app.include_router(auth_api_router, tags=["Auth"])
    app.include_router(agent_api_router, tags=["Agent"])
    app.include_router(worker_api_router, tags=["Worker"])


# Root Endpoint
@app.get("/")
async def root():
    """A simple health check endpoint."""
    return {
        "message": "Genomic Variant Analysis Agent API is running.",
        "version": "1.0.0",
        "authentication": "Firebase Auth enabled",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "genomic-variant-analysis",
        "version": "1.0.0",
    }


# Uvicorn Runner
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level.lower(),
    )
