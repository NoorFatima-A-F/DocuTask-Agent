"""
Trace Tree Analyzer & Critical Path Calculator.

Reconstructs hierarchical span trees from raw trace spans, calculates critical execution paths,
and pinpoints latency bottlenecks across microservices.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.observability.tracing.models import Span, SpanStatus

logger = logging.getLogger("infrastructure.observability.tracing.spans")


class SpanTreeNode(BaseModel):
    """Hierarchical node in a distributed trace tree."""
    span: Span
    children: List[SpanTreeNode] = Field(default_factory=list)
    depth: int = 0
    exclusive_duration_ms: float = 0.0


class TraceAnalysisReport(BaseModel):
    """Comprehensive analysis report for a distributed trace."""
    trace_id: str
    root_service: str
    total_duration_ms: float
    total_spans: int
    error_count: int
    services_involved: List[str]
    critical_path: List[str]  # List of operation names on the critical path
    root_node: Optional[SpanTreeNode] = None


class TraceTreeAnalyzer:
    """
    Builds trace trees, computes exclusive execution times, and finds critical latency bottlenecks.
    """

    @classmethod
    def build_tree(cls, spans: List[Span]) -> Optional[SpanTreeNode]:
        """Reconstruct span tree from unordered spans."""
        if not spans:
            return None

        span_map: Dict[str, Span] = {s.span_id: s for s in spans}
        children_map: Dict[Optional[str], List[Span]] = {}

        for s in spans:
            children_map.setdefault(s.parent_span_id, []).append(s)

        # Identify root span (parent_span_id is None or not in span_map)
        root_candidates = [s for s in spans if not s.parent_span_id or s.parent_span_id not in span_map]
        root_span = root_candidates[0] if root_candidates else spans[0]

        def _build_node(span: Span, depth: int) -> SpanTreeNode:
            node = SpanTreeNode(span=span, depth=depth)
            child_spans = children_map.get(span.span_id, [])
            # Sort children by start time
            child_spans.sort(key=lambda x: x.start_time)

            child_duration_sum = 0.0
            for child in child_spans:
                child_node = _build_node(child, depth + 1)
                node.children.append(child_node)
                if child.duration_ms:
                    child_duration_sum += child.duration_ms

            span_dur = span.duration_ms or 0.0
            node.exclusive_duration_ms = max(0.0, span_dur - child_duration_sum)
            return node

        return _build_node(root_span, 0)

    @classmethod
    def analyze_trace(cls, spans: List[Span]) -> Optional[TraceAnalysisReport]:
        """Perform end-to-end trace tree and critical path analysis."""
        if not spans:
            return None

        tree = cls.build_tree(spans)
        if not tree:
            return None

        trace_id = spans[0].trace_id
        root_service = tree.span.service_name
        total_duration = max((s.duration_ms or 0.0) for s in spans)
        error_count = sum(1 for s in spans if s.status == SpanStatus.ERROR)
        services = sorted(list({s.service_name for s in spans}))

        # Find critical path (longest sequential chain of children)
        critical_path: List[str] = []

        def _trace_critical(node: SpanTreeNode) -> None:
            critical_path.append(f"{node.span.service_name}:{node.span.operation_name}")
            if node.children:
                # Pick child with highest duration
                longest_child = max(node.children, key=lambda c: c.span.duration_ms or 0.0)
                _trace_critical(longest_child)

        _trace_critical(tree)

        return TraceAnalysisReport(
            trace_id=trace_id,
            root_service=root_service,
            total_duration_ms=round(total_duration, 2),
            total_spans=len(spans),
            error_count=error_count,
            services_involved=services,
            critical_path=critical_path,
            root_node=tree,
        )
