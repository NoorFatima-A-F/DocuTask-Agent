"""
Secondary Event Inverted Index.

Provides high-speed indexing across multiple dimensions (mission_id, trace_id, agent_id,
worker_id, event_type, category, severity) to enable instantaneous event querying,
filtering, and timeline construction.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional, Set
from app.runtime.observability.schemas import BaseRuntimeEvent, EventCategory, EventSeverity


class EventIndex:
    """In-memory secondary inverted index for fast querying across multidimensional fields."""

    def __init__(self) -> None:
        self._by_id: Dict[str, BaseRuntimeEvent] = {}
        self._by_mission: Dict[str, List[str]] = defaultdict(list)
        self._by_trace: Dict[str, List[str]] = defaultdict(list)
        self._by_agent: Dict[str, List[str]] = defaultdict(list)
        self._by_worker: Dict[str, List[str]] = defaultdict(list)
        self._by_type: Dict[str, List[str]] = defaultdict(list)
        self._by_category: Dict[EventCategory, List[str]] = defaultdict(list)
        self._by_severity: Dict[EventSeverity, List[str]] = defaultdict(list)
        self._by_correlation: Dict[str, List[str]] = defaultdict(list)

    def index_event(self, event: BaseRuntimeEvent) -> None:
        """Indexes an event across all secondary dimensions."""
        eid = event.event_id
        self._by_id[eid] = event

        self._by_mission[event.mission_id].append(eid)
        if event.trace_context and event.trace_context.trace_id:
            self._by_trace[event.trace_context.trace_id].append(eid)
        if event.agent_id:
            self._by_agent[event.agent_id].append(eid)
        if event.worker_id:
            self._by_worker[event.worker_id].append(eid)
        if event.correlation_id:
            self._by_correlation[event.correlation_id].append(eid)

        self._by_type[event.event_type].append(eid)
        self._by_category[event.category].append(eid)
        self._by_severity[event.severity].append(eid)

    def get_by_id(self, event_id: str) -> Optional[BaseRuntimeEvent]:
        return self._by_id.get(event_id)

    def get_by_mission(self, mission_id: str) -> List[BaseRuntimeEvent]:
        return [self._by_id[eid] for eid in self._by_mission.get(mission_id, [])]

    def get_by_trace(self, trace_id: str) -> List[BaseRuntimeEvent]:
        return [self._by_id[eid] for eid in self._by_trace.get(trace_id, [])]

    def get_by_worker(self, worker_id: str) -> List[BaseRuntimeEvent]:
        return [self._by_id[eid] for eid in self._by_worker.get(worker_id, [])]

    def get_by_category(self, category: EventCategory) -> List[BaseRuntimeEvent]:
        return [self._by_id[eid] for eid in self._by_category.get(category, [])]

    def query(
        self,
        mission_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        category: Optional[EventCategory] = None,
        severity: Optional[EventSeverity] = None,
        event_type: Optional[str] = None,
        worker_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[BaseRuntimeEvent]:
        """Performs intersection query across specified filter criteria with pagination."""
        candidate_sets: List[Set[str]] = []

        if mission_id is not None:
            candidate_sets.append(set(self._by_mission.get(mission_id, [])))
        if trace_id is not None:
            candidate_sets.append(set(self._by_trace.get(trace_id, [])))
        if category is not None:
            candidate_sets.append(set(self._by_category.get(category, [])))
        if severity is not None:
            candidate_sets.append(set(self._by_severity.get(severity, [])))
        if event_type is not None:
            candidate_sets.append(set(self._by_type.get(event_type, [])))
        if worker_id is not None:
            candidate_sets.append(set(self._by_worker.get(worker_id, [])))

        if not candidate_sets:
            # Return all events sorted by timestamp
            all_events = list(self._by_id.values())
            all_events.sort(key=lambda e: e.timestamp)
            return all_events[offset : offset + limit]

        # Intersection of all filters
        matching_ids = candidate_sets[0]
        for s in candidate_sets[1:]:
            matching_ids = matching_ids.intersection(s)

        matched_events = [self._by_id[eid] for eid in matching_ids if eid in self._by_id]
        matched_events.sort(key=lambda e: e.timestamp)
        return matched_events[offset : offset + limit]

    def clear(self) -> None:
        """Clears the index."""
        self._by_id.clear()
        self._by_mission.clear()
        self._by_trace.clear()
        self._by_agent.clear()
        self._by_worker.clear()
        self._by_type.clear()
        self._by_category.clear()
        self._by_severity.clear()
        self._by_correlation.clear()
