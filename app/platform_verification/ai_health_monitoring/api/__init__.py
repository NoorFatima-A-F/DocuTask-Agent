"""AI Monitoring API package."""

from app.platform_verification.ai_health_monitoring.api.ai_health_monitoring_api import (
    router as ai_monitoring_router,
)

__all__ = [
    "ai_monitoring_router",
]
