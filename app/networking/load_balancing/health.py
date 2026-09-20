"""Active and Passive Health Checking and Outlier Detection."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from ..discovery.registry import EndpointHealth, ServiceEndpoint, ServiceRegistry


@dataclass
class HealthCheckConfig:
    interval_seconds: float = 10.0
    timeout_seconds: float = 2.0
    healthy_threshold: int = 2
    unhealthy_threshold: int = 3
    health_check_path: str = "/health"


@dataclass
class OutlierDetectionTracker:
    consecutive_errors: int = 0
    ejected: bool = False
    ejected_until: float = 0.0


class HealthCheckEngine:
    """Manages active probes and passive outlier ejection for endpoint pools."""

    def __init__(self, registry: Optional[ServiceRegistry] = None):
        self.registry = registry or ServiceRegistry()
        self._outlier_trackers: Dict[str, OutlierDetectionTracker] = {}

    def record_call_result(
        self,
        endpoint_id: str,
        is_error: bool,
        consecutive_error_threshold: int = 3,
        ejection_duration_seconds: float = 30.0,
    ) -> None:
        """Record passive outcome of a live traffic call."""
        tracker = self._outlier_trackers.get(endpoint_id)
        if not tracker:
            tracker = OutlierDetectionTracker()
            self._outlier_trackers[endpoint_id] = tracker

        now = time.time()
        # Check if currently ejected and ejection expired
        if tracker.ejected and now >= tracker.ejected_until:
            tracker.ejected = False
            tracker.consecutive_errors = 0
            self.registry.heartbeat(endpoint_id, EndpointHealth.HEALTHY)

        if is_error:
            tracker.consecutive_errors += 1
            if tracker.consecutive_errors >= consecutive_error_threshold:
                tracker.ejected = True
                tracker.ejected_until = now + ejection_duration_seconds
                self.registry.heartbeat(endpoint_id, EndpointHealth.UNHEALTHY)
        else:
            tracker.consecutive_errors = 0
            if not tracker.ejected:
                self.registry.heartbeat(endpoint_id, EndpointHealth.HEALTHY)

    def is_ejected(self, endpoint_id: str) -> bool:
        tracker = self._outlier_trackers.get(endpoint_id)
        if not tracker:
            return False
        if tracker.ejected and time.time() < tracker.ejected_until:
            return True
        return False

    def run_active_probes(
        self,
        probe_fn: Optional[Callable[[ServiceEndpoint], bool]] = None,
    ) -> Dict[str, bool]:
        """Execute active health check probes against all registered endpoints."""
        endpoints = self.registry.list_endpoints(healthy_only=False)
        results: Dict[str, bool] = {}
        for ep in endpoints:
            is_healthy = probe_fn(ep) if probe_fn else True
            new_health = EndpointHealth.HEALTHY if is_healthy else EndpointHealth.UNHEALTHY
            self.registry.heartbeat(ep.endpoint_id, new_health)
            results[ep.endpoint_id] = is_healthy
        return results
