"""
Platform Kernel Health Checking Protocols and Data Models.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class HealthStatus(str, Enum):
    """Health classification status for any platform component or service."""
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ComponentHealth:
    """Standard health evaluation report for a single platform component."""
    component_name: str
    status: HealthStatus = HealthStatus.HEALTHY
    latency_ms: float = 0.0
    message: str = "Component operational"
    checked_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "component_name": self.component_name,
            "status": self.status.value,
            "latency_ms": round(self.latency_ms, 2),
            "message": self.message,
            "checked_at": self.checked_at.isoformat(),
            "details": self.details,
        }


class IHealthCheckable(ABC):
    """Interface for components that can be polled for health."""

    @abstractmethod
    async def check_health(self) -> ComponentHealth:
        """Perform health check and return report."""
        pass
