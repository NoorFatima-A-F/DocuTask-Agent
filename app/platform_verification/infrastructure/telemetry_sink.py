"""
Structured Telemetry & OpenTelemetry-Compatible Metric Sink
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class TelemetrySink:
    def __init__(self):
        self._metrics_stream: List[Dict[str, Any]] = []

    def record_gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        self._metrics_stream.append({
            "name": name,
            "type": "GAUGE",
            "value": value,
            "tags": tags or {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    def get_stream(self) -> List[Dict[str, Any]]:
        return list(self._metrics_stream)

telemetry_sink = TelemetrySink()
