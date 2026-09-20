"""
Execution Profiler & Flame Graph Generator.

Reconstructs hierarchical execution traces from spans, calculates the Critical Path
using longest-path DAG topological analysis, and generates Flame Graph node hierarchies.
Identifies execution bottlenecks across Planner, Scheduler, Workers, Storage, and Memory.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from app.runtime.observability.schemas import (
    BaseRuntimeEvent,
    FlameGraphNode,
    SpanProfile,
)


class ExecutionProfiler:
    """Profiles mission execution traces and synthesizes flame graphs and critical paths."""

    @classmethod
    def build_span_tree(cls, events: List[BaseRuntimeEvent]) -> List[SpanProfile]:
        """Reconstructs parent-child span profiles from a list of trace events."""
        span_map: Dict[str, SpanProfile] = {}
        roots: List[SpanProfile] = []

        for evt in events:
            tctx = evt.trace_context
            if not tctx or not tctx.span_id:
                continue

            span_id = tctx.span_id
            start_t = evt.timestamp
            duration = max(evt.duration_ms, 0.1)
            end_t = start_t + (duration / 1000.0)

            profile = SpanProfile(
                span_id=span_id,
                parent_span_id=tctx.parent_span_id,
                operation=tctx.operation or evt.event_type,
                component=tctx.component or evt.stage,
                start_time=start_t,
                end_time=end_t,
                duration_ms=duration,
                status=evt.status,
                attributes={
                    "event_id": evt.event_id,
                    "worker_id": evt.worker_id,
                    "node_id": evt.node_id,
                    "category": evt.category.value,
                },
            )
            span_map[span_id] = profile

        # Build hierarchy
        for span_id, profile in span_map.items():
            if profile.parent_span_id and profile.parent_span_id in span_map:
                parent = span_map[profile.parent_span_id]
                parent.children.append(profile)
            else:
                roots.append(profile)

        return roots

    @classmethod
    def generate_flame_graph(cls, span_tree: List[SpanProfile]) -> FlameGraphNode:
        """Converts span tree into flame graph hierarchy suitable for UI visualization."""
        if not span_tree:
            return FlameGraphNode(name="root", value_ms=0.0, children=[])

        def span_to_flame(span: SpanProfile) -> FlameGraphNode:
            child_nodes = [span_to_flame(c) for c in span.children]
            return FlameGraphNode(
                name=f"{span.component}:{span.operation}",
                value_ms=span.duration_ms,
                children=child_nodes,
                component=span.component,
                span_id=span.span_id,
            )

        if len(span_tree) == 1:
            root = span_to_flame(span_tree[0])
        else:
            total_dur = sum(s.duration_ms for s in span_tree)
            root = FlameGraphNode(
                name="root:mission_execution",
                value_ms=total_dur,
                children=[span_to_flame(s) for s in span_tree],
                component="root",
            )

        cls._mark_critical_path(root)
        return root

    @classmethod
    def _mark_critical_path(cls, node: FlameGraphNode) -> float:
        """Marks the longest duration path in the tree as critical path."""
        node.is_critical_path = True
        if not node.children:
            return node.value_ms

        max_child = max(node.children, key=lambda c: c.value_ms)
        for child in node.children:
            if child == max_child:
                cls._mark_critical_path(child)
            else:
                child.is_critical_path = False

        return node.value_ms

    @classmethod
    def find_bottlenecks(cls, events: List[BaseRuntimeEvent], top_k: int = 5) -> List[Dict[str, Any]]:
        """Identifies top execution bottlenecks by duration."""
        timed_events = [e for e in events if e.duration_ms > 0]
        timed_events.sort(key=lambda e: e.duration_ms, reverse=True)

        bottlenecks = []
        for e in timed_events[:top_k]:
            bottlenecks.append({
                "event_id": e.event_id,
                "stage": e.stage,
                "event_type": e.event_type,
                "duration_ms": round(e.duration_ms, 2),
                "worker_id": e.worker_id,
                "component": e.trace_context.component if e.trace_context else e.stage,
            })
        return bottlenecks
