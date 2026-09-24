"""
Health History Storage Engine (Part 3H.3.3.5).
Persists and queries health lifecycle transitions, failure events, and recovery durations.
"""
from typing import Dict, Any, List
from app.platform_verification.health_transition_intelligence.domain.models import (
    HealthEvent,
)


class HealthHistoryStorage:
    """
    In-memory and relational audit storage for service health events.
    """

    def __init__(self):
        self._events: List[HealthEvent] = []

    def save_event(self, event: HealthEvent) -> None:
        self._events.append(event)

    def get_events_for_service(self, service_name: str) -> List[HealthEvent]:
        return [e for e in self._events if e.service_name == service_name]

    def get_all_events(self) -> List[HealthEvent]:
        return list(self._events)

    def get_transition_summary(self) -> Dict[str, Any]:
        transitions_by_state: Dict[str, int] = {}
        for e in self._events:
            key = f"{e.previous_state.value} -> {e.new_state.value}"
            transitions_by_state[key] = transitions_by_state.get(key, 0) + 1

        return {
            "total_events": len(self._events),
            "transition_breakdown": transitions_by_state,
            "first_event_timestamp": self._events[0].timestamp if self._events else None,
            "last_event_timestamp": self._events[-1].timestamp if self._events else None,
        }
