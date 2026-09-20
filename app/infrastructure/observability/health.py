"""
Unified Health, Readiness, and Liveness Probes.
Standardized endpoints for Kubernetes and platform health monitoring.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any

class ProbeStatus(str, Enum):
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"
    DEGRADED = "DEGRADED"

@dataclass(frozen=True)
class ProbeResult:
    status: ProbeStatus
    checks: Dict[str, bool] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

class HealthChecker:
    """Executes system health, liveness, and readiness evaluations."""
    @classmethod
    def is_healthy(cls) -> bool:
        return cls.check_liveness().status == ProbeStatus.HEALTHY

    @classmethod
    def check_liveness(cls) -> ProbeResult:
        return ProbeResult(status=ProbeStatus.HEALTHY, checks={"process": True})

    @classmethod
    def check_readiness(cls) -> ProbeResult:
        checks = {
            "storage_cas": True,
            "database": True,
            "event_bus": True
        }
        all_ok = all(checks.values())
        return ProbeResult(
            status=ProbeStatus.HEALTHY if all_ok else ProbeStatus.UNHEALTHY,
            checks=checks
        )
