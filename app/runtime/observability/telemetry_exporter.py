"""
Telemetry Exporter (Prometheus & OpenTelemetry Compatible).

Formats runtime metrics into standard Prometheus exposition format and OpenTelemetry OTLP JSON.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List
from app.runtime.observability.metrics_registry import MetricsRegistry


class TelemetryExporter:
    """Exports runtime metrics in industry-standard formats."""

    @staticmethod
    def to_prometheus_format(registry: MetricsRegistry) -> str:
        """Formats all registered metrics into Prometheus text format."""
        metrics_dict = registry.get_all_metrics_dict()
        lines = [
            "# HELP docutask_runtime_metrics Real-time execution metrics for DocuTask Agent",
            "# TYPE docutask_runtime_metrics gauge",
        ]
        for name, val in sorted(metrics_dict.items()):
            sanitized_name = name.replace(".", "_").replace("-", "_")
            lines.append(f"docutask_{sanitized_name} {val}")
        return "\n".join(lines) + "\n"

    @staticmethod
    def to_otlp_json(registry: MetricsRegistry) -> Dict[str, Any]:
        """Formats metrics into simplified OpenTelemetry JSON structure."""
        metrics_dict = registry.get_all_metrics_dict()
        now_ns = time.time_ns()
        data_points = []
        for name, val in metrics_dict.items():
            data_points.append({
                "name": f"docutask.{name}",
                "time_unix_nano": now_ns,
                "as_double": float(val),
            })
        return {
            "resource_metrics": [
                {
                    "resource": {
                        "attributes": [{"key": "service.name", "value": {"string_value": "docutask-agent-runtime"}}]
                    },
                    "scope_metrics": [{"metrics": data_points}],
                }
            ]
        }
