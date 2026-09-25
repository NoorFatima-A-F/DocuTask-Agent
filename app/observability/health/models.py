"""
Observability Health Domain Models.
6-level health hierarchy: Organization -> Platform -> Module -> Service -> Worker -> Connector.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict
from ...platform.kernel.health import HealthStatus


class HealthLevel(str, Enum):
    ORGANIZATION = "ORGANIZATION"
    PLATFORM = "PLATFORM"
    MODULE = "MODULE"
    SERVICE = "SERVICE"
    WORKER = "WORKER"
    CONNECTOR = "CONNECTOR"


@dataclass
class HealthCheckResult:
    """Result of an individual subsystem health check."""
    name: str
    level: HealthLevel = HealthLevel.SERVICE
    status: HealthStatus = HealthStatus.HEALTHY
    latency_ms: float = 0.0
    message: str = "OK"
    checked_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "level": self.level.value,
            "status": self.status.value,
            "latency_ms": round(self.latency_ms, 2),
            "message": self.message,
            "checked_at": self.checked_at.isoformat(),
            "details": self.details,
        }


@dataclass
class PlatformHealthReport:
    """Aggregate platform health report with live/ready/startup evaluation."""
    status: HealthStatus
    uptime_seconds: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    live: bool = True
    ready: bool = True
    startup_complete: bool = True
    checks: Dict[str, HealthCheckResult] = field(default_factory=dict)
    summary: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "live": self.live,
            "ready": self.ready,
            "startup_complete": self.startup_complete,
            "uptime_seconds": round(self.uptime_seconds, 2),
            "timestamp": self.timestamp.isoformat(),
            "summary": self.summary,
            "checks": {k: v.to_dict() for k, v in self.checks.items()},
        }
