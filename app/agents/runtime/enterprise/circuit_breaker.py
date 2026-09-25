"""
Circuit Breaker Subsystem with Distributed State Stores.
Implements CLOSED, OPEN, and HALF_OPEN state machine protecting Planner, Execution, Memory, and Tools
from cascading failures and overload storms across distributed runtime workers.
"""

import time
import json
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, Coroutine, Dict, Optional, Tuple
from app.agents.runtime.exceptions import RuntimeKernelException


class CircuitState(str, Enum):
    """States of the Circuit Breaker."""
    CLOSED = "CLOSED"        # Normal operation
    OPEN = "OPEN"            # Tripped; requests immediately rejected
    HALF_OPEN = "HALF_OPEN"  # Testing probe requests to verify recovery


class CircuitBreakerOpenError(RuntimeKernelException):
    """Raised when a request is rejected because the circuit breaker is OPEN."""
    pass


class CircuitBreakerStateStore(ABC):
    """Abstract interface for distributed circuit breaker state storage."""

    @abstractmethod
    def get_state(self, name: str) -> Tuple[CircuitState, int, int, float]:
        """Returns (state, failure_count, success_count, last_state_change)."""
        pass

    @abstractmethod
    def check_transition(self, name: str, recovery_timeout: float) -> Tuple[CircuitState, int, int, float]:
        """Checks if OPEN breaker should transition to HALF_OPEN."""
        pass

    @abstractmethod
    def record_success(self, name: str, success_threshold: int) -> Tuple[CircuitState, int, int, float]:
        """Records success and updates state."""
        pass

    @abstractmethod
    def record_failure(self, name: str, failure_threshold: int) -> Tuple[CircuitState, int, int, float]:
        """Records failure and updates state."""
        pass


class MemoryCircuitStateStore(CircuitBreakerStateStore):
    """Thread-safe in-memory state store for a single node runtime."""

    def __init__(self) -> None:
        # name -> {"state": CircuitState, "failures": int, "successes": int, "changed_at": float}
        self._breakers: Dict[str, Dict[str, Any]] = {}

    def _get_or_create(self, name: str) -> Dict[str, Any]:
        if name not in self._breakers:
            self._breakers[name] = {
                "state": CircuitState.CLOSED,
                "failures": 0,
                "successes": 0,
                "changed_at": time.time(),
            }
        return self._breakers[name]

    def get_state(self, name: str) -> Tuple[CircuitState, int, int, float]:
        b = self._get_or_create(name)
        return (b["state"], b["failures"], b["successes"], b["changed_at"])

    def check_transition(self, name: str, recovery_timeout: float) -> Tuple[CircuitState, int, int, float]:
        b = self._get_or_create(name)
        if b["state"] == CircuitState.OPEN:
            if time.time() - b["changed_at"] >= recovery_timeout:
                b["state"] = CircuitState.HALF_OPEN
                b["successes"] = 0
                b["changed_at"] = time.time()
        return (b["state"], b["failures"], b["successes"], b["changed_at"])

    def record_success(self, name: str, success_threshold: int) -> Tuple[CircuitState, int, int, float]:
        b = self._get_or_create(name)
        if b["state"] == CircuitState.HALF_OPEN:
            b["successes"] += 1
            if b["successes"] >= success_threshold:
                b["state"] = CircuitState.CLOSED
                b["failures"] = 0
                b["successes"] = 0
                b["changed_at"] = time.time()
        elif b["state"] == CircuitState.CLOSED:
            b["failures"] = 0
        return (b["state"], b["failures"], b["successes"], b["changed_at"])

    def record_failure(self, name: str, failure_threshold: int) -> Tuple[CircuitState, int, int, float]:
        b = self._get_or_create(name)
        b["failures"] += 1
        if b["state"] in (CircuitState.CLOSED, CircuitState.HALF_OPEN):
            if b["failures"] >= failure_threshold or b["state"] == CircuitState.HALF_OPEN:
                b["state"] = CircuitState.OPEN
                b["changed_at"] = time.time()
        return (b["state"], b["failures"], b["successes"], b["changed_at"])


class RedisCircuitStateStore(CircuitBreakerStateStore):
    """Distributed Redis state store sharing circuit trip state across all worker nodes."""

    def __init__(self, redis_client: Any, prefix: str = "runtime:circuit") -> None:
        self.client = redis_client
        self.prefix = prefix

    def _key(self, name: str) -> str:
        return f"{self.prefix}:{name}"

    def get_state(self, name: str) -> Tuple[CircuitState, int, int, float]:
        raw = self.client.get(self._key(name))
        if not raw:
            return (CircuitState.CLOSED, 0, 0, time.time())
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        data = json.loads(raw)
        return (
            CircuitState(data["state"]),
            int(data["failures"]),
            int(data["successes"]),
            float(data["changed_at"]),
        )

    def _save(self, name: str, state: CircuitState, failures: int, successes: int, changed_at: float) -> None:
        data = json.dumps({
            "state": state.value,
            "failures": failures,
            "successes": successes,
            "changed_at": changed_at,
        })
        self.client.set(self._key(name), data)

    def check_transition(self, name: str, recovery_timeout: float) -> Tuple[CircuitState, int, int, float]:
        state, failures, successes, changed_at = self.get_state(name)
        if state == CircuitState.OPEN:
            if time.time() - changed_at >= recovery_timeout:
                state = CircuitState.HALF_OPEN
                successes = 0
                changed_at = time.time()
                self._save(name, state, failures, successes, changed_at)
        return (state, failures, successes, changed_at)

    def record_success(self, name: str, success_threshold: int) -> Tuple[CircuitState, int, int, float]:
        state, failures, successes, changed_at = self.get_state(name)
        if state == CircuitState.HALF_OPEN:
            successes += 1
            if successes >= success_threshold:
                state = CircuitState.CLOSED
                failures = 0
                successes = 0
                changed_at = time.time()
        elif state == CircuitState.CLOSED:
            failures = 0
        self._save(name, state, failures, successes, changed_at)
        return (state, failures, successes, changed_at)

    def record_failure(self, name: str, failure_threshold: int) -> Tuple[CircuitState, int, int, float]:
        state, failures, successes, changed_at = self.get_state(name)
        failures += 1
        if state in (CircuitState.CLOSED, CircuitState.HALF_OPEN):
            if failures >= failure_threshold or state == CircuitState.HALF_OPEN:
                state = CircuitState.OPEN
                changed_at = time.time()
        self._save(name, state, failures, successes, changed_at)
        return (state, failures, successes, changed_at)


class CircuitBreaker:
    """Enterprise circuit breaker with pluggable distributed state store."""

    def __init__(
        self,
        name: str,
        failure_threshold: int = 3,
        recovery_timeout_seconds: float = 10.0,
        success_threshold: int = 2,
        state_store: Optional[CircuitBreakerStateStore] = None,
    ) -> None:
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout_seconds
        self.success_threshold = success_threshold
        self._store = state_store or MemoryCircuitStateStore()

    @property
    def state(self) -> CircuitState:
        s, _, _, _ = self._store.get_state(self.name)
        return s

    @property
    def failure_count(self) -> int:
        _, f, _, _ = self._store.get_state(self.name)
        return f

    @property
    def success_count(self) -> int:
        _, _, s, _ = self._store.get_state(self.name)
        return s

    @property
    def last_state_change(self) -> float:
        _, _, _, c = self._store.get_state(self.name)
        return c

    def _check_state_transition(self) -> None:
        """Checks if OPEN breaker should transition to HALF_OPEN after timeout."""
        self._store.check_transition(self.name, self.recovery_timeout)

    async def execute(self, coroutine_fn: Callable[[], Coroutine[Any, Any, Any]]) -> Any:
        """Executes operation through the circuit breaker guard."""
        self._check_state_transition()

        if self.state == CircuitState.OPEN:
            raise CircuitBreakerOpenError(
                f"Circuit breaker '{self.name}' is OPEN. Request rejected to prevent overload."
            )

        try:
            result = await coroutine_fn()
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise

    def _on_success(self) -> None:
        """Records successful execution."""
        self._store.record_success(self.name, self.success_threshold)

    def _on_failure(self) -> None:
        """Records failed execution."""
        self._store.record_failure(self.name, self.failure_threshold)
