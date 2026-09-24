"""
Centralized Telemetry Ingestion Pipeline & Collector.

Buffers, filters, enriches, and dispatches telemetry signals (metrics, logs, traces, profiles, events)
across multi-cloud and multi-region infrastructure.
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any, Dict, List, Optional

from app.infrastructure.observability.telemetry.context import (
    TelemetryContext,
    get_current_context,
    mask_sensitive_data,
)
from app.infrastructure.observability.telemetry.exporters import (
    InMemoryExporter,
    TelemetryBatch,
    TelemetryExporter,
)

logger = logging.getLogger("infrastructure.observability.telemetry.collector")


class TelemetryCollectorPipeline:
    """
    Centralized collector buffering and processing all platform telemetry.
    """

    def __init__(
        self,
        batch_size: int = 100,
        flush_interval_seconds: float = 1.0,
        default_exporter: Optional[TelemetryExporter] = None,
    ) -> None:
        self.batch_size = batch_size
        self.flush_interval_seconds = flush_interval_seconds
        self.exporters: List[TelemetryExporter] = [default_exporter or InMemoryExporter()]
        self._metric_buffer: List[Dict[str, Any]] = []
        self._log_buffer: List[Dict[str, Any]] = []
        self._trace_buffer: List[Dict[str, Any]] = []
        self._profile_buffer: List[Dict[str, Any]] = []
        self._event_buffer: List[Dict[str, Any]] = []
        self._last_flush_time = time.time()

    def add_exporter(self, exporter: TelemetryExporter) -> None:
        self.exporters.append(exporter)

    def _enrich_record(self, data: Dict[str, Any], context: Optional[TelemetryContext] = None) -> Dict[str, Any]:
        ctx = context or get_current_context()
        record = dict(data)
        record["context"] = ctx.model_dump(mode="json")
        if "timestamp" not in record:
            record["timestamp"] = time.time()
        # Apply string masking to any string fields
        for k, v in list(record.items()):
            if isinstance(v, str):
                record[k] = mask_sensitive_data(v)
            elif isinstance(v, dict):
                record[k] = {
                    sub_k: mask_sensitive_data(sub_v) if isinstance(sub_v, str) else sub_v
                    for sub_k, sub_v in v.items()
                }
        return record

    def record_metric(self, metric_data: Dict[str, Any], context: Optional[TelemetryContext] = None) -> None:
        enriched = self._enrich_record(metric_data, context)
        self._metric_buffer.append(enriched)
        self._check_buffer()

    def record_log(self, log_data: Dict[str, Any], context: Optional[TelemetryContext] = None) -> None:
        enriched = self._enrich_record(log_data, context)
        self._log_buffer.append(enriched)
        self._check_buffer()

    def record_trace(self, span_data: Dict[str, Any], context: Optional[TelemetryContext] = None) -> None:
        enriched = self._enrich_record(span_data, context)
        self._trace_buffer.append(enriched)
        self._check_buffer()

    def record_profile(self, profile_data: Dict[str, Any], context: Optional[TelemetryContext] = None) -> None:
        enriched = self._enrich_record(profile_data, context)
        self._profile_buffer.append(enriched)
        self._check_buffer()

    def record_event(self, event_data: Dict[str, Any], context: Optional[TelemetryContext] = None) -> None:
        enriched = self._enrich_record(event_data, context)
        self._event_buffer.append(enriched)
        self._check_buffer()

    def _check_buffer(self) -> None:
        total_items = (
            len(self._metric_buffer)
            + len(self._log_buffer)
            + len(self._trace_buffer)
            + len(self._profile_buffer)
            + len(self._event_buffer)
        )
        if total_items >= self.batch_size or (time.time() - self._last_flush_time) >= self.flush_interval_seconds:
            self.flush()

    def flush(self) -> TelemetryBatch:
        """Flush buffered telemetry to all registered exporters."""
        batch = TelemetryBatch(
            batch_id=f"batch-{uuid.uuid4().hex[:8]}",
            metrics=list(self._metric_buffer),
            logs=list(self._log_buffer),
            traces=list(self._trace_buffer),
            profiles=list(self._profile_buffer),
            events=list(self._event_buffer),
        )

        self._metric_buffer.clear()
        self._log_buffer.clear()
        self._trace_buffer.clear()
        self._profile_buffer.clear()
        self._event_buffer.clear()
        self._last_flush_time = time.time()

        for exp in self.exporters:
            try:
                exp.export_batch(batch)
                exp.flush()
            except Exception:
                pass
        return batch


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

