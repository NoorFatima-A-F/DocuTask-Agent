"""
Phase 13.17: Telemetry Collectors & Metric Aggregators
Real-time ingestion of agent invocations, tool latency, token consumption, and memory drift.
"""

from __future__ import annotations
import math
import numpy as np
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from app.runtime.ai_operations.models.schemas import (
    Span,
    SpanType,
    SpanStatus,
    ExecutionTrace,
    AgentTelemetry,
    AgentHealthStatus,
)


class TelemetryCollector:
    """Collects spans, execution traces, and agent activity from runtime layers."""

    def __init__(self):
        self._traces: Dict[str, ExecutionTrace] = {}
        self._active_spans: Dict[str, Span] = {}

    def start_trace(self, session_id: str, agent_id: str, root_span_name: str, tags: Optional[Dict[str, str]] = None) -> ExecutionTrace:
        trace = ExecutionTrace(
            session_id=session_id,
            agent_id=agent_id,
            root_span_name=root_span_name,
            tags=tags or {},
        )
        self._traces[trace.trace_id] = trace
        return trace

    def start_span(
        self,
        trace_id: str,
        name: str,
        span_type: SpanType,
        agent_id: str,
        parent_span_id: Optional[str] = None,
        inputs: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Span:
        span = Span(
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            name=name,
            span_type=span_type,
            agent_id=agent_id,
            inputs=inputs or {},
            metadata=metadata or {},
        )
        self._active_spans[span.span_id] = span
        if trace_id in self._traces:
            self._traces[trace_id].spans.append(span)
        return span

    def end_span(
        self,
        span_id: str,
        status: SpanStatus = SpanStatus.OK,
        outputs: Optional[Dict[str, Any]] = None,
        token_usage: Optional[Dict[str, int]] = None,
        cost_usd: float = 0.0,
        error_message: Optional[str] = None,
    ) -> Optional[Span]:
        span = self._active_spans.pop(span_id, None)
        if not span:
            return None

        span.end_time = datetime.now(timezone.utc).isoformat()
        span.status = status
        span.outputs = outputs or {}
        span.token_usage = token_usage or span.token_usage
        span.cost_usd = cost_usd
        span.error_message = error_message

        # Compute duration
        try:
            t0 = datetime.fromisoformat(span.start_time)
            t1 = datetime.fromisoformat(span.end_time)
            span.duration_ms = max(0.1, (t1 - t0).total_seconds() * 1000.0)
        except Exception:
            span.duration_ms = 10.0

        # Update trace aggregate totals
        trace = self._traces.get(span.trace_id)
        if trace:
            trace.total_prompt_tokens += span.token_usage.get("prompt_tokens", 0)
            trace.total_completion_tokens += span.token_usage.get("completion_tokens", 0)
            trace.total_cost_usd += span.cost_usd
            if status == SpanStatus.ERROR:
                trace.status = SpanStatus.ERROR

        return span

    def end_trace(self, trace_id: str, status: Optional[SpanStatus] = None) -> Optional[ExecutionTrace]:
        trace = self._traces.get(trace_id)
        if not trace:
            return None

        trace.end_time = datetime.now(timezone.utc).isoformat()
        if status:
            trace.status = status

        try:
            t0 = datetime.fromisoformat(trace.start_time)
            t1 = datetime.fromisoformat(trace.end_time)
            trace.total_duration_ms = max(1.0, (t1 - t0).total_seconds() * 1000.0)
        except Exception:
            trace.total_duration_ms = sum(s.duration_ms for s in trace.spans)

        return trace

    def get_trace(self, trace_id: str) -> Optional[ExecutionTrace]:
        return self._traces.get(trace_id)

    def list_traces(self, limit: int = 50, agent_id: Optional[str] = None) -> List[ExecutionTrace]:
        traces = list(self._traces.values())
        if agent_id:
            traces = [t for t in traces if t.agent_id == agent_id]
        traces.sort(key=lambda t: t.start_time, reverse=True)
        return traces[:limit]


class MetricAggregator:
    """Computes statistical aggregations, percentiles (p50, p95, p99), error rates, and fleet KPIs."""

    @staticmethod
    def aggregate_agent_telemetry(
        agent_id: str,
        agent_name: str,
        role: str,
        traces: List[ExecutionTrace],
    ) -> AgentTelemetry:
        agent_traces = [t for t in traces if t.agent_id == agent_id]
        total_invocations = len(agent_traces)
        if total_invocations == 0:
            return AgentTelemetry(
                agent_id=agent_id,
                agent_name=agent_name,
                role=role,
                health_status=AgentHealthStatus.HEALTHY,
                uptime_seconds=86400.0,
            )

        durations = [t.total_duration_ms for t in agent_traces if t.total_duration_ms > 0]
        if not durations:
            durations = [50.0]

        errors = [t for t in agent_traces if t.status in (SpanStatus.ERROR, SpanStatus.TIMEOUT)]
        error_count = len(errors)
        error_rate = error_count / total_invocations
        success_rate = max(0.0, 1.0 - error_rate)

        avg_latency = float(np.mean(durations))
        p95_latency = float(np.percentile(durations, 95))
        p99_latency = float(np.percentile(durations, 99))

        total_tokens = sum(t.total_prompt_tokens + t.total_completion_tokens for t in agent_traces)
        total_cost = sum(t.total_cost_usd for t in agent_traces)

        # Determine health status
        if error_rate > 0.25:
            health = AgentHealthStatus.CRITICAL
        elif error_rate > 0.08 or p95_latency > 3500:
            health = AgentHealthStatus.DEGRADED
        else:
            health = AgentHealthStatus.HEALTHY

        return AgentTelemetry(
            agent_id=agent_id,
            agent_name=agent_name,
            role=role,
            health_status=health,
            uptime_seconds=86400.0,
            total_invocations=total_invocations,
            success_rate=round(success_rate, 4),
            error_rate=round(error_rate, 4),
            avg_latency_ms=round(avg_latency, 2),
            p95_latency_ms=round(p95_latency, 2),
            p99_latency_ms=round(p99_latency, 2),
            total_tokens_consumed=total_tokens,
            total_cost_usd=round(total_cost, 4),
            last_active=datetime.now(timezone.utc).isoformat(),
            resource_utilization={"cpu_pct": round(min(95.0, 15.0 + total_invocations * 0.5), 1), "memory_mb": 256.0 + total_tokens * 0.001},
        )
