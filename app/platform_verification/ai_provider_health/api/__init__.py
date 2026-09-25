"""AI API package."""

from app.platform_verification.ai_provider_health.api.ai_provider_health_api import router as ai_health_router

__all__ = [
    "ai_health_router",
]
