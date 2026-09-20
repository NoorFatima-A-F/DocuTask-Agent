"""
Cloud Telemetry Exporter for Enterprise Agent Operating System.
Provides structured JSON logging, OpenTelemetry span formatting, and Prometheus metrics exporting.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class StructuredLogEntry:
    """Structured JSON log compliant with Google Cloud Logging / FluentBit."""

    severity: str
    message: str
    component: str
    execution_id: str = ""
    agent_id: str = ""
    trace_id: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        data = {
            "severity": self.severity,
            "message": self.message,
            "component": self.component,
            "execution_id": self.execution_id,
            "agent_id": self.agent_id,
            "trace_id": self.trace_id,
            "timestamp": self.timestamp.isoformat(),
            "attributes": self.attributes,
        }
        return json.dumps(data)


class CloudTelemetryExporter:
    """Exports Prometheus-compatible metrics and structured traces."""

    def __init__(self) -> None:
        self._counters: Dict[str, int] = {}
        self._gauges: Dict[str, float] = {}

    def increment_counter(self, name: str, value: int = 1) -> None:
        self._counters[name] = self._counters.get(name, 0) + value

    def set_gauge(self, name: str, value: float) -> None:
        self._gauges[name] = value

    def export_prometheus_metrics(self) -> str:
        """Generates OpenMetrics / Prometheus text output."""
        lines = []
        for name, count in sorted(self._counters.items()):
            lines.append(f"# TYPE {name} counter")
            lines.append(f"{name} {count}")

        for name, val in sorted(self._gauges.items()):
            lines.append(f"# TYPE {name} gauge")
            lines.append(f"{name} {val:.4f}")

        return "\n".join(lines)
