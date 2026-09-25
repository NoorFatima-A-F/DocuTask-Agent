"""
Telemetry Collector and Metrics Exporter Interface.
Captures verification duration, throughput, and error metrics for Prometheus / OpenTelemetry export.
"""
from typing import Dict, Any

class TelemetryCollector:
    """In-memory telemetry accumulator for verification workloads."""
    def __init__(self):
        self._metrics: Dict[str, float] = {}
        self._counters: Dict[str, int] = {}

    def increment(self, metric_name: str, count: int = 1) -> None:
        self._counters[metric_name] = self._counters.get(metric_name, 0) + count

    def gauge(self, metric_name: str, value: float) -> None:
        self._metrics[metric_name] = value

    def get_snapshot(self) -> Dict[str, Any]:
        return {
            "metrics": dict(self._metrics),
            "counters": dict(self._counters)
        }
