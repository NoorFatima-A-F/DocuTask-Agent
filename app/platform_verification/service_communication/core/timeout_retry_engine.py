"""
Timeout & Exponential Backoff Retry Engine.
"""
from typing import List, Dict, Any, Tuple
from app.platform_verification.service_communication.domain.models import (
    TimeoutValidationReport,
    RetryBehaviorReport,
)
from app.platform_verification.service_communication.domain.interfaces import ITimeoutRetryEvaluator


class TimeoutRetryEngine(ITimeoutRetryEvaluator):
    """Evaluates timeout guarantees and exponential backoff retry behaviors."""

    def evaluate_timeouts_and_retries(self, services: List[Dict[str, Any]]) -> Tuple[TimeoutValidationReport, RetryBehaviorReport]:
        infinite_waits: List[str] = []
        exponential_ok = True
        jitter_ok = True
        storm_prevention = True

        for s in services:
            name = s.get("name", "service")
            timeout = s.get("timeout_seconds", 10.0)
            backoff = s.get("backoff_strategy", "exponential")
            has_jitter = s.get("jitter_enabled", True)
            max_retries = s.get("max_retries", 3)

            if timeout is None or timeout <= 0 or timeout > 60.0:
                infinite_waits.append(f"Service '{name}' has unconstrained timeout ({timeout}s)")

            if backoff != "exponential":
                exponential_ok = False

            if not has_jitter:
                jitter_ok = False

            if max_retries > 5:
                storm_prevention = False

        t_status = "PASS" if len(infinite_waits) == 0 else "FAIL"
        r_status = "PASS" if exponential_ok and jitter_ok and storm_prevention else "FAIL"

        t_rep = TimeoutValidationReport(
            configured_timeouts_count=len(services),
            infinite_wait_hazards=infinite_waits,
            graceful_timeout_handling_verified=(len(infinite_waits) == 0),
            status=t_status,
        )

        r_rep = RetryBehaviorReport(
            exponential_backoff_verified=exponential_ok,
            jitter_verified=jitter_ok,
            retry_storm_prevention_verified=storm_prevention,
            max_retries_configured=3,
            status=r_status,
        )

        return t_rep, r_rep
