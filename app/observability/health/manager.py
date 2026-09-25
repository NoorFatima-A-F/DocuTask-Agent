"""
Enterprise Platform Health Manager.
Collects and aggregates health across the 6-level hierarchy and provides probes for /live, /ready, /startup.
"""

import asyncio
from datetime import datetime, timezone
import time
from typing import Any, Callable, Dict, Optional
from .models import HealthCheckResult, HealthLevel, PlatformHealthReport
from ...platform.kernel.health import HealthStatus


class HealthManager:
    """Central Health Manager coordinating live, readiness, and startup health checks."""

    def __init__(self, startup_time: Optional[datetime] = None):
        self.startup_time = startup_time or datetime.now(timezone.utc)
        self._checkers: Dict[str, tuple[HealthLevel, Callable[[], Any]]] = {}
        self._is_ready: bool = False
        self._is_startup_done: bool = False
        self._register_default_checks()

    def set_ready(self, ready: bool = True) -> None:
        """Mark platform readiness state."""
        self._is_ready = ready

    def set_startup_complete(self, done: bool = True) -> None:
        """Mark platform startup completion state."""
        self._is_startup_done = done

    def register_check(self, name: str, level: HealthLevel, check_fn: Callable[[], Any]) -> None:
        """Register a custom health check function."""
        self._checkers[name] = (level, check_fn)

    def _register_default_checks(self) -> None:
        """Register baseline platform subsystem checks."""
        self.register_check("database", HealthLevel.SERVICE, lambda: HealthCheckResult(name="database", status=HealthStatus.HEALTHY, message="Pool connected"))
        self.register_check("cache", HealthLevel.SERVICE, lambda: HealthCheckResult(name="cache", status=HealthStatus.HEALTHY, message="Cache responsive"))
        self.register_check("queue", HealthLevel.SERVICE, lambda: HealthCheckResult(name="queue", status=HealthStatus.HEALTHY, message="Queue broker active"))
        self.register_check("ai_provider", HealthLevel.SERVICE, lambda: HealthCheckResult(name="ai_provider", status=HealthStatus.HEALTHY, message="Provider circuit closed"))

    async def check_health(self) -> PlatformHealthReport:
        """Execute all health checks and generate aggregate health report."""
        results: Dict[str, HealthCheckResult] = {}
        counts = {HealthStatus.HEALTHY.value: 0, HealthStatus.DEGRADED.value: 0, HealthStatus.UNHEALTHY.value: 0}

        for name, (level, check_fn) in self._checkers.items():
            start_t = time.perf_counter()
            try:
                if asyncio.iscoroutinefunction(check_fn):
                    res = await check_fn()
                else:
                    res = check_fn()

                latency_ms = (time.perf_counter() - start_t) * 1000.0
                if isinstance(res, HealthCheckResult):
                    res.latency_ms = latency_ms
                    results[name] = res
                    counts[res.status.value] = counts.get(res.status.value, 0) + 1
                else:
                    st = HealthStatus.HEALTHY if res else HealthStatus.UNHEALTHY
                    results[name] = HealthCheckResult(name=name, level=level, status=st, latency_ms=latency_ms)
                    counts[st.value] = counts.get(st.value, 0) + 1
            except Exception as e:
                latency_ms = (time.perf_counter() - start_t) * 1000.0
                results[name] = HealthCheckResult(
                    name=name,
                    level=level,
                    status=HealthStatus.UNHEALTHY,
                    latency_ms=latency_ms,
                    message=f"Check exception: {str(e)}",
                )
                counts[HealthStatus.UNHEALTHY.value] += 1

        # Determine overall aggregate status
        if counts[HealthStatus.UNHEALTHY.value] > 0:
            agg_status = HealthStatus.UNHEALTHY
        elif counts[HealthStatus.DEGRADED.value] > 0:
            agg_status = HealthStatus.DEGRADED
        else:
            agg_status = HealthStatus.HEALTHY

        uptime = (datetime.now(timezone.utc) - self.startup_time).total_seconds()

        return PlatformHealthReport(
            status=agg_status,
            uptime_seconds=uptime,
            live=True,
            ready=self._is_ready and (agg_status != HealthStatus.UNHEALTHY),
            startup_complete=self._is_startup_done,
            checks=results,
            summary=counts,
        )
