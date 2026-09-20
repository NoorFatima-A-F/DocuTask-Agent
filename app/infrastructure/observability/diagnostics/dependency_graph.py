"""
Dynamic Service Dependency Graph.

Reconstructs runtime service dependency topology from distributed trace spans,
calculating edge call counts, average/p99 latencies, and error rates.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field

from app.infrastructure.observability.tracing.models import Span, SpanStatus

logger = logging.getLogger("infrastructure.observability.diagnostics.dependency_graph")


class DependencyEdge(BaseModel):
    """Directed dependency connection from caller service to callee service."""
    caller_service: str
    callee_service: str
    call_count: int = 0
    error_count: int = 0
    total_latency_ms: float = 0.0
    avg_latency_ms: float = 0.0
    error_rate_percent: float = 0.0


class ServiceDependencyGraph:
    """
    Constructs and queries the live service dependency topology.
    """

    def __init__(self) -> None:
        self._edges: Dict[str, DependencyEdge] = {}  # key: caller->callee

    @staticmethod
    def _edge_key(caller: str, callee: str) -> str:
        return f"{caller}->{callee}"

    def record_interaction(
        self,
        caller_service: str,
        callee_service: str,
        latency_ms: float,
        is_error: bool = False,
    ) -> None:
        """Record a single cross-service RPC or message call."""
        if caller_service == callee_service:
            return  # Ignore self-loops

        key = self._edge_key(caller_service, callee_service)
        if key not in self._edges:
            self._edges[key] = DependencyEdge(
                caller_service=caller_service,
                callee_service=callee_service,
            )

        edge = self._edges[key]
        edge.call_count += 1
        edge.total_latency_ms += latency_ms
        if is_error:
            edge.error_count += 1

        edge.avg_latency_ms = round(edge.total_latency_ms / edge.call_count, 2)
        edge.error_rate_percent = round((edge.error_count / edge.call_count) * 100.0, 2)

    def ingest_spans(self, spans: List[Span]) -> None:
        """Derive dependencies automatically from a set of spans in a trace."""
        span_map = {s.span_id: s for s in spans}
        for s in spans:
            if s.parent_span_id and s.parent_span_id in span_map:
                parent = span_map[s.parent_span_id]
                if parent.service_name != s.service_name:
                    self.record_interaction(
                        caller_service=parent.service_name,
                        callee_service=s.service_name,
                        latency_ms=s.duration_ms or 0.0,
                        is_error=(s.status == SpanStatus.ERROR),
                    )

    def get_upstream_dependencies(self, service_name: str) -> List[DependencyEdge]:
        """Find services calling this service."""
        return [e for e in self._edges.values() if e.callee_service == service_name]

    def get_downstream_dependencies(self, service_name: str) -> List[DependencyEdge]:
        """Find services called by this service."""
        return [e for e in self._edges.values() if e.caller_service == service_name]

    def list_all_edges(self) -> List[DependencyEdge]:
        return list(self._edges.values())

    def list_all_services(self) -> List[str]:
        services: Set[str] = set()
        for e in self._edges.values():
            services.add(e.caller_service)
            services.add(e.callee_service)
        return sorted(list(services))
