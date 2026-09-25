"""Circuit Breaker Pattern Implementation."""

from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional

from ..mesh.data_plane import MeshRequest, MeshResponse


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


@dataclass
class CircuitBreakerConfig:
    failure_rate_threshold_pct: float = 50.0  # 50%
    slow_call_rate_threshold_pct: float = 50.0
    slow_call_duration_ms: float = 1000.0
    wait_duration_in_open_seconds: float = 5.0
    sliding_window_size: int = 10
    minimum_number_of_calls: int = 5
    permitted_calls_in_half_open: int = 3


class CircuitBreaker:
    """Stateful circuit breaker guarding downstream services against cascading failure."""

    def __init__(self, service_name: str, config: Optional[CircuitBreakerConfig] = None):
        self.service_name = service_name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self._window: List[tuple[bool, bool]] = []  # List of (is_failure, is_slow)
        self._last_state_change: float = time.time()
        self._half_open_calls: int = 0
        self._half_open_successes: int = 0

    def can_execute(self) -> bool:
        """Check if request can proceed through the circuit breaker."""
        now = time.time()
        if self.state == CircuitState.CLOSED:
            return True
        elif self.state == CircuitState.OPEN:
            if (now - self._last_state_change) >= self.config.wait_duration_in_open_seconds:
                # Transition to HALF_OPEN
                self.state = CircuitState.HALF_OPEN
                self._last_state_change = now
                self._half_open_calls = 0
                self._half_open_successes = 0
                return True
            return False
        elif self.state == CircuitState.HALF_OPEN:
            return self._half_open_calls < self.config.permitted_calls_in_half_open
        return False

    def record_result(self, is_failure: bool, duration_ms: float = 0.0) -> None:
        """Record the outcome of a service invocation."""
        is_slow = duration_ms >= self.config.slow_call_duration_ms
        now = time.time()

        if self.state == CircuitState.HALF_OPEN:
            self._half_open_calls += 1
            if not is_failure:
                self._half_open_successes += 1

            if self._half_open_calls >= self.config.permitted_calls_in_half_open:
                if self._half_open_successes == self.config.permitted_calls_in_half_open:
                    # All trial calls succeeded -> transition to CLOSED
                    self.state = CircuitState.CLOSED
                    self._window.clear()
                    self._last_state_change = now
                else:
                    # One or more failed -> transition back to OPEN
                    self.state = CircuitState.OPEN
                    self._last_state_change = now
            return

        if self.state == CircuitState.CLOSED:
            self._window.append((is_failure, is_slow))
            if len(self._window) > self.config.sliding_window_size:
                self._window.pop(0)

            if len(self._window) >= self.config.minimum_number_of_calls:
                failures = sum(1 for f, _ in self._window if f)
                slow_calls = sum(1 for _, s in self._window if s)
                total = len(self._window)

                failure_rate = (failures / total) * 100.0
                slow_rate = (slow_calls / total) * 100.0

                if failure_rate >= self.config.failure_rate_threshold_pct or slow_rate >= self.config.slow_call_rate_threshold_pct:
                    self.state = CircuitState.OPEN
                    self._last_state_change = now

    def execute(
        self,
        request: MeshRequest,
        operation_fn: Callable[[MeshRequest], MeshResponse],
        fallback_fn: Optional[Callable[[MeshRequest], MeshResponse]] = None,
    ) -> MeshResponse:
        """Execute request under circuit breaker protection."""
        if not self.can_execute():
            if fallback_fn:
                return fallback_fn(request)
            return MeshResponse(
                status_code=503,
                error_message=f"Circuit breaker for {self.service_name} is OPEN",
                request_id=request.request_id,
            )

        start_time = time.time()
        try:
            response = operation_fn(request)
            duration_ms = (time.time() - start_time) * 1000.0
            is_failure = response.status_code >= 500
            self.record_result(is_failure=is_failure, duration_ms=duration_ms)
            return response
        except Exception as ex:
            duration_ms = (time.time() - start_time) * 1000.0
            self.record_result(is_failure=True, duration_ms=duration_ms)
            if fallback_fn:
                return fallback_fn(request)
            return MeshResponse(
                status_code=503,
                error_message=f"Circuit execution exception: {str(ex)}",
                request_id=request.request_id,
            )
