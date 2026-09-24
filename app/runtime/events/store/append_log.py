"""
DocuTask Agent - Sequential Append-Only Event Log
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

import hashlib
import json
from typing import List, Optional
from app.runtime.events.models.event import DomainEvent


class AppendOnlyEventLog:
    """
    Append-Only Sequential Event Log.
    Enforces absolute event immutability, monotonic replay offsets,
    and cryptographic SHA-256 hash continuity.
    """

    def __init__(self, partition_id: str = "default"):
        self.partition_id = partition_id
        self._events: List[DomainEvent] = []
        self._latest_hash: str = "0" * 64

    def append(self, event: DomainEvent) -> int:
        """
        Appends an event to the log.
        Sets the sequential replay offset and links the SHA-256 parent hash chain.
        """
        offset = len(self._events)
        event.replay_offset = offset

        # Compute hash continuity
        payload_canonical = json.dumps(event.payload, sort_keys=True, default=str)
        link_str = f"{self._latest_hash}:{offset}:{event.event_id}:{event.timestamp_utc}:{payload_canonical}"
        event.truth_ledger_hash = hashlib.sha256(link_str.encode("utf-8")).hexdigest()
        self._latest_hash = event.truth_ledger_hash

        self._events.append(event)
        return offset

    def get_events(self, from_offset: int = 0, limit: Optional[int] = None) -> List[DomainEvent]:
        """Retrieves an ordered slice of events from the specified offset."""
        if from_offset < 0:
            from_offset = 0
        slice_events = self._events[from_offset:]
        if limit is not None and limit > 0:
            slice_events = slice_events[:limit]
        return slice_events

    def get_by_offset(self, offset: int) -> Optional[DomainEvent]:
        """Retrieves a single event by its exact sequential offset."""
        if 0 <= offset < len(self._events):
            return self._events[offset]
        return None

    def verify_integrity(self) -> bool:
        """Cryptographically verifies that the append log has not been tampered with."""
        prev_hash = "0" * 64
        for idx, event in enumerate(self._events):
            if event.replay_offset != idx:
                return False
            payload_canonical = json.dumps(event.payload, sort_keys=True, default=str)
            expected_link = f"{prev_hash}:{idx}:{event.event_id}:{event.timestamp_utc}:{payload_canonical}"
            expected_hash = hashlib.sha256(expected_link.encode("utf-8")).hexdigest()
            if event.truth_ledger_hash != expected_hash:
                return False
            prev_hash = expected_hash
        return True

    @property
    def total_count(self) -> int:
        return len(self._events)
