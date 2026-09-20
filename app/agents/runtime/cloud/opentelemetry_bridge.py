"""
OpenTelemetry Distributed Tracing Bridge & SLO Metric Collector for AAOS.
Provides distributed span context propagation, latency histograms, token/cost tracking,
and real-time SLO error budget burn rate calculators.
"""

from __future__ import annotations

import asyncio
import logging
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class SpanKind(str, Enum):
    INTERNAL = "INTERNAL"
    SERVER = "SERVER"
    CLIENT = "CLIENT"
    PRODUCER = "PRODUCER"
    CONSUMER = "CONSUMER"


@dataclass
class TelemetrySpan:
    """Represents an OpenTelemetry-compatible tracing span."""

    name: str
    trace_id: str
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    parent_span_id: Optional[str] = None
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    kind: SpanKind = SpanKind.INTERNAL
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "UNSET"  # OK, ERROR, UNSET

    def finish(self, status: str = "OK") -> None:
        self.end_time = time.time()
        self.status = status

    def duration_ms(self) -> float:
        end = self.end_time or time.time()
        return (end - self.start_time) * 1000.0


@dataclass
class SLOMetricSnapshot:
    """Snapshot of system Service Level Objectives and error budget."""

    target_availability_pct: float = 99.9
    current_availability_pct: float = 100.0
    total_requests: int = 0
    failed_requests: int = 0
    error_budget_remaining_pct: float = 100.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0


class OpenTelemetryBridge:
    """
    OpenTelemetry Bridge for AAOS.
    Manages active distributed spans, records metrics, and tracks error budgets.
    """

    def __init__(self, service_name: str = "aaos-cognitive-runtime") -> None:
        self.service_name = service_name
        self.active_spans: Dict[str, TelemetrySpan] = {}
        self.finished_spans: List[TelemetrySpan] = []
        self._latencies: List[float] = []
        self.total_requests: int = 0
        self.failed_requests: int = 0

    def start_span(
        self,
        name: str,
        trace_id: Optional[str] = None,
        parent_span_id: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> TelemetrySpan:
        """Starts and registers a new tracing span."""
        t_id = trace_id or uuid.uuid4().hex
        span = TelemetrySpan(
            name=name,
            trace_id=t_id,
            parent_span_id=parent_span_id,
            attributes=attributes or {},
        )
        self.active_spans[span.span_id] = span
        self.total_requests += 1
        return span

    def end_span(self, span: TelemetrySpan, status: str = "OK", error: Optional[Exception] = None) -> None:
        """Finishes an active span and calculates metrics."""
        if error:
            span.status = "ERROR"
            span.attributes["error.type"] = type(error).__name__
            span.attributes["error.message"] = str(error)
            self.failed_requests += 1
        else:
            span.status = status

        span.finish(span.status)
        if span.span_id in self.active_spans:
            del self.active_spans[span.span_id]
        self.finished_spans.append(span)
        self._latencies.append(span.duration_ms())

    def get_slo_snapshot(self) -> SLOMetricSnapshot:
        """Computes current SLO compliance, p95/p99 latencies, and error budget."""
        if not self.total_requests:
            return SLOMetricSnapshot()

        avail = max(0.0, 100.0 * (1.0 - (self.failed_requests / self.total_requests)))
        allowed_failures = max(1.0, self.total_requests * 0.001)  # for 99.9% SLO
        remaining_budget = max(0.0, 100.0 * (1.0 - (self.failed_requests / allowed_failures)))

        sorted_lat = sorted(self._latencies) if self._latencies else [0.0]
        p95_idx = int(len(sorted_lat) * 0.95)
        p99_idx = int(len(sorted_lat) * 0.99)

        return SLOMetricSnapshot(
            target_availability_pct=99.9,
            current_availability_pct=round(avail, 3),
            total_requests=self.total_requests,
            failed_requests=self.failed_requests,
            error_budget_remaining_pct=round(remaining_budget, 2),
            p95_latency_ms=round(sorted_lat[min(p95_idx, len(sorted_lat) - 1)], 2),
            p99_latency_ms=round(sorted_lat[min(p99_idx, len(sorted_lat) - 1)], 2),
        )
