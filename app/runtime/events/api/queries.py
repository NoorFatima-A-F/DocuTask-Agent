"""
DocuTask Agent - Event Query Service & Aggregator
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import Dict, List, Any, Optional
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.models.event_types import DomainEventType
from app.runtime.events.store.event_store import domain_event_store
from app.runtime.events.bus.event_bus import domain_event_bus
from app.runtime.events.projections.dashboard_projection import dashboard_projection
from app.runtime.events.projections.planner_projection import planner_projection
from app.runtime.events.projections.mission_projection import mission_projection
from app.runtime.events.projections.worker_projection import worker_projection
from app.runtime.events.projections.telemetry_projection import telemetry_projection
from app.runtime.events.filters.filtering import EventFilterEngine, EventFilterCriteria
from app.runtime.events.correlation.causation import CausationDAGBuilder
from app.runtime.events.correlation.correlation import correlation_tracker


class EventQueryService:
    """
    Unified Event Query & Projection Dispatcher Service.
    Connects EventBus events to the persistent EventStore, projections, and correlation engines.
    """

    def __init__(self):
        # Auto-subscribe store and projections to the event bus
        domain_event_bus.subscribe("system-event-store-indexer", self._on_event_published)

    async def _on_event_published(self, event: DomainEvent) -> None:
        """Handler that writes to store and updates read projections synchronously."""
        await domain_event_store.append(event)
        dashboard_projection.apply_event(event)
        correlation_tracker.track(event)

    async def publish_domain_event(self, event: DomainEvent) -> DomainEvent:
        """Publishes event through the bus (which automatically stores & updates projections)."""
        await domain_event_bus.publish(event)
        return event

    def get_events_for_mission(
        self,
        mission_id: str,
        from_offset: int = 0,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        events = domain_event_store.get_by_mission(mission_id, from_offset=from_offset, limit=limit)
        return [e.to_dict() for e in events]

    def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        event = domain_event_store.get_by_id(event_id)
        return event.to_dict() if event else None

    def get_timeline(
        self,
        from_offset: int = 0,
        limit: int = 100,
        min_timestamp: Optional[float] = None,
        max_timestamp: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        events = domain_event_store.get_timeline(
            from_offset=from_offset,
            limit=limit,
            min_timestamp=min_timestamp,
            max_timestamp=max_timestamp,
        )
        return [e.to_dict() for e in events]

    def filter_events(self, criteria_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        criteria = EventFilterCriteria(
            mission_id=criteria_dict.get("mission_id"),
            event_types=set(criteria_dict["event_types"]) if "event_types" in criteria_dict else None,
            subsystems=set(criteria_dict["subsystems"]) if "subsystems" in criteria_dict else None,
            actor_ids=set(criteria_dict["actor_ids"]) if "actor_ids" in criteria_dict else None,
            severities=set(criteria_dict["severities"]) if "severities" in criteria_dict else None,
            min_timestamp=criteria_dict.get("min_timestamp"),
            max_timestamp=criteria_dict.get("max_timestamp"),
            search_text=criteria_dict.get("search_text"),
        )
        all_events = domain_event_store.get_timeline(limit=1000)
        filtered = EventFilterEngine.filter_events(all_events, criteria)
        return [e.to_dict() for e in filtered]

    def get_correlation_trace(self, correlation_id: str) -> Dict[str, Any]:
        events = domain_event_store.get_by_correlation(correlation_id)
        causation_tree = CausationDAGBuilder.build_causation_tree(events)
        return {
            "correlation_id": correlation_id,
            "total_events": len(events),
            "events": [e.to_dict() for e in events],
            "causation_tree": causation_tree,
        }

    def get_planner_state(self) -> Dict[str, Any]:
        return planner_projection.get_projection_state()

    def get_worker_state(self) -> Dict[str, Any]:
        return worker_projection.get_worker_pool_state()

    def get_telemetry_state(self) -> Dict[str, Any]:
        return telemetry_projection.get_telemetry_state()

    def get_dashboard_state(self) -> Dict[str, Any]:
        return dashboard_projection.get_composite_dashboard_state()


# Global singleton query service
event_query_service = EventQueryService()
