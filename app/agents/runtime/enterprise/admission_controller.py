"""
Runtime Admission Controller.
Controls intake admission based on current backpressure state and request priority.
"""

from typing import Any, Dict, Optional
from app.agents.runtime.enterprise.backpressure import BackpressureMonitor, BackpressureState
from app.agents.runtime.enterprise.scheduler_state import JobPriority
from app.agents.runtime.exceptions import RuntimeKernelException


class RequestSheddedError(RuntimeKernelException):
    """Raised when an intake request is rejected due to load shedding."""
    pass


class AdmissionController:
    """Gates request admission to preserve runtime kernel responsiveness."""

    def __init__(self, monitor: Optional[BackpressureMonitor] = None) -> None:
        self.monitor = monitor or BackpressureMonitor()

    def can_admit(self, priority: JobPriority, current_queue_depth: int) -> bool:
        """Determines if a request with given priority can be admitted."""
        state = self.monitor.evaluate_state(current_queue_depth)

        if state == BackpressureState.NORMAL:
            return True
        elif state == BackpressureState.THROTTLED:
            # Drop LOW priority when throttled
            return priority != JobPriority.LOW
        elif state == BackpressureState.SHEDDING:
            # Only CRITICAL requests admitted when shedding
            return priority == JobPriority.CRITICAL

    def admit_or_reject(self, priority: JobPriority, current_queue_depth: int) -> None:
        """Admits request or raises RequestSheddedError."""
        if not self.can_admit(priority, current_queue_depth):
            raise RequestSheddedError(
                f"Request with priority {priority.name} was shedded due to backpressure (queue depth={current_queue_depth})."
            )
