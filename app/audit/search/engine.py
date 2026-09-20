"""Multi-Facet Audit Search Engine & Execution Timeline Graph Reconstruction."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from ..core.events import AuditEvent
from ..storage.repository import AuditRepository
from .filters import AuditSearchFilter
from .indexing import AuditInvertedIndex


class AuditSearchResult(BaseModel):
    total_count: int
    matched_count: int
    events: List[AuditEvent] = Field(default_factory=list)
    limit: int
    offset: int


class ExecutionTimelineNode(BaseModel):
    event_id: str
    event_type: str
    action: str
    actor_id: str
    actor_type: str
    resource_type: str
    resource_id: str
    timestamp: datetime
    duration_ms: Optional[float] = None
    outcome: str
    severity: str
    children: List["ExecutionTimelineNode"] = Field(default_factory=list)


class ExecutionTimelineGraph(BaseModel):
    correlation_id: str
    tenant_id: str
    total_events: int
    root_nodes: List[ExecutionTimelineNode] = Field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_duration_ms: Optional[float] = None
    has_errors: bool = False


class AuditSearchEngine:
    """High-performance search and timeline reconstruction engine."""

    def __init__(self, repository: Optional[AuditRepository] = None):
        self.repository = repository or AuditRepository()
        self.indexer = AuditInvertedIndex()

    def index_events(self, events: List[AuditEvent]) -> None:
        for ev in events:
            self.indexer.index_event(ev)

    def search(self, search_filter: AuditSearchFilter) -> AuditSearchResult:
        tenant_events = self.repository.list_by_tenant(search_filter.tenant_id)
        
        # 1. Full-text filter if query provided
        matching_ids: Optional[set] = None
        if search_filter.query:
            self.index_events(tenant_events)
            matching_ids = self.indexer.search_terms(search_filter.query)

        filtered: List[AuditEvent] = []
        for ev in tenant_events:
            if matching_ids is not None and ev.event_id not in matching_ids:
                continue

            # Faceted filters
            if search_filter.organization_id and ev.organization_id != search_filter.organization_id:
                continue
            if search_filter.actor_id and ev.actor_id != search_filter.actor_id:
                continue
            if search_filter.actor_type and (ev.actor_type.value if hasattr(ev.actor_type, "value") else str(ev.actor_type)) != search_filter.actor_type:
                continue
            if search_filter.resource_type and ev.resource_type != search_filter.resource_type:
                continue
            if search_filter.resource_id and ev.resource_id != search_filter.resource_id:
                continue
            if search_filter.event_type and ev.event_type != search_filter.event_type:
                continue
            if search_filter.category and (ev.category.value if hasattr(ev.category, "value") else str(ev.category)) != search_filter.category:
                continue
            if search_filter.severity and (ev.severity.value if hasattr(ev.severity, "value") else str(ev.severity)) != search_filter.severity:
                continue
            if search_filter.outcome and (ev.outcome.value if hasattr(ev.outcome, "value") else str(ev.outcome)) != search_filter.outcome:
                continue
            if search_filter.correlation_id and ev.correlation_id != search_filter.correlation_id:
                continue
            if search_filter.request_id and ev.request_id != search_filter.request_id:
                continue
            if search_filter.workflow_id and ev.workflow_id != search_filter.workflow_id:
                continue
            if search_filter.agent_id and ev.agent_id != search_filter.agent_id:
                continue
            if search_filter.min_risk_score is not None and ev.risk_score < search_filter.min_risk_score:
                continue
            if search_filter.start_time and ev.timestamp < search_filter.start_time:
                continue
            if search_filter.end_time and ev.timestamp > search_filter.end_time:
                continue

            filtered.append(ev)

        # Sort by timestamp descending
        filtered.sort(key=lambda e: e.timestamp, reverse=True)

        total_matched = len(filtered)
        paginated = filtered[search_filter.offset : search_filter.offset + search_filter.limit]

        return AuditSearchResult(
            total_count=len(tenant_events),
            matched_count=total_matched,
            events=paginated,
            limit=search_filter.limit,
            offset=search_filter.offset,
        )

    def reconstruct_timeline(self, correlation_id: str, tenant_id: str) -> ExecutionTimelineGraph:
        """Builds a hierarchical execution tree across all events sharing correlation_id."""
        events = self.repository.find_by_correlation(correlation_id, tenant_id=tenant_id)
        if not events:
            return ExecutionTimelineGraph(
                correlation_id=correlation_id,
                tenant_id=tenant_id,
                total_events=0,
            )

        # Sort chronologically
        events.sort(key=lambda e: e.timestamp)
        nodes: Dict[str, ExecutionTimelineNode] = {}
        has_errors = False

        for ev in events:
            if ev.outcome.value in ["FAILURE", "ERROR", "DENIED"]:
                has_errors = True
            nodes[ev.event_id] = ExecutionTimelineNode(
                event_id=ev.event_id,
                event_type=ev.event_type,
                action=ev.action,
                actor_id=ev.actor_id,
                actor_type=ev.actor_type.value if hasattr(ev.actor_type, "value") else str(ev.actor_type),
                resource_type=ev.resource_type,
                resource_id=ev.resource_id,
                timestamp=ev.timestamp,
                duration_ms=ev.duration_ms,
                outcome=ev.outcome.value if hasattr(ev.outcome, "value") else str(ev.outcome),
                severity=ev.severity.value if hasattr(ev.severity, "value") else str(ev.severity),
            )

        root_nodes: List[ExecutionTimelineNode] = []
        for ev in events:
            node = nodes[ev.event_id]
            if ev.parent_event_id and ev.parent_event_id in nodes:
                nodes[ev.parent_event_id].children.append(node)
            else:
                root_nodes.append(node)

        start_time = events[0].timestamp
        end_time = events[-1].timestamp
        total_duration = (end_time - start_time).total_seconds() * 1000.0

        return ExecutionTimelineGraph(
            correlation_id=correlation_id,
            tenant_id=tenant_id,
            total_events=len(events),
            root_nodes=root_nodes,
            start_time=start_time,
            end_time=end_time,
            total_duration_ms=round(total_duration, 2),
            has_errors=has_errors,
        )
