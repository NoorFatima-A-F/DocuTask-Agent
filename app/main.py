"""
FastAPI Application Entry Point.
Initializes application, CORS middleware, exception handlers, API routers, and Frontend SPA serving.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.health import router as health_router
from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.logging import logger
from app.database.base import Base
from app.database.session import engine
from app.dependencies.workers import get_worker_engine
from app.middleware.exception_handler import register_exception_handlers
from app.middleware.request_context import RequestContextMiddleware
from app.middleware.rate_limit import RateLimitMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for application startup and shutdown events."""
    logger.info(f"Starting {settings.PROJECT_NAME} in [{settings.ENVIRONMENT}] mode...")
    
    # Auto-create tables for development mode if SQLite / local
    if "sqlite" in settings.DATABASE_URL:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # Start Background Worker Engine
    worker_engine = get_worker_engine()
    await worker_engine.start()
            
    yield

    # Shutdown Background Worker Engine
    logger.info("Shutting down worker engine...")
    await worker_engine.stop()
    logger.info("Shutting down application...")


def find_frontend_index() -> str | None:
    """Discovers the frontend index.html across production and local dev directories."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(repo_root, "frontend", "dist", "index.html"),
        os.path.join(repo_root, "frontend", "index.html"),
        os.path.join(repo_root, "dist", "index.html"),
        os.path.join(os.getcwd(), "frontend", "dist", "index.html"),
        os.path.join(os.getcwd(), "frontend", "index.html"),
        os.path.join(os.getcwd(), "dist", "index.html"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def create_application() -> FastAPI:
    """Application factory method."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        lifespan=lifespan
    )

    # Request Context & Security Headers Middleware
    app.add_middleware(RequestContextMiddleware)

    # Rate Limiting Middleware
    app.add_middleware(RateLimitMiddleware)

    # CORS Middleware
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Exception Handlers
    register_exception_handlers(app)

    # Include Health & System Readiness Probes
    app.include_router(health_router)
    app.include_router(health_router, prefix=settings.API_V1_STR)

    # Include API Routers
    app.include_router(api_v1_router, prefix=settings.API_V1_STR)

    # Mount static assets if dist exists
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_assets_dir = os.path.join(repo_root, "frontend", "dist", "assets")
    if os.path.exists(static_assets_dir):
        app.mount("/assets", StaticFiles(directory=static_assets_dir), name="assets")

    # Favicon Route
    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # Root route and SPA Catch-all routes serving HITL Frontend Dashboard
    @app.get("/", include_in_schema=False)
    @app.get("/upload", include_in_schema=False)
    @app.get("/jobs", include_in_schema=False)
    @app.get("/jobs/{job_id}", include_in_schema=False)
    @app.get("/documents/{document_id}/review", include_in_schema=False)
    @app.get("/reviewer", include_in_schema=False)
    @app.get("/dashboard", include_in_schema=False)
    async def serve_frontend():
        index_file = find_frontend_index()
        if index_file:
            return FileResponse(index_file)
        return HTMLResponse(
            "<!DOCTYPE html><html><body style='background:#090d16;color:#fff;font-family:sans-serif;padding:2rem;text-align:center;'>"
            "<h1>DocuTask Agent API</h1>"
            "<p>API is healthy and online.</p>"
            "<a style='color:#6366f1;' href='/api/v1/docs'>Go to OpenAPI Documentation (/api/v1/docs)</a>"
            "</body></html>"
        )

    return app


app = create_application()
