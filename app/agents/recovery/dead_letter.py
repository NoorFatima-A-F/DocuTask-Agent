"""
Dead Letter Management.
Captures permanently failed executions and tasks for manual audit or batch replay.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.recovery.failure import Failure


class DeadLetterRecord(BaseModel):
    """Record placed in dead-letter storage when automatic recovery is exhausted."""
    dead_letter_id: UUID = Field(default_factory=uuid4)
    execution_id: UUID
    failure: Failure
    reason: str
    quarantined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_resolved: bool = Field(default=False)
    model_config = {"frozen": True}


class DeadLetterQueue:
    """Queue storing dead-letter failure records."""

    def __init__(self):
        self._queue: Dict[UUID, DeadLetterRecord] = {}

    def push(self, execution_id: UUID, failure: Failure, reason: str) -> DeadLetterRecord:
        record = DeadLetterRecord(execution_id=execution_id, failure=failure, reason=reason)
        self._queue[record.dead_letter_id] = record
        return record

    def get(self, record_id: UUID) -> Optional[DeadLetterRecord]:
        return self._queue.get(record_id)

    def list_all(self) -> List[DeadLetterRecord]:
        return list(self._queue.values())
