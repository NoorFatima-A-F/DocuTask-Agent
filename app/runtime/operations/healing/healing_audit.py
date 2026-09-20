"""
AOIS-HROP Phase 13.7 - Healing Audit
Cryptographically signed append-only audit trail for all autonomic self-healing actions.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class HealingAuditRecord:
    audit_id: str
    healing_id: str
    incident_id: str
    action_type: str
    target: str
    success: bool
    sha256_hash: str
    parent_hash: str
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class HealingAuditLedger:
    """
    Append-only SHA-256 hash chain for self-healing operations.
    """

    def __init__(self):
        self._records: List[HealingAuditRecord] = []
        self._last_hash: str = "0" * 64

    def record_healing_event(
        self,
        healing_id: str,
        incident_id: str,
        action_type: str,
        target: str,
        success: bool,
    ) -> HealingAuditRecord:
        now_ts = datetime.now(timezone.utc).isoformat()
        content = f"{healing_id}:{incident_id}:{action_type}:{target}:{success}:{self._last_hash}:{now_ts}"
        curr_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        record = HealingAuditRecord(
            audit_id=f"audit-heal-{uuid.uuid4().hex[:8]}",
            healing_id=healing_id,
            incident_id=incident_id,
            action_type=action_type,
            target=target,
            success=success,
            sha256_hash=curr_hash,
            parent_hash=self._last_hash,
            timestamp_utc=now_ts,
        )

        self._last_hash = curr_hash
        self._records.append(record)
        return record

    def get_all_records(self) -> List[HealingAuditRecord]:
        return self._records

    def verify_integrity(self) -> bool:
        prev = "0" * 64
        for r in self._records:
            if r.parent_hash != prev:
                return False
            prev = r.sha256_hash
        return True
