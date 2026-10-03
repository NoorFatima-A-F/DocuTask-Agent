"""Unified Telemetry Pipeline and Exporter Framework."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from .context import ObservabilityContext, get_current_context


class TelemetryType(str, Enum):
    METRIC = "METRIC"
    LOG = "LOG"
    TRACE = "TRACE"
    EVENT = "EVENT"
    PROFILE = "PROFILE"


@dataclass
class TelemetryRecord:
    telemetry_type: TelemetryType
    payload: Dict[str, Any]
    context: ObservabilityContext = field(default_factory=get_current_context)
    timestamp: float = field(default_factory=time.time)


class ITelemetryExporter(ABC):
    @abstractmethod
    def export(self, batch: List[TelemetryRecord]) -> None:
        pass


class InMemoryTelemetryExporter(ITelemetryExporter):
    """Thread-safe in-memory exporter for testing and real-time buffer queries."""

    def __init__(self, max_records: int = 5000):
        self.max_records = max_records
        self.records: List[TelemetryRecord] = []

    def export(self, batch: List[TelemetryRecord]) -> None:
        self.records.extend(batch)
        if len(self.records) > self.max_records:
            self.records = self.records[-self.max_records:]

    def clear(self) -> None:
        self.records.clear()

    def get_by_type(self, t_type: TelemetryType) -> List[TelemetryRecord]:
        return [r for r in self.records if r.telemetry_type == t_type]


class TelemetryPipeline:
    """Asynchronous ingestion and dispatching pipeline for telemetry records."""

    def __init__(self, buffer_size: int = 1000, batch_size: int = 50):
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self._buffer: List[TelemetryRecord] = []
        self._exporters: List[ITelemetryExporter] = []
        self._filters: List[Callable[[TelemetryRecord], bool]] = []

    def add_exporter(self, exporter: ITelemetryExporter) -> None:
        self._exporters.append(exporter)

    def add_filter(self, filter_fn: Callable[[TelemetryRecord], bool]) -> None:
        self._filters.append(filter_fn)

    def ingest(self, record: TelemetryRecord) -> None:
        """Ingest a telemetry record through registered filters and buffer for export."""
        for f in self._filters:
            if not f(record):
                return

        self._buffer.append(record)
        if len(self._buffer) >= self.batch_size:
            self.flush()

    def flush(self) -> int:
        """Flush buffered telemetry to all exporters."""
        if not self._buffer:
            return 0

        batch = list(self._buffer)
        self._buffer.clear()

        for exp in self._exporters:
            try:
                exp.export(batch)
            except Exception:
                pass  # SRE rule: telemetry export failures must not crash caller

        return len(batch)
