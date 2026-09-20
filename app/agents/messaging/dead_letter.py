"""
Dead Letter Queue (DLQ) Subsystem.
Captures failed messages after retry policy exhaustion for inspection and replay.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from app.agents.messaging.envelopes import MessageEnvelope


class FailedMessage(BaseModel):
    """Failed message record captured in DLQ."""

    envelope: MessageEnvelope
    failure_reason: str
    failed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    attempt_count: int = Field(default=1, ge=1)

    model_config = {"frozen": True}


class DeadLetterQueue:
    """In-memory / Cloud Pub/Sub compatible Dead Letter Queue."""

    def __init__(self):
        self._dead_letters: List[FailedMessage] = []

    def enqueue(self, envelope: MessageEnvelope, reason: str, attempts: int = 1) -> None:
        """Enqueues a failed message to DLQ."""
        failed = FailedMessage(envelope=envelope, failure_reason=reason, attempt_count=attempts)
        self._dead_letters.append(failed)

    def list_failed(self) -> List[FailedMessage]:
        """Lists all dead-lettered messages."""
        return list(self._dead_letters)

    def clear(self) -> None:
        """Clears dead letter queue."""
        self._dead_letters.clear()
