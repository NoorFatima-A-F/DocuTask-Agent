"""
Runtime Backpressure System.
Monitors queue depths, resource saturation, and determines dynamic backpressure states.
"""

from enum import Enum


class BackpressureState(str, Enum):
    """Platform saturation level."""
    NORMAL = "NORMAL"
    THROTTLED = "THROTTLED"
    SHEDDING = "SHEDDING"


class BackpressureMonitor:
    """Evaluates queue saturation and computes backpressure level."""

    def __init__(self, throttle_threshold: int = 100, shedding_threshold: int = 500) -> None:
        self.throttle_threshold = throttle_threshold
        self.shedding_threshold = shedding_threshold

    def evaluate_state(self, current_queue_depth: int) -> BackpressureState:
        """Determines backpressure state from current pending queue depth."""
        if current_queue_depth >= self.shedding_threshold:
            return BackpressureState.SHEDDING
        elif current_queue_depth >= self.throttle_threshold:
            return BackpressureState.THROTTLED
        return BackpressureState.NORMAL
