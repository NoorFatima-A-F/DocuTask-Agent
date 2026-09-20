"""
DocuTask Agent - Immutable Domain Event Store
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

import asyncio
from typing import Dict, List, Optional, Any, AsyncIterator
import time
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.models.event_types import DomainEventType
from app.runtime.events.store.partition import MissionPartitionManager
from app.runtime.events.store.append_log import AppendOnlyEventLog


class DomainEventStore:
    """
    Immutable Domain Event Store.
    Provides append-only persistence, mission-partitioned streams,
    correlation index lookups, and deterministic replay capabilities.
    """

    def __init__(self):
        self._partitions = MissionPartitionManager()
        self._global_log = AppendOnlyEventLog(partition_id="global")
        self._index_by_id: Dict[str, DomainEvent] = {}
        self._index_by_correlation: Dict[str, List[DomainEvent]] = {}
        self._index_by_type: Dict[str, List[DomainEvent]] = {}
        self._lock = asyncio.Lock()

    async def append(self, event: DomainEvent) -> int:
        """Appends a domain event to the store with full indexing and hash chaining."""
        async with self._lock:
            # 1. Append to global log
            offset = self._global_log.append(event)

            # 2. Append to mission partition log
            self._partitions.append_to_partition(event)

            # 3. Index by ID
            self._index_by_id[event.event_id] = event

            # 4. Index by Correlation ID
            if event.correlation_id not in self._index_by_correlation:
                self._index_by_correlation[event.correlation_id] = []
            self._index_by_correlation[event.correlation_id].append(event)

            # 5. Index by Event Type
            type_key = event.event_type.value if isinstance(event.event_type, DomainEventType) else str(event.event_type)
            if type_key not in self._index_by_type:
                self._index_by_type[type_key] = []
            self._index_by_type[type_key].append(event)

            return offset

    def get_by_id(self, event_id: str) -> Optional[DomainEvent]:
        """Retrieves a single domain event by its unique ID."""
        return self._index_by_id.get(event_id)

    def get_by_mission(
        self,
        mission_id: str,
        from_offset: int = 0,
        limit: Optional[int] = None,
    ) -> List[DomainEvent]:
        """Retrieves all domain events for a specific mission partition."""
        return self._partitions.get_mission_events(mission_id, from_offset=from_offset, limit=limit)

    def get_by_correlation(self, correlation_id: str) -> List[DomainEvent]:
        """Retrieves all events linked to a single distributed correlation trace."""
        return self._index_by_correlation.get(correlation_id, [])

    def get_by_type(self, event_type: DomainEventType) -> List[DomainEvent]:
        """Retrieves all events of a specific domain event type."""
        type_key = event_type.value if isinstance(event_type, DomainEventType) else str(event_type)
        return self._index_by_type.get(type_key, [])

    def get_timeline(
        self,
        from_offset: int = 0,
        limit: Optional[int] = 100,
        min_timestamp: Optional[float] = None,
        max_timestamp: Optional[float] = None,
    ) -> List[DomainEvent]:
        """Returns chronological global event timeline."""
        events = self._global_log.get_events(from_offset=from_offset, limit=limit)
        if min_timestamp is not None:
            events = [e for e in events if e.timestamp_utc >= min_timestamp]
        if max_timestamp is not None:
            events = [e for e in events if e.timestamp_utc <= max_timestamp]
        return events

    def get_store_stats(self) -> Dict[str, Any]:
        """Returns event store capacity and partitioning metrics."""
        return {
            "total_events_stored": self._global_log.total_count,
            "total_missions_partitioned": len(self._partitions.list_partition_ids()),
            "partitions": self._partitions.get_partition_stats(),
            "indexed_event_types_count": len(self._index_by_type),
            "indexed_correlations_count": len(self._index_by_correlation),
            "integrity_verified": self._global_log.verify_integrity(),
            "timestamp_utc": time.time(),
        }

    async def replay_mission_stream(
        self,
        mission_id: str,
        delay_seconds: float = 0.0,
    ) -> AsyncIterator[DomainEvent]:
        """Asynchronously streams recorded events for deterministic replay."""
        events = self.get_by_mission(mission_id)
        for event in events:
            if delay_seconds > 0:
                await asyncio.sleep(delay_seconds)
            yield event


    def query(
        self,
        mission_id: Optional[str] = None,
        category: Optional[Any] = None,
        limit: int = 50,
    ) -> List[DomainEvent]:
        """Queries stored events by mission ID and/or category."""
        if mission_id:
            events = self.get_by_mission(mission_id, limit=limit)
        else:
            events = self.get_timeline(limit=limit)
        return events


# Global singleton domain event store
domain_event_store = DomainEventStore()


def get_global_event_store() -> DomainEventStore:
    """Returns global singleton domain event store."""
    return domain_event_store
