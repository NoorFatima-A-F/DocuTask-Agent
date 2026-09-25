r"""
Immutable Append-Only Event Store.

Maintains the authoritative, tamper-evident log of all system execution events.
Enforces hash-chaining ($E_k \to \text{SHA256}(E_{k-1} + \dots)$), supports pagination,
range filtering, fast replays, and mission state snapshots.
"""

from __future__ import annotations

import asyncio
from typing import Dict, List, Optional, Tuple
from app.runtime.observability.event_index import EventIndex
from app.runtime.observability.event_serializer import EventSerializer
from app.runtime.observability.schemas import (
    BaseRuntimeEvent,
    EventCategory,
    EventSeverity,
)


class EventStore:
    """Thread-safe and async-safe append-only immutable event store with cryptographic integrity."""

    def __init__(self) -> None:
        self._events: List[BaseRuntimeEvent] = []
        self._index: EventIndex = EventIndex()
        self._lock: asyncio.Lock = asyncio.Lock()
        self._last_event_hash_by_mission: Dict[str, str] = {}
        self._global_last_hash: str = "GENESIS"

    async def append(self, event: BaseRuntimeEvent) -> BaseRuntimeEvent:
        """Appends a new event, computing its SHA-256 hash and updating the chain."""
        async with self._lock:
            mission_id = event.mission_id
            prev_hash = self._last_event_hash_by_mission.get(mission_id, "GENESIS")
            
            # Sign and hash-chain event
            signed_event = EventSerializer.sign_and_chain_event(event, prev_hash)
            
            self._events.append(signed_event)
            self._index.index_event(signed_event)
            
            # Update hash pointers
            self._last_event_hash_by_mission[mission_id] = signed_event.event_hash  # type: ignore
            self._global_last_hash = signed_event.event_hash  # type: ignore
            
            return signed_event

    def append_sync(self, event: BaseRuntimeEvent) -> BaseRuntimeEvent:
        """Synchronous append for synchronous execution paths."""
        mission_id = event.mission_id
        prev_hash = self._last_event_hash_by_mission.get(mission_id, "GENESIS")
        signed_event = EventSerializer.sign_and_chain_event(event, prev_hash)
        self._events.append(signed_event)
        self._index.index_event(signed_event)
        self._last_event_hash_by_mission[mission_id] = signed_event.event_hash  # type: ignore
        self._global_last_hash = signed_event.event_hash  # type: ignore
        return signed_event

    def get_events_for_mission(self, mission_id: str) -> List[BaseRuntimeEvent]:
        """Retrieves all events for a given mission in chronological order."""
        events = self._index.get_by_mission(mission_id)
        events.sort(key=lambda e: e.timestamp)
        return events

    def get_events_by_mission(self, mission_id: str) -> List[BaseRuntimeEvent]:
        """Alias for get_events_for_mission."""
        return self.get_events_for_mission(mission_id)

    def get_events_for_trace(self, trace_id: str) -> List[BaseRuntimeEvent]:
        """Retrieves all events belonging to a distributed trace."""
        events = self._index.get_by_trace(trace_id)
        events.sort(key=lambda e: e.timestamp)
        return events

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
        """Queries events using the multi-dimensional secondary index."""
        return self._index.query(
            mission_id=mission_id,
            trace_id=trace_id,
            category=category,
            severity=severity,
            event_type=event_type,
            worker_id=worker_id,
            limit=limit,
            offset=offset,
        )

    def verify_mission_integrity(self, mission_id: str) -> Tuple[bool, int, str]:
        """Verifies cryptographic hash chain integrity for a specific mission."""
        events = self.get_events_for_mission(mission_id)
        return EventSerializer.verify_stream_integrity(events)

    def total_count(self) -> int:
        return len(self._events)

    def clear(self) -> None:
        """Clears all stored events (primarily for testing)."""
        self._events.clear()
        self._index.clear()
        self._last_event_hash_by_mission.clear()
        self._global_last_hash = "GENESIS"
