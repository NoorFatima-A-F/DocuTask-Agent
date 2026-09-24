"""
OpenTelemetry and Jaeger-Compatible Trace Correlation Engine for DocuTask Agent.
Builds hierarchical execution DAG trees and calculates critical path latencies from RuntimeEvents.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from app.runtime.events.base import RuntimeEvent


@dataclass
class TraceSpan:
    span_id: str
    trace_id: str
    parent_span_id: Optional[str]
    event_id: str
    event_type: str
    agent_id: Optional[str]
    worker_id: Optional[str]
    timestamp: str
    duration_ms: float
    status: str
    payload: Dict[str, Any]
    children: List[TraceSpan] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "span_id": self.span_id,
            "trace_id": self.trace_id,
            "parent_span_id": self.parent_span_id,
            "event_id": self.event_id,
            "event_type": self.event_type,
            "agent_id": self.agent_id,
            "worker_id": self.worker_id,
            "timestamp": self.timestamp,
            "duration_ms": self.duration_ms,
            "status": self.status,
            "payload": self.payload,
            "children": [c.to_dict() for c in self.children],
        }


@dataclass
class TraceTree:
    trace_id: str
    root_spans: List[TraceSpan]
    total_spans: int
    total_duration_ms: float
    critical_path_ms: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "root_spans": [s.to_dict() for s in self.root_spans],
            "total_spans": self.total_spans,
            "total_duration_ms": self.total_duration_ms,
            "critical_path_ms": self.critical_path_ms,
        }


class TraceCorrelationEngine:
    """
    Constructs hierarchical OpenTelemetry trace DAGs from raw event collections.
    """

    def build_trace_trees(self, events: List[RuntimeEvent]) -> List[TraceTree]:
        if not events:
            return []

        # Group by trace_id
        traces_map: Dict[str, List[RuntimeEvent]] = {}
        for ev in events:
            t_id = ev.trace_id or "default_trace"
            traces_map.setdefault(t_id, []).append(ev)

        result_trees: List[TraceTree] = []

        for trace_id, trace_events in traces_map.items():
            spans_by_id: Dict[str, TraceSpan] = {}
            for ev in trace_events:
                s_id = ev.span_id or ev.event_id
                spans_by_id[s_id] = TraceSpan(
                    span_id=s_id,
                    trace_id=trace_id,
                    parent_span_id=ev.parent_event_id,
                    event_id=ev.event_id,
                    event_type=ev.event_type,
                    agent_id=ev.agent_id,
                    worker_id=ev.worker_id,
                    timestamp=ev.timestamp.isoformat() if hasattr(ev.timestamp, "isoformat") else str(ev.timestamp),
                    duration_ms=float(ev.duration_ms or ev.payload.get("duration_ms", 12.0)),
                    status=ev.status,
                    payload=ev.payload,
                    children=[],
                )

            root_spans: List[TraceSpan] = []
            for s_id, span in spans_by_id.items():
                if span.parent_span_id and span.parent_span_id in spans_by_id:
                    spans_by_id[span.parent_span_id].children.append(span)
                else:
                    root_spans.append(span)

            total_dur = sum(s.duration_ms for s in spans_by_id.values())
            crit_path = max((self._calc_critical_path(s) for s in root_spans), default=0.0)

            result_trees.append(
                TraceTree(
                    trace_id=trace_id,
                    root_spans=root_spans,
                    total_spans=len(spans_by_id),
                    total_duration_ms=round(total_dur, 2),
                    critical_path_ms=round(crit_path, 2),
                )
            )

        return result_trees

    def _calc_critical_path(self, span: TraceSpan) -> float:
        child_max = max((self._calc_critical_path(c) for c in span.children), default=0.0)
        return span.duration_ms + child_max
