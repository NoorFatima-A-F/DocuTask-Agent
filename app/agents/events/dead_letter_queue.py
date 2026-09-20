"""
Dead Letter Queue (DLQ) for Autonomous Agent Operating System.
Captures unroutable, failed, or poisoned events with complete diagnostic context,
supporting inspection, quarantine, retry, and replay.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from app.agents.events.event_types import AgentEvent

logger = logging.getLogger(__name__)


@dataclass
class DeadLetterRecord:
    """Encapsulates a failed event with error diagnostic telemetry."""

    dlq_id: UUID = field(default_factory=uuid4)
    event: AgentEvent = field(default_factory=lambda: AgentEvent())
    topic: str = ""
    error_message: str = ""
    error_type: str = ""
    stack_trace: str = ""
    retry_count: int = 0
    quarantined: bool = False
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dlq_id": str(self.dlq_id),
            "event_id": str(self.event.event_id),
            "event_type": self.event.event_type,
            "topic": self.topic,
            "error_message": self.error_message,
            "error_type": self.error_type,
            "retry_count": self.retry_count,
            "quarantined": self.quarantined,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


class DeadLetterQueue:
    """Thread-safe and async-safe DLQ store."""

    def __init__(self, max_capacity: int = 10000) -> None:
        self._max_capacity = max_capacity
        self._records: List[DeadLetterRecord] = []

    def enqueue(
        self,
        event: AgentEvent,
        topic: str,
        error: Exception,
        retry_count: int = 0,
        quarantined: bool = False,
        stack_trace: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> DeadLetterRecord:
        """Stores a failed event into the dead letter queue."""
        if len(self._records) >= self._max_capacity:
            # Evict oldest non-quarantined record
            for i, r in enumerate(self._records):
                if not r.quarantined:
                    self._records.pop(i)
                    break
            else:
                self._records.pop(0)

        record = DeadLetterRecord(
            event=event,
            topic=topic,
            error_message=str(error),
            error_type=type(error).__name__,
            stack_trace=stack_trace,
            retry_count=retry_count,
            quarantined=quarantined,
            metadata=metadata or {},
        )
        self._records.append(record)
        logger.warning(
            "Event %s on topic '%s' enqueued to DLQ. Error: %s",
            event.event_id,
            topic,
            record.error_message,
        )
        return record

    def get_records(
        self,
        quarantined_only: bool = False,
        event_type: Optional[str] = None,
        limit: int = 100,
    ) -> List[DeadLetterRecord]:
        """Retrieves DLQ records matching criteria."""
        results = []
        for r in reversed(self._records):
            if quarantined_only and not r.quarantined:
                continue
            if event_type and r.event.event_type != event_type:
                continue
            results.append(r)
            if len(results) >= limit:
                break
        return results

    def quarantine(self, dlq_id: UUID) -> bool:
        """Quarantine a record to prevent automated replay."""
        for r in self._records:
            if r.dlq_id == dlq_id:
                r.quarantined = True
                return True
        return False

    def release(self, dlq_id: UUID) -> Optional[DeadLetterRecord]:
        """Releases and removes a record from the DLQ for reprocessing."""
        for i, r in enumerate(self._records):
            if r.dlq_id == dlq_id:
                return self._records.pop(i)
        return None

    def clear(self) -> int:
        """Clears all DLQ records and returns count cleared."""
        count = len(self._records)
        self._records.clear()
        return count

    def __len__(self) -> int:
        return len(self._records)
