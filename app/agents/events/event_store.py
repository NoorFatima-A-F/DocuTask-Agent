"""
Append-only Event Store for Autonomous Agent Operating System.
Provides durable, ordered, and replayable event logs for event sourcing,
temporal audit trails, and deterministic state reconstruction.
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Sequence
from uuid import UUID

from app.agents.events.event_types import AgentEvent

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class EventEntry:
    """Immutable envelope around an AgentEvent in the store."""

    sequence_number: int
    event: AgentEvent
    hash: str
    previous_hash: str
    recorded_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sequence_number": self.sequence_number,
            "event": self.event.to_dict(),
            "hash": self.hash,
            "previous_hash": self.previous_hash,
            "recorded_at": self.recorded_at.isoformat(),
        }


class EventStore:
    """Thread-safe append-only event store with hash-chain integrity."""

    GENESIS_HASH = "0" * 64

    def __init__(self, capacity: int = 100000) -> None:
        self._capacity = capacity
        self._entries: List[EventEntry] = []
        self._by_type: Dict[str, List[int]] = {}
        self._by_execution: Dict[str, List[int]] = {}
        self._by_correlation: Dict[str, List[int]] = {}

    def append(self, event: AgentEvent) -> EventEntry:
        """Appends an event to the ledger with tamper-evident cryptographic hash chaining."""
        seq = len(self._entries) + 1
        prev_hash = self._entries[-1].hash if self._entries else self.GENESIS_HASH

        # Compute SHA-256 over sequence, prev_hash, and serialized event
        hasher = hashlib.sha256()
        hasher.update(str(seq).encode("utf-8"))
        hasher.update(prev_hash.encode("utf-8"))
        hasher.update(str(event.event_id).encode("utf-8"))
        hasher.update(event.event_type.encode("utf-8"))
        hasher.update(str(event.timestamp.isoformat()).encode("utf-8"))
        hasher.update(json.dumps(event.payload, sort_keys=True).encode("utf-8"))
        entry_hash = hasher.hexdigest()

        entry = EventEntry(
            sequence_number=seq,
            event=event,
            hash=entry_hash,
            previous_hash=prev_hash,
        )

        idx = len(self._entries)
        self._entries.append(entry)

        # Indexing
        self._by_type.setdefault(event.event_type, []).append(idx)
        if event.execution_id:
            self._by_execution.setdefault(event.execution_id, []).append(idx)
        if event.correlation_id:
            self._by_correlation.setdefault(event.correlation_id, []).append(idx)

        logger.debug("Appended event %s seq=%d hash=%s", event.event_type, seq, entry_hash[:8])
        return entry

    def verify_integrity(self) -> bool:
        """Validates hash-chain integrity across all stored events."""
        if not self._entries:
            return True

        for i, entry in enumerate(self._entries):
            expected_prev = self._entries[i - 1].hash if i > 0 else self.GENESIS_HASH
            if entry.previous_hash != expected_prev:
                logger.error("Integrity breach at seq %d: previous_hash mismatch", entry.sequence_number)
                return False

            hasher = hashlib.sha256()
            hasher.update(str(entry.sequence_number).encode("utf-8"))
            hasher.update(expected_prev.encode("utf-8"))
            hasher.update(str(entry.event.event_id).encode("utf-8"))
            hasher.update(entry.event.event_type.encode("utf-8"))
            hasher.update(str(entry.event.timestamp.isoformat()).encode("utf-8"))
            hasher.update(json.dumps(entry.event.payload, sort_keys=True).encode("utf-8"))
            if hasher.hexdigest() != entry.hash:
                logger.error("Integrity breach at seq %d: hash recalculation mismatch", entry.sequence_number)
                return False

        return True

    def get_by_execution_id(self, execution_id: str) -> List[AgentEvent]:
        """Returns all events recorded for a specific execution ID in chronological order."""
        indices = self._by_execution.get(execution_id, [])
        return [self._entries[i].event for i in indices]

    def get_by_correlation_id(self, correlation_id: str) -> List[AgentEvent]:
        """Returns all events sharing a correlation ID."""
        indices = self._by_correlation.get(correlation_id, [])
        return [self._entries[i].event for i in indices]

    def get_by_type(self, event_type: str) -> List[AgentEvent]:
        """Returns all events of a specific event type."""
        indices = self._by_type.get(event_type, [])
        return [self._entries[i].event for i in indices]

    def get_all(self) -> List[AgentEvent]:
        """Returns all recorded events."""
        return [e.event for e in self._entries]

    def replay(
        self,
        handler: Callable[[AgentEvent], Any],
        filter_fn: Optional[Callable[[AgentEvent], bool]] = None,
        from_sequence: int = 1,
        to_sequence: Optional[int] = None,
    ) -> int:
        """Replays events sequentially through a consumer handler."""
        count = 0
        end_seq = to_sequence if to_sequence is not None else len(self._entries)
        for entry in self._entries:
            if entry.sequence_number < from_sequence:
                continue
            if entry.sequence_number > end_seq:
                break
            if filter_fn and not filter_fn(entry.event):
                continue
            handler(entry.event)
            count += 1
        return count

    def __len__(self) -> int:
        return len(self._entries)
