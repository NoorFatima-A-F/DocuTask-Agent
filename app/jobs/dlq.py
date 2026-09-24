from app.core.security import sanitize_log_input
"""
Dead Letter Queue (DLQ) & Manual Replay Engine.
Stores failed jobs exceeding max attempts and provides manual replay capabilities.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import logger
from app.jobs.broker import job_broker


class DLQItem(BaseModel):
    """Schema representing a Dead Letter Queue item."""
    job_id: str
    document_id: str
    failure_reason: str
    attempt_count: int
    stack_trace: Optional[str] = None
    original_payload: Dict[str, Any]
    failed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DeadLetterQueueEngine:
    """Engine managing DLQ persistence and manual replay functionality."""

    _dlq_store: Dict[str, DLQItem] = {}

    @classmethod
    def move_to_dlq(
        cls,
        job_id: str,
        document_id: str,
        failure_reason: str,
        attempt_count: int,
        original_payload: Dict[str, Any],
        stack_trace: Optional[str] = None
    ) -> DLQItem:
        """
        Moves a permanently failed job into the DLQ.
        """
        item = DLQItem(
            job_id=job_id,
            document_id=document_id,
            failure_reason=failure_reason,
            attempt_count=attempt_count,
            stack_trace=stack_trace,
            original_payload=original_payload
        )
        cls._dlq_store[job_id] = item
        logger.error(f"Moved permanently failed job '{sanitize_log_input(job_id)}' to DLQ: Reason='{sanitize_log_input(failure_reason)}'")
        return item

    @classmethod
    async def replay_job(cls, job_id: str) -> bool:
        """
        Replays a failed job from DLQ back into the active processing queue.
        """
        if job_id not in cls._dlq_store:
            logger.warning(f"DLQ Replay failed: Job '{sanitize_log_input(job_id)}' not found in DLQ.")
            return False

        item = cls._dlq_store.pop(job_id)
        # Reset attempts and re-enqueue payload
        payload = item.original_payload
        payload["attempt_count"] = 0

        await job_broker.enqueue(payload, priority=payload.get("priority", "HIGH"))
        logger.info(f"Successfully replayed DLQ job '{sanitize_log_input(job_id)}' back to active queue.")
        return True

    @classmethod
    def list_dlq_items(cls) -> List[DLQItem]:
        """Lists all items currently in the DLQ."""
        return list(cls._dlq_store.values())
