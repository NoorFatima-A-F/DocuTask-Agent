"""
DocuTask Agent - Mission Partition Manager
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import Dict, List, Optional
from app.runtime.events.store.append_log import AppendOnlyEventLog
from app.runtime.events.models.event import DomainEvent


class MissionPartitionManager:
    """
    Manages isolated append logs partitioned by Mission ID.
    Ensures zero cross-mission contamination and enables independent replay slicing.
    """

    def __init__(self):
        self._partitions: Dict[str, AppendOnlyEventLog] = {}

    def get_or_create_partition(self, mission_id: str) -> AppendOnlyEventLog:
        """Retrieves or creates a partition log for the specified mission."""
        if mission_id not in self._partitions:
            self._partitions[mission_id] = AppendOnlyEventLog(partition_id=mission_id)
        return self._partitions[mission_id]

    def append_to_partition(self, event: DomainEvent) -> int:
        """Appends a domain event to its mission partition."""
        partition = self.get_or_create_partition(event.mission_id)
        return partition.append(event)

    def get_mission_events(
        self,
        mission_id: str,
        from_offset: int = 0,
        limit: Optional[int] = None,
    ) -> List[DomainEvent]:
        """Retrieves events from a mission's partition log."""
        if mission_id not in self._partitions:
            return []
        return self._partitions[mission_id].get_events(from_offset=from_offset, limit=limit)

    def list_partition_ids(self) -> List[str]:
        """Returns all active mission partition IDs."""
        return list(self._partitions.keys())

    def get_partition_stats(self) -> Dict[str, int]:
        """Returns event counts per mission partition."""
        return {m_id: p.total_count for m_id, p in self._partitions.items()}
