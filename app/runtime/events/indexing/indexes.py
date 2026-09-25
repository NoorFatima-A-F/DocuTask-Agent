"""
DocuTask Agent - In-Memory Multi-Key Event Index Trees
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import Dict, List
from app.runtime.events.models.event import DomainEvent


class EventIndexTree:
    """
    High-performance in-memory index maps for O(1) multi-attribute lookups.
    """

    def __init__(self):
        self.by_mission: Dict[str, List[str]] = {}
        self.by_type: Dict[str, List[str]] = {}
        self.by_correlation: Dict[str, List[str]] = {}
        self.by_actor: Dict[str, List[str]] = {}

    def index_event(self, event: DomainEvent) -> None:
        """Indexes an event across all primary lookup keys."""
        e_id = event.event_id

        # Index by Mission
        if event.mission_id not in self.by_mission:
            self.by_mission[event.mission_id] = []
        self.by_mission[event.mission_id].append(e_id)

        # Index by Type
        type_str = event.event_type.value if hasattr(event.event_type, "value") else str(event.event_type)
        if type_str not in self.by_type:
            self.by_type[type_str] = []
        self.by_type[type_str].append(e_id)

        # Index by Correlation
        if event.correlation_id not in self.by_correlation:
            self.by_correlation[event.correlation_id] = []
        self.by_correlation[event.correlation_id].append(e_id)

        # Index by Actor
        if event.actor.actor_id not in self.by_actor:
            self.by_actor[event.actor.actor_id] = []
        self.by_actor[event.actor.actor_id].append(e_id)

    def get_event_ids_by_mission(self, mission_id: str) -> List[str]:
        return self.by_mission.get(mission_id, [])

    def get_event_ids_by_type(self, event_type: str) -> List[str]:
        return self.by_type.get(event_type, [])

    def get_event_ids_by_correlation(self, correlation_id: str) -> List[str]:
        return self.by_correlation.get(correlation_id, [])
