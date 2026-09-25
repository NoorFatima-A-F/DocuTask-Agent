"""
Multi-Region Failover REST API Subsystem.
"""
from app.platform_verification.multi_region_failover.api.failover_api import (
    router,
)

__all__ = ["router"]
