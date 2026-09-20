"""
Readiness Decision Engine (Part 3).
Evaluates incoming dependency health signals and computes deterministic readiness states
and automated load balancer traffic routing actions.
"""
from typing import Dict, Any, Tuple
from app.platform_verification.readiness_contract.domain.models import (
    ReadinessState,
    TrafficAction,
)


class ReadinessDecisionEngine:
    """
    Evaluates system capabilities and decides traffic admission.
    """

    CRITICAL_DEPENDENCIES = ["database", "queue", "storage", "workers"]
    NON_CRITICAL_DEPENDENCIES = ["ai_provider", "analytics", "optional_monitoring"]

    def evaluate_signals(self, signals: Dict[str, str]) -> Tuple[ReadinessState, TrafficAction]:
        # Check critical dependencies
        critical_failed = any(signals.get(dep) in ["failed", "unhealthy", "down"] for dep in self.CRITICAL_DEPENDENCIES)
        if critical_failed:
            return ReadinessState.NOT_READY, TrafficAction.WITHHOLD_TRAFFIC

        # Check non-critical dependencies
        non_critical_failed = any(signals.get(dep) in ["failed", "unhealthy", "degraded", "down"] for dep in self.NON_CRITICAL_DEPENDENCIES)
        if non_critical_failed:
            return ReadinessState.DEGRADED, TrafficAction.THROTTLE_TRAFFIC

        # If all healthy
        return ReadinessState.READY, TrafficAction.ADMIT_TRAFFIC
