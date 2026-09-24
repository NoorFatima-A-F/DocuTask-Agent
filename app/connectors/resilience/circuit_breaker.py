"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Circuit Breaker.
Protects upstream workflows and the platform kernel from cascading connector failures.
States: CLOSED -> OPEN -> HALF_OPEN -> RECOVERY.
"""

from __future__ import annotations

from enum import Enum
import logging
import time
from typing import Any, Callable, Optional
from pydantic import BaseModel

from app.connectors.core.exceptions import CircuitBreakerOpenError

logger = logging.getLogger(__name__)


class CircuitState(str, Enum):
    """Four-state circuit breaker finite state machine."""
    CLOSED = "CLOSED"        # Normal operations; calls are allowed through
    OPEN = "OPEN"            # Tripped; calls immediately fail fast
    HALF_OPEN = "HALF_OPEN"  # Testing recovery; allows a limited probe call
    RECOVERY = "RECOVERY"    # Progressive stabilization phase


class CircuitBreakerConfig(BaseModel):
    """Configuration for circuit breaker failure thresholds and reset windows."""
    failure_threshold: int = 5
    recovery_timeout_seconds: float = 10.0
    half_open_success_threshold: int = 2
    failure_window_seconds: float = 60.0


class CircuitBreaker:
    """
    Per-connector circuit breaker isolating unstable downstream external APIs.
    """

    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self._consecutive_failures = 0
        self._consecutive_successes = 0
        self._last_state_change = time.time()
        self._last_failure_time: Optional[float] = None

    def allow_request(self) -> bool:
        """
        Determines whether a request may proceed based on the circuit state.
        """
        now = time.time()

        if self.state == CircuitState.CLOSED:
            return True

        elif self.state == CircuitState.OPEN:
            # Check if recovery timeout has elapsed to enter HALF_OPEN
            if now - self._last_state_change >= self.config.recovery_timeout_seconds:
                self._transition_to(CircuitState.HALF_OPEN, "Recovery timeout elapsed")
                return True
            return False

        elif self.state == CircuitState.HALF_OPEN:
            # Allow trial traffic
            return True

        elif self.state == CircuitState.RECOVERY:
            return True

        return False

    def record_success(self) -> None:
        """Records a successful connector call and advances recovery state."""
        self._consecutive_failures = 0

        if self.state == CircuitState.HALF_OPEN:
            self._consecutive_successes += 1
            if self._consecutive_successes >= self.config.half_open_success_threshold:
                self._transition_to(CircuitState.CLOSED, "Target successfully recovered")
        elif self.state == CircuitState.RECOVERY:
            self._transition_to(CircuitState.CLOSED, "Stabilization complete")

    def record_failure(self, error: Optional[Exception] = None) -> None:
        """Records a failure and trips the breaker if threshold is exceeded."""
        self._consecutive_failures += 1
        self._last_failure_time = time.time()
        self._consecutive_successes = 0

        if self.state in (CircuitState.CLOSED, CircuitState.RECOVERY):
            if self._consecutive_failures >= self.config.failure_threshold:
                self._transition_to(CircuitState.OPEN, f"Failure threshold ({self.config.failure_threshold}) exceeded: {error}")
        elif self.state == CircuitState.HALF_OPEN:
            # Immediate trip back to OPEN on any failure during trial
            self._transition_to(CircuitState.OPEN, f"Failed probe in HALF_OPEN: {error}")

    def _transition_to(self, new_state: CircuitState, reason: str) -> None:
        old_state = self.state
        self.state = new_state
        self._last_state_change = time.time()
        logger.info(f"CircuitBreaker '{self.name}' transitioned {old_state.value} -> {new_state.value}: {reason}")

    def call(self, func: Callable[[], Any]) -> Any:
        """Executes a callable through the circuit breaker."""
        if not self.allow_request():
            raise CircuitBreakerOpenError(
                f"Circuit breaker '{self.name}' is OPEN. Requests blocked to prevent cascading failure.",
                connector_id=self.name,
            )

        try:
            result = func()
            self.record_success()
            return result
        except Exception as e:
            self.record_failure(e)
            raise
