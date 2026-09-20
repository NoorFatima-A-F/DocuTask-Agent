"""
DocuTask Agent - Multi-Criteria Event Filtering Engine
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import List, Dict, Any, Optional, Set
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.models.event_types import DomainEventType, EventSubsystem, EventSeverity


class EventFilterCriteria:
    """Multi-dimensional filtering parameters."""

    def __init__(
        self,
        mission_id: Optional[str] = None,
        event_types: Optional[Set[str]] = None,
        subsystems: Optional[Set[str]] = None,
        actor_ids: Optional[Set[str]] = None,
        severities: Optional[Set[str]] = None,
        min_timestamp: Optional[float] = None,
        max_timestamp: Optional[float] = None,
        search_text: Optional[str] = None,
    ):
        self.mission_id = mission_id
        self.event_types = event_types
        self.subsystems = subsystems
        self.actor_ids = actor_ids
        self.severities = severities
        self.min_timestamp = min_timestamp
        self.max_timestamp = max_timestamp
        self.search_text = search_text.lower() if search_text else None


class EventFilterEngine:
    """
    Evaluates multi-attribute filtering predicates over lists of DomainEvents.
    """

    @staticmethod
    def filter_events(events: List[DomainEvent], criteria: EventFilterCriteria) -> List[DomainEvent]:
        filtered = []

        for e in events:
            if criteria.mission_id and e.mission_id != criteria.mission_id:
                continue

            type_val = e.event_type.value if hasattr(e.event_type, "value") else str(e.event_type)
            if criteria.event_types and type_val not in criteria.event_types:
                continue

            sub_val = e.subsystem.value if hasattr(e.subsystem, "value") else str(e.subsystem)
            if criteria.subsystems and sub_val not in criteria.subsystems:
                continue

            if criteria.actor_ids and e.actor.actor_id not in criteria.actor_ids:
                continue

            sev_val = e.severity.value if hasattr(e.severity, "value") else str(e.severity)
            if criteria.severities and sev_val not in criteria.severities:
                continue

            if criteria.min_timestamp is not None and e.timestamp_utc < criteria.min_timestamp:
                continue

            if criteria.max_timestamp is not None and e.timestamp_utc > criteria.max_timestamp:
                continue

            if criteria.search_text:
                serialized = str(e.payload).lower() + " " + e.component.lower() + " " + type_val.lower()
                if criteria.search_text not in serialized:
                    continue

            filtered.append(e)

        return filtered
