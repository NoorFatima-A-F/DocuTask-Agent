"""
Sync Coordinator & Delta Synchronization.

Coordinates delta replication batches, catch-up synchronization,
sync leases, and cross-region synchronization checkpoints.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("infrastructure.replication.sync")


class SyncBatch(BaseModel):
    """Batch of delta mutations to replicate across regions."""
    batch_id: str
    stream_id: str
    mutation_count: int = Field(default=0, ge=0)
    sequence_start: int = Field(default=0, ge=0)
    sequence_end: int = Field(default=0, ge=0)
    payload_items: List[Dict[str, Any]] = Field(default_factory=list)
    applied: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SyncCoordinator:
    """
    Coordinates atomic delta synchronization batches between active replication streams.
    """

    def __init__(self) -> None:
        self._batches: Dict[str, SyncBatch] = {}
        self._stream_sequences: Dict[str, int] = {}  # stream_id -> last_sequence_id
        self._sync_locks: Dict[str, float] = {}  # stream_id -> lock_expiration_timestamp

    def acquire_sync_lock(self, stream_id: str, lock_ttl_seconds: float = 30.0) -> bool:
        """Acquire an exclusive sync lease for a replication stream."""
        now = time.time()
        current_lock = self._sync_locks.get(stream_id, 0.0)
        if now < current_lock:
            return False  # Lock held

        self._sync_locks[stream_id] = now + lock_ttl_seconds
        return True

    def release_sync_lock(self, stream_id: str) -> None:
        self._sync_locks.pop(stream_id, None)

    def create_batch(
        self,
        batch_id: str,
        stream_id: str,
        items: List[Dict[str, Any]],
    ) -> SyncBatch:
        """Create a new delta synchronization batch."""
        last_seq = self._stream_sequences.get(stream_id, 0)
        seq_start = last_seq + 1
        seq_end = last_seq + len(items)

        batch = SyncBatch(
            batch_id=batch_id,
            stream_id=stream_id,
            mutation_count=len(items),
            sequence_start=seq_start,
            sequence_end=seq_end,
            payload_items=items,
            applied=False,
        )

        self._batches[batch_id] = batch
        self._stream_sequences[stream_id] = seq_end
        return batch

    def apply_batch(self, batch_id: str) -> bool:
        """Mark a sync batch as successfully applied on target replica."""
        batch = self._batches.get(batch_id)
        if not batch:
            return False
        batch.applied = True
        logger.info(f"Replication batch '{batch_id}' applied successfully for stream '{batch.stream_id}'")
        return True

    def get_batch(self, batch_id: str) -> Optional[SyncBatch]:
        return self._batches.get(batch_id)

    def list_unapplied_batches(self, stream_id: Optional[str] = None) -> List[SyncBatch]:
        batches = [b for b in self._batches.values() if not b.applied]
        if stream_id:
            batches = [b for b in batches if b.stream_id == stream_id]
        return batches
