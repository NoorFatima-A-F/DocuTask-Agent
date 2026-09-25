"""
Health Probes & Probe Registry.

Defines 6 probe categories (STARTUP, READINESS, LIVENESS, DEPENDENCY, RESOURCE, BUSINESS),
probe lifecycle execution, timeouts, thresholds, and registry management.
"""

from __future__ import annotations

import asyncio
import enum
import logging
import time
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Union
from pydantic import BaseModel, Field

logger = logging.getLogger("infrastructure.health.probes")


class ProbeType(str, enum.Enum):
    """Six enterprise probe classifications."""
    STARTUP = "STARTUP"
    READINESS = "READINESS"
    LIVENESS = "LIVENESS"
    DEPENDENCY = "DEPENDENCY"
    RESOURCE = "RESOURCE"
    BUSINESS = "BUSINESS"


class ProbeStatus(str, enum.Enum):
    """Probe execution evaluation status."""
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


class ProbeResult(BaseModel):
    """Detailed result of a single probe evaluation."""
    probe_id: str
    component_id: str
    probe_type: ProbeType
    status: ProbeStatus
    latency_ms: float
    message: str = ""
    error: Optional[str] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)
    executed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class HealthProbe(BaseModel):
    """Configurable health probe definition."""
    probe_id: str
    component_id: str
    probe_type: ProbeType
    interval_seconds: float = Field(default=10.0, ge=0.5)
    timeout_seconds: float = Field(default=3.0, ge=0.1)
    consecutive_success_threshold: int = Field(default=1, ge=1)
    consecutive_failure_threshold: int = Field(default=3, ge=1)
    enabled: bool = Field(default=True)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProbeRegistry:
    """
    Registry managing probe definitions, registered execution handlers,
    and historic probe outcomes.
    """

    def __init__(self) -> None:
        self._probes: Dict[str, HealthProbe] = {}
        self._handlers: Dict[str, Callable[[], Union[ProbeResult, bool, Dict[str, Any]]]] = {}
        self._async_handlers: Dict[str, Callable[[], Any]] = {}
        self._history: Dict[str, List[ProbeResult]] = {}
        self._consecutive_successes: Dict[str, int] = {}
        self._consecutive_failures: Dict[str, int] = {}
        self._current_status: Dict[str, ProbeStatus] = {}

    def register_probe(
        self,
        probe: HealthProbe,
        handler: Optional[Callable[[], Union[ProbeResult, bool, Dict[str, Any]]]] = None,
        async_handler: Optional[Callable[[], Any]] = None,
    ) -> None:
        """Register a probe with an optional sync or async execution handler."""
        self._probes[probe.probe_id] = probe
        if handler:
            self._handlers[probe.probe_id] = handler
        if async_handler:
            self._async_handlers[probe.probe_id] = async_handler
        if probe.probe_id not in self._history:
            self._history[probe.probe_id] = []
            self._consecutive_successes[probe.probe_id] = 0
            self._consecutive_failures[probe.probe_id] = 0
            self._current_status[probe.probe_id] = ProbeStatus.UNKNOWN

    def get_probe(self, probe_id: str) -> Optional[HealthProbe]:
        return self._probes.get(probe_id)

    def list_probes_for_component(self, component_id: str) -> List[HealthProbe]:
        return [p for p in self._probes.values() if p.component_id == component_id]

    def get_probe_status(self, probe_id: str) -> ProbeStatus:
        return self._current_status.get(probe_id, ProbeStatus.UNKNOWN)

    def get_probe_history(self, probe_id: str, limit: int = 50) -> List[ProbeResult]:
        return self._history.get(probe_id, [])[-limit:]

    def record_result(self, result: ProbeResult) -> ProbeStatus:
        """Record outcome and calculate consolidated probe status."""
        probe = self._probes.get(result.probe_id)
        if not probe:
            return result.status

        hist = self._history.setdefault(result.probe_id, [])
        hist.append(result)
        if len(hist) > 200:
            hist.pop(0)

        if result.status == ProbeStatus.HEALTHY:
            self._consecutive_successes[result.probe_id] += 1
            self._consecutive_failures[result.probe_id] = 0
            if self._consecutive_successes[result.probe_id] >= probe.consecutive_success_threshold:
                self._current_status[result.probe_id] = ProbeStatus.HEALTHY
        elif result.status == ProbeStatus.DEGRADED:
            self._consecutive_successes[result.probe_id] = 0
            self._current_status[result.probe_id] = ProbeStatus.DEGRADED
        else:  # UNHEALTHY or error
            self._consecutive_failures[result.probe_id] += 1
            self._consecutive_successes[result.probe_id] = 0
            if self._consecutive_failures[result.probe_id] >= probe.consecutive_failure_threshold:
                self._current_status[result.probe_id] = ProbeStatus.UNHEALTHY

        return self._current_status[result.probe_id]

    def execute_probe_sync(self, probe_id: str) -> ProbeResult:
        """Synchronously execute a registered probe."""
        probe = self._probes.get(probe_id)
        if not probe:
            raise KeyError(f"Probe '{probe_id}' not found.")

        handler = self._handlers.get(probe_id)
        start = time.perf_counter()

        if not handler:
            # Default healthy if no handler attached
            result = ProbeResult(
                probe_id=probe_id,
                component_id=probe.component_id,
                probe_type=probe.probe_type,
                status=ProbeStatus.HEALTHY,
                latency_ms=(time.perf_counter() - start) * 1000,
                message="No custom handler registered; default check passed.",
            )
        else:
            try:
                res = handler()
                latency = (time.perf_counter() - start) * 1000
                if isinstance(res, ProbeResult):
                    result = res
                elif isinstance(res, bool):
                    result = ProbeResult(
                        probe_id=probe_id,
                        component_id=probe.component_id,
                        probe_type=probe.probe_type,
                        status=ProbeStatus.HEALTHY if res else ProbeStatus.UNHEALTHY,
                        latency_ms=latency,
                        message="Boolean handler check",
                    )
                elif isinstance(res, dict):
                    status_str = res.get("status", "HEALTHY").upper()
                    status = getattr(ProbeStatus, status_str, ProbeStatus.HEALTHY)
                    result = ProbeResult(
                        probe_id=probe_id,
                        component_id=probe.component_id,
                        probe_type=probe.probe_type,
                        status=status,
                        latency_ms=latency,
                        message=res.get("message", ""),
                        metrics=res.get("metrics", {}),
                    )
                else:
                    result = ProbeResult(
                        probe_id=probe_id,
                        component_id=probe.component_id,
                        probe_type=probe.probe_type,
                        status=ProbeStatus.HEALTHY,
                        latency_ms=latency,
                        message=str(res),
                    )
            except Exception as e:
                latency = (time.perf_counter() - start) * 1000
                result = ProbeResult(
                    probe_id=probe_id,
                    component_id=probe.component_id,
                    probe_type=probe.probe_type,
                    status=ProbeStatus.UNHEALTHY,
                    latency_ms=latency,
                    message="Probe execution threw exception",
                    error=str(e),
                )

        self.record_result(result)
        return result

    async def execute_probe_async(self, probe_id: str) -> ProbeResult:
        """Asynchronously execute a registered probe."""
        probe = self._probes.get(probe_id)
        if not probe:
            raise KeyError(f"Probe '{probe_id}' not found.")

        async_handler = self._async_handlers.get(probe_id)
        if async_handler:
            start = time.perf_counter()
            try:
                coro = async_handler() if callable(async_handler) else async_handler
                res = await asyncio.wait_for(coro, timeout=probe.timeout_seconds)
                latency = (time.perf_counter() - start) * 1000
                if isinstance(res, ProbeResult):
                    result = res
                elif isinstance(res, bool):
                    result = ProbeResult(
                        probe_id=probe_id,
                        component_id=probe.component_id,
                        probe_type=probe.probe_type,
                        status=ProbeStatus.HEALTHY if res else ProbeStatus.UNHEALTHY,
                        latency_ms=latency,
                    )
                elif isinstance(res, dict):
                    status_str = res.get("status", "HEALTHY").upper()
                    status = getattr(ProbeStatus, status_str, ProbeStatus.HEALTHY)
                    result = ProbeResult(
                        probe_id=probe_id,
                        component_id=probe.component_id,
                        probe_type=probe.probe_type,
                        status=status,
                        latency_ms=latency,
                        message=res.get("message", ""),
                        metrics=res.get("metrics", {}),
                    )
                else:
                    result = ProbeResult(
                        probe_id=probe_id,
                        component_id=probe.component_id,
                        probe_type=probe.probe_type,
                        status=ProbeStatus.HEALTHY,
                        latency_ms=latency,
                        message=str(res),
                    )
            except Exception as e:
                latency = (time.perf_counter() - start) * 1000
                result = ProbeResult(
                    probe_id=probe_id,
                    component_id=probe.component_id,
                    probe_type=probe.probe_type,
                    status=ProbeStatus.UNHEALTHY,
                    latency_ms=latency,
                    error=str(e),
                )
            self.record_result(result)
            return result
        else:
            return self.execute_probe_sync(probe_id)
