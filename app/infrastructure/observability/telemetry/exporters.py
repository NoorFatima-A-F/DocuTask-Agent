"""
Telemetry Exporters.

Provides multi-target exporters (In-Memory, OTLP JSON, File Stream, Alert Forwarding)
for processing and distributing metrics, logs, traces, profiles, and events.
"""

from __future__ import annotations

import abc
import json
import logging
from typing import Any, Dict, List
from pydantic import BaseModel

logger = logging.getLogger("infrastructure.observability.telemetry.exporters")


class TelemetryBatch(BaseModel):
    """Container for batch telemetry export."""
    batch_id: str
    metrics: List[Dict[str, Any]] = []
    logs: List[Dict[str, Any]] = []
    traces: List[Dict[str, Any]] = []
    profiles: List[Dict[str, Any]] = []
    events: List[Dict[str, Any]] = []


class TelemetryExporter(abc.ABC):
    """Abstract base class for telemetry exporters."""

    @abc.abstractmethod
    def export_batch(self, batch: TelemetryBatch) -> bool:
        """Export a batch of telemetry records."""
        raise NotImplementedError

    @abc.abstractmethod
    def flush(self) -> None:
        """Flush any pending buffered data."""
        pass


class InMemoryExporter(TelemetryExporter):
    """In-memory telemetry store for real-time querying, testing, and inspection."""

    def __init__(self, max_items_per_category: int = 5000) -> None:
        self.max_items_per_category = max_items_per_category
        self.metrics: List[Dict[str, Any]] = []
        self.logs: List[Dict[str, Any]] = []
        self.traces: List[Dict[str, Any]] = []
        self.profiles: List[Dict[str, Any]] = []
        self.events: List[Dict[str, Any]] = []

    def export_batch(self, batch: TelemetryBatch) -> bool:
        self.metrics.extend(batch.metrics)
        self.logs.extend(batch.logs)
        self.traces.extend(batch.traces)
        self.profiles.extend(batch.profiles)
        self.events.extend(batch.events)

        # Trim buffers
        if len(self.metrics) > self.max_items_per_category:
            self.metrics = self.metrics[-self.max_items_per_category:]
        if len(self.logs) > self.max_items_per_category:
            self.logs = self.logs[-self.max_items_per_category:]
        if len(self.traces) > self.max_items_per_category:
            self.traces = self.traces[-self.max_items_per_category:]
        if len(self.profiles) > self.max_items_per_category:
            self.profiles = self.profiles[-self.max_items_per_category:]
        if len(self.events) > self.max_items_per_category:
            self.events = self.events[-self.max_items_per_category:]

        return True

    def flush(self) -> None:
        pass

    def clear(self) -> None:
        self.metrics.clear()
        self.logs.clear()
        self.traces.clear()
        self.profiles.clear()
        self.events.clear()


class OTLPJsonExporter(TelemetryExporter):
    """Exports telemetry formatted according to OpenTelemetry standard JSON schemas."""

    def __init__(self) -> None:
        self.exported_payloads: List[str] = []

    def export_batch(self, batch: TelemetryBatch) -> bool:
        otlp_doc = {
            "resourceMetrics": [{"scopeMetrics": [{"metrics": batch.metrics}]}],
            "resourceLogs": [{"scopeLogs": [{"logRecords": batch.logs}]}],
            "resourceSpans": [{"scopeSpans": [{"spans": batch.traces}]}],
        }
        serialized = json.dumps(otlp_doc, default=str)
        self.exported_payloads.append(serialized)
        return True

    def flush(self) -> None:
        pass
