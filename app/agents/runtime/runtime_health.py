"""
Runtime Health Aggregation Model.
Aggregates health, readiness, and latencies across all 9 platform subsystems into a single health report.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SubsystemHealthStatus(str, Enum):
    """Health classification for a platform subsystem."""
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


class SubsystemHealthReport(BaseModel):
    """Health evaluation of an individual platform subsystem."""
    subsystem_name: str
    status: SubsystemHealthStatus = SubsystemHealthStatus.HEALTHY
    latency_ms: float = 0.0
    details: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class PlatformHealthReport(BaseModel):
    """Unified health report for the entire agent platform."""
    overall_status: SubsystemHealthStatus = SubsystemHealthStatus.HEALTHY
    healthy_count: int = 0
    degraded_count: int = 0
    unhealthy_count: int = 0
    subsystems: Dict[str, SubsystemHealthReport] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def aggregate(cls, reports: List[SubsystemHealthReport]) -> "PlatformHealthReport":
        """Calculates aggregate health status across all individual reports."""
        subsystems_map = {r.subsystem_name: r for r in reports}
        h_count = sum(1 for r in reports if r.status == SubsystemHealthStatus.HEALTHY)
        d_count = sum(1 for r in reports if r.status == SubsystemHealthStatus.DEGRADED)
        u_count = sum(1 for r in reports if r.status == SubsystemHealthStatus.UNHEALTHY)

        if u_count > 0:
            overall = SubsystemHealthStatus.UNHEALTHY
        elif d_count > 0:
            overall = SubsystemHealthStatus.DEGRADED
        else:
            overall = SubsystemHealthStatus.HEALTHY

        return cls(
            overall_status=overall,
            healthy_count=h_count,
            degraded_count=d_count,
            unhealthy_count=u_count,
            subsystems=subsystems_map,
        )

    model_config = {"frozen": True}
