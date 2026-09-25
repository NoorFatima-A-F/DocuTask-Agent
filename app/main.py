"""
FastAPI Application Entry Point.
Initializes application, CORS middleware, exception handlers, and API routers.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

    # Include Routers
    app.include_router(api_v1_router, prefix=settings.API_V1_STR)

    # Root route serving the full HITL Frontend Dashboard
    @app.get("/", include_in_schema=False)
    async def serve_frontend():
        import os
        from fastapi.responses import FileResponse, HTMLResponse
        frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist", "index.html")
        if os.path.exists(frontend_path):
            return FileResponse(frontend_path)
        return HTMLResponse("<h1>DocuTask Agent API</h1><p>Visit <a href='/api/v1/docs'>/api/v1/docs</a> for API inspection.</p>")

    return app


app = create_application()

