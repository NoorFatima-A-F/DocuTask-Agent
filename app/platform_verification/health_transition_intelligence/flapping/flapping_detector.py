"""
Health Flapping Detector (Part 3H.3.3.7).
Identifies rapid oscillatory transitions between healthy and failed states
and activates dampening to prevent destructive container restart storms.
"""
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from app.platform_verification.health_transition_intelligence.domain.models import (
    HealthState,
    FlappingReport,
)


class HealthFlappingDetector:
    """
    Monitors transition frequency to detect and mitigate service flapping.
    """

    def __init__(
        self,
        service_name: str = "docutask-worker",
        max_transitions_window_seconds: int = 600,
        max_allowed_transitions: int = 5,
    ):
        self.service_name = service_name
        self.window_seconds = max_transitions_window_seconds
        self.max_allowed_transitions = max_allowed_transitions
        self._transition_timestamps: List[datetime] = []
        self._suppressed_restarts = 0

    def record_transition(
        self,
        from_state: HealthState,
        to_state: HealthState,
        now: Optional[datetime] = None,
    ) -> FlappingReport:
        current_time = now or datetime.now(timezone.utc)
        self._transition_timestamps.append(current_time)

        # Prune events outside window
        cutoff = current_time - timedelta(seconds=self.window_seconds)
        self._transition_timestamps = [t for t in self._transition_timestamps if t >= cutoff]

        count = len(self._transition_timestamps)
        flapping_detected = count > self.max_allowed_transitions

        if flapping_detected:
            self._suppressed_restarts += 1

        return FlappingReport(
            service=self.service_name,
            flapping_detected=flapping_detected,
            transition_count=count,
            window_seconds=self.window_seconds,
            dampening_active=flapping_detected,
            suppressed_restart_count=self._suppressed_restarts,
            passed=True,
            details={
                "threshold": self.max_allowed_transitions,
                "mitigation_action": "Dampen probe oscillation and prevent container restart loop" if flapping_detected else "Normal operation",
            },
        )
