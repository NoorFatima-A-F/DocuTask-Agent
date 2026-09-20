"""
Checkpoint Manager & State Snapshots.

Manages point-in-time state snapshots, cryptographic verification,
cataloging, restore mechanics, and retention lifecycle.
"""

from __future__ import annotations

import enum
import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("infrastructure.recovery.checkpoints")


class CheckpointType(str, enum.Enum):
    """Type of state checkpoint."""
    STATE_SNAPSHOT = "STATE_SNAPSHOT"
    DATABASE_DUMP = "DATABASE_DUMP"
    TRANSACTION_LOG = "TRANSACTION_LOG"
    WORKLOAD_STATE = "WORKLOAD_STATE"
    CLUSTER_TOPOLOGY = "CLUSTER_TOPOLOGY"


class CheckpointStatus(str, enum.Enum):
    """Lifecycle status of a checkpoint."""
    CREATED = "CREATED"
    VERIFIED = "VERIFIED"
    RESTORING = "RESTORING"
    RESTORED = "RESTORED"
    CORRUPTED = "CORRUPTED"
    EXPIRED = "EXPIRED"


class Checkpoint(BaseModel):
    """Immutable state snapshot metadata."""
    checkpoint_id: str
    checkpoint_type: CheckpointType
    entity_id: str
    region_id: str
    payload_hash: str
    size_bytes: int = 0
    status: CheckpointStatus = CheckpointStatus.CREATED
    retention_days: int = Field(default=30, ge=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CheckpointManager:
    """
    Catalog and manager for state checkpoints with cryptographic integrity verification.
    """

    def __init__(self) -> None:
        self._checkpoints: Dict[str, Checkpoint] = {}
        self._payload_storage: Dict[str, str] = {}  # checkpoint_id -> serialized payload

    def create_checkpoint(
        self,
        checkpoint_id: str,
        checkpoint_type: CheckpointType,
        entity_id: str,
        region_id: str,
        payload_data: Any,
        retention_days: int = 30,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Checkpoint:
        """Create and index a new verified state checkpoint."""
        serialized = json.dumps(payload_data, sort_keys=True, default=str)
        payload_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        size_bytes = len(serialized.encode("utf-8"))

        cp = Checkpoint(
            checkpoint_id=checkpoint_id,
            checkpoint_type=checkpoint_type,
            entity_id=entity_id,
            region_id=region_id,
            payload_hash=payload_hash,
            size_bytes=size_bytes,
            status=CheckpointStatus.CREATED,
            retention_days=retention_days,
            metadata=metadata or {},
        )

        self._checkpoints[checkpoint_id] = cp
        self._payload_storage[checkpoint_id] = serialized
        self.verify_checkpoint(checkpoint_id)
        logger.info(f"Checkpoint '{checkpoint_id}' created and verified for entity '{entity_id}'")
        return cp

    def verify_checkpoint(self, checkpoint_id: str) -> bool:
        """Verify checksum integrity of stored payload."""
        cp = self._checkpoints.get(checkpoint_id)
        payload = self._payload_storage.get(checkpoint_id)
        if not cp or payload is None:
            return False

        computed_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        if computed_hash == cp.payload_hash:
            cp.status = CheckpointStatus.VERIFIED
            return True
        else:
            cp.status = CheckpointStatus.CORRUPTED
            logger.error(f"Checkpoint '{checkpoint_id}' payload hash mismatch: {computed_hash} != {cp.payload_hash}")
            return False

    def get_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        return self._checkpoints.get(checkpoint_id)

    def get_payload(self, checkpoint_id: str) -> Optional[Any]:
        payload_str = self._payload_storage.get(checkpoint_id)
        if payload_str:
            return json.loads(payload_str)
        return None

    def list_checkpoints_for_entity(self, entity_id: str) -> List[Checkpoint]:
        return [cp for cp in self._checkpoints.values() if cp.entity_id == entity_id]

    def prune_expired(self, current_time: Optional[datetime] = None) -> int:
        """Prune checkpoints that have exceeded their retention period."""
        now = current_time or datetime.now(timezone.utc)
        to_delete = []
        for cid, cp in self._checkpoints.items():
            age_days = (now - cp.created_at).total_seconds() / 86400.0
            if age_days > cp.retention_days:
                to_delete.append(cid)

        for cid in to_delete:
            del self._checkpoints[cid]
            self._payload_storage.pop(cid, None)

        return len(to_delete)
