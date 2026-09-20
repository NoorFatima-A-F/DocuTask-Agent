"""
Circuit Breaker Implementation.
Manages failure thresholds and transition between Closed, Open, and Half-Open states.
"""

from datetime import datetime, timezone
from enum import Enum
from app.agents.recovery.exceptions import CircuitBreakerOpenException


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreaker:
    """Protects external tools, workers, and providers from catastrophic cascading failures."""

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_seconds: float = 30.0
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: float = 0.0

    def record_success(self) -> None:
        """Records a successful operation, resetting failure counters."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def record_failure(self) -> None:
        """Records a failure, transitioning to OPEN if threshold is exceeded."""
        self.failure_count += 1
        self.last_failure_time = datetime.now(timezone.utc).timestamp()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def allow_execution(self) -> bool:
        """Checks if operation execution is permitted."""
        if self.state == CircuitState.CLOSED:
            return True

        now = datetime.now(timezone.utc).timestamp()
        if self.state == CircuitState.OPEN:
            if now - self.last_failure_time >= self.recovery_timeout_seconds:
                self.state = CircuitState.HALF_OPEN
                return True
            raise CircuitBreakerOpenException(f"Circuit breaker '{self.name}' is OPEN. Execution rejected.")

        # HALF_OPEN allows single trial probe
        return True
