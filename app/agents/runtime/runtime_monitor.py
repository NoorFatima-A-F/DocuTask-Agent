"""
Runtime Monitor.
Implements IHealthMonitor; collects live health checks from registered probes and generates aggregate reports.
"""

import time
from typing import Any, Callable, Coroutine, Dict, List
from app.agents.runtime.interfaces import IHealthMonitor
from app.agents.runtime.runtime_health import (
    PlatformHealthReport,
    SubsystemHealthReport,
    SubsystemHealthStatus,
)


class RuntimeMonitor(IHealthMonitor):
    """Monitors live health and responsiveness of platform subsystems."""

    def __init__(self) -> None:
        self._probes: Dict[str, Callable[[], Coroutine[Any, Any, Dict[str, Any]]]] = {}

    def register_probe(
        self,
        subsystem_name: str,
        probe_fn: Callable[[], Coroutine[Any, Any, Dict[str, Any]]],
    ) -> None:
        """Registers an asynchronous health probe for a subsystem."""
        self._probes[subsystem_name] = probe_fn

    async def check_health(self) -> PlatformHealthReport:
        """Executes all registered health probes and returns an aggregated platform health report."""
        reports: List[SubsystemHealthReport] = []

        for name, probe in self._probes.items():
            start_time = time.perf_counter()
            try:
                details = await probe()
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                status = SubsystemHealthStatus(details.get("status", "HEALTHY"))
                reports.append(
                    SubsystemHealthReport(
                        subsystem_name=name,
                        status=status,
                        latency_ms=elapsed_ms,
                        details=details,
                    )
                )
            except Exception as ex:
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                reports.append(
                    SubsystemHealthReport(
                        subsystem_name=name,
                        status=SubsystemHealthStatus.UNHEALTHY,
                        latency_ms=elapsed_ms,
                        details={"error": str(ex)},
                    )
                )

        if not reports:
            # Default healthy state if no probes explicitly registered
            reports.append(
                SubsystemHealthReport(
                    subsystem_name="Kernel",
                    status=SubsystemHealthStatus.HEALTHY,
                    latency_ms=0.1,
                    details={"status": "UP"},
                )
            )

        return PlatformHealthReport.aggregate(reports)
