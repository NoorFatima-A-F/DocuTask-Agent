"""
OpenTelemetry Telemetry and Distributed Tracing Adapter.
"""
from typing import Dict, Optional

class TelemetryAdapter:
    def __init__(self, service_name: str = "verification-platform"):
        self.service_name = service_name
        self._metrics: Dict[str, float] = {}

    def record_counter(self, name: str, value: float = 1.0, tags: Optional[Dict[str, str]] = None) -> None:
        self._metrics[name] = self._metrics.get(name, 0.0) + value

    def record_gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        self._metrics[name] = value

    def get_metrics(self) -> Dict[str, float]:
        return dict(self._metrics)
