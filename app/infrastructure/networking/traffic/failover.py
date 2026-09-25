"""Traffic Failover Manager, Outlier Detection, and Circuit Breakers."""

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Dict, Optional
import threading

from ..control_plane.registry import NetworkEndpoint


class CircuitState(str, Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, fast reject
    HALF_OPEN = "half_open"  # Testing recovery


@dataclass
class CircuitBreakerConfig:
    """Circuit breaker thresholds."""
    consecutive_errors_threshold: int = 5
    recovery_time_seconds: float = 15.0
    half_open_success_threshold: int = 2


class TrafficFailoverManager:
    """Monitors endpoint error rates, triggers circuit breakers, and manages cross-region failover."""

    def __init__(self, config: Optional[CircuitBreakerConfig] = None) -> None:
        self.config = config or CircuitBreakerConfig()
        self._circuits: Dict[str, CircuitState] = {}  # endpoint_address -> CircuitState
        self._consecutive_errors: Dict[str, int] = {}
        self._consecutive_successes: Dict[str, int] = {}
        self._opened_at: Dict[str, datetime] = {}
        self._lock = threading.RLock()

    def get_circuit_state(self, endpoint: NetworkEndpoint) -> CircuitState:
        """Get current circuit breaker state for an endpoint."""
        addr = endpoint.address
        with self._lock:
            state = self._circuits.get(addr, CircuitState.CLOSED)
            if state == CircuitState.OPEN:
                opened_time = self._opened_at.get(addr)
                if opened_time and datetime.now(timezone.utc) - opened_time > timedelta(seconds=self.config.recovery_time_seconds):
                    self._circuits[addr] = CircuitState.HALF_OPEN
                    return CircuitState.HALF_OPEN
            return state

    def record_success(self, endpoint: NetworkEndpoint) -> None:
        """Record successful call to endpoint."""
        addr = endpoint.address
        with self._lock:
            self._consecutive_errors[addr] = 0
            state = self._circuits.get(addr, CircuitState.CLOSED)

            if state == CircuitState.HALF_OPEN:
                succ = self._consecutive_successes.get(addr, 0) + 1
                self._consecutive_successes[addr] = succ
                if succ >= self.config.half_open_success_threshold:
                    self._circuits[addr] = CircuitState.CLOSED
                    self._consecutive_successes[addr] = 0
                    endpoint.healthy = True

    def record_failure(self, endpoint: NetworkEndpoint) -> None:
        """Record failed call to endpoint."""
        addr = endpoint.address
        with self._lock:
            self._consecutive_successes[addr] = 0
            errs = self._consecutive_errors.get(addr, 0) + 1
            self._consecutive_errors[addr] = errs

            state = self._circuits.get(addr, CircuitState.CLOSED)
            if state == CircuitState.HALF_OPEN or errs >= self.config.consecutive_errors_threshold:
                self._circuits[addr] = CircuitState.OPEN
                self._opened_at[addr] = datetime.now(timezone.utc)
                endpoint.healthy = False

    def can_execute(self, endpoint: NetworkEndpoint) -> bool:
        """Check if request to endpoint is permitted by circuit breaker."""
        state = self.get_circuit_state(endpoint)
        return state in (CircuitState.CLOSED, CircuitState.HALF_OPEN)
