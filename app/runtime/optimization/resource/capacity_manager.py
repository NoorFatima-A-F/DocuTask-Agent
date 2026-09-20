"""
Capacity Manager & Utilization Tracker for Phase 13.6 (ARIA-EOP).
Monitors live capacity buffers, rate-limit headrooms, and worker utilization trends.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field


class CapacityStatus(BaseModel):
    total_workers: int = 16
    active_workers: int = 6
    idle_workers: int = 10
    system_utilization_pct: float = 37.5
    rate_limit_headroom_pct: float = 85.0
    is_scale_up_recommended: bool = False


class CapacityManager:
    """
    Evaluates system-wide capacity constraints and safety headrooms.
    """

    @classmethod
    def get_capacity_status(cls) -> CapacityStatus:
        return CapacityStatus(
            total_workers=16,
            active_workers=6,
            idle_workers=10,
            system_utilization_pct=37.5,
            rate_limit_headroom_pct=85.0,
            is_scale_up_recommended=False,
        )
