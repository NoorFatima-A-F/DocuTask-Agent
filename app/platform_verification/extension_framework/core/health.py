"""
Plugin Health & Telemetry Monitor.
Tracks error rates, latency histograms, and availability states.
"""
from typing import Dict, List, Optional
from datetime import datetime, timezone
import numpy as np
from app.platform_verification.extension_framework.domain.models import (
    PluginHealthMetrics, PluginHealthState
)


class PluginHealthMonitor:
    def __init__(self):
        self._metrics: Dict[str, PluginHealthMetrics] = {}
        self._latency_samples: Dict[str, List[float]] = {}

    def get_health(self, plugin_id: str) -> PluginHealthMetrics:
        if plugin_id not in self._metrics:
            self._metrics[plugin_id] = PluginHealthMetrics(plugin_id=plugin_id)
            self._latency_samples[plugin_id] = []
        return self._metrics[plugin_id]

    def record_execution(
        self,
        plugin_id: str,
        is_success: bool,
        latency_ms: float,
        error: Optional[str] = None
    ) -> PluginHealthMetrics:
        health = self.get_health(plugin_id)
        health.total_executions += 1
        if is_success:
            health.successful_executions += 1
        else:
            health.failed_executions += 1
            health.last_error = error

        health.success_rate = round(health.successful_executions / health.total_executions, 4)

        samples = self._latency_samples[plugin_id]
        samples.append(latency_ms)
        if len(samples) > 1000:
            samples.pop(0)

        health.avg_latency_ms = round(float(np.mean(samples)), 2)
        health.p95_latency_ms = round(float(np.percentile(samples, 95)), 2) if len(samples) > 1 else latency_ms
        health.p99_latency_ms = round(float(np.percentile(samples, 99)), 2) if len(samples) > 1 else latency_ms
        health.last_health_check = datetime.now(timezone.utc).isoformat()

        # Update health state based on error rate
        if health.total_executions >= 5:
            if health.success_rate < 0.70:
                health.state = PluginHealthState.UNHEALTHY
            elif health.success_rate < 0.95 or health.p95_latency_ms > 5000:
                health.state = PluginHealthState.DEGRADED
            else:
                health.state = PluginHealthState.HEALTHY

        return health

    def list_all_health(self) -> List[PluginHealthMetrics]:
        return list(self._metrics.values())


plugin_health_monitor = PluginHealthMonitor()
