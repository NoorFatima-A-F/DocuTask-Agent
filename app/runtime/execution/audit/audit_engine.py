"""
Audit & Compliance Engine for Phase 13.15.
Maintains a tamper-evident, SHA-256 cryptographically chained execution audit ledger.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.execution.events.execution_events import (
    ExecutionEvent,
    ExecutionEventType,
    RiskLevel,
    execution_event_bus,
)


@dataclass
class AuditEntry:
    entry_id: str
    mission_id: str
    step_id: Optional[str]
    tool_id: Optional[str]
    action_type: str  # execution, validation, approval, compensation, rollback
    actor: str
    risk_level: RiskLevel
    payload_summary: Dict[str, Any]
    prev_hash: str
    hash_signature: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "mission_id": self.mission_id,
            "step_id": self.step_id,
            "tool_id": self.tool_id,
            "action_type": self.action_type,
            "actor": self.actor,
            "risk_level": self.risk_level.value if isinstance(self.risk_level, RiskLevel) else str(self.risk_level),
            "payload_summary": self.payload_summary,
            "prev_hash": self.prev_hash,
            "hash_signature": self.hash_signature,
            "timestamp": self.timestamp,
        }


class AuditEngine:
    """Manages immutable audit log with cryptographic block chaining."""

    GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

    def __init__(self):
        self._entries: List[AuditEntry] = []
        self._last_hash: str = self.GENESIS_HASH
        self._initialize_seed_audit()

    def _initialize_seed_audit(self) -> None:
        pass

    def record_entry(
        self,
        mission_id: str,
        action_type: str,
        actor: str,
        risk_level: RiskLevel,
        payload_summary: Dict[str, Any],
        step_id: Optional[str] = None,
        tool_id: Optional[str] = None,
    ) -> AuditEntry:
        eid = f"audit_{uuid.uuid4().hex[:10]}"
        now = datetime.now(timezone.utc).isoformat()

        # Compute hash chaining signature
        content_to_hash = json.dumps(
            {
                "entry_id": eid,
                "mission_id": mission_id,
                "step_id": step_id,
                "tool_id": tool_id,
                "action_type": action_type,
                "actor": actor,
                "risk_level": risk_level.value if isinstance(risk_level, RiskLevel) else str(risk_level),
                "payload": payload_summary,
                "prev_hash": self._last_hash,
                "timestamp": now,
            },
            sort_keys=True,
        )
        current_hash = hashlib.sha256(content_to_hash.encode("utf-8")).hexdigest()

        entry = AuditEntry(
            entry_id=eid,
            mission_id=mission_id,
            step_id=step_id,
            tool_id=tool_id,
            action_type=action_type,
            actor=actor,
            risk_level=risk_level,
            payload_summary=payload_summary,
            prev_hash=self._last_hash,
            hash_signature=current_hash,
            timestamp=now,
        )

        self._entries.append(entry)
        self._last_hash = current_hash

        execution_event_bus.publish(
            ExecutionEvent(
                event_type=ExecutionEventType.AUDIT_LOG_APPENDED,
                source="audit_engine",
                payload={"entry_id": eid, "action": action_type, "signature": current_hash},
            )
        )

        return entry

    def verify_ledger_integrity(self) -> tuple[bool, Optional[str]]:
        """Verifies the complete SHA-256 chain from genesis to head."""
        prev = self.GENESIS_HASH
        for i, entry in enumerate(self._entries):
            if entry.prev_hash != prev:
                return False, f"Broken chain link at index {i} (entry {entry.entry_id})"

            content_to_hash = json.dumps(
                {
                    "entry_id": entry.entry_id,
                    "mission_id": entry.mission_id,
                    "step_id": entry.step_id,
                    "tool_id": entry.tool_id,
                    "action_type": entry.action_type,
                    "actor": entry.actor,
                    "risk_level": entry.risk_level.value if isinstance(entry.risk_level, RiskLevel) else str(entry.risk_level),
                    "payload": entry.payload_summary,
                    "prev_hash": entry.prev_hash,
                    "timestamp": entry.timestamp,
                },
                sort_keys=True,
            )
            recomputed = hashlib.sha256(content_to_hash.encode("utf-8")).hexdigest()
            if recomputed != entry.hash_signature:
                return False, f"Tampered hash signature detected at entry {entry.entry_id}"
            prev = entry.hash_signature

        return True, None

    def list_entries(self, mission_id: Optional[str] = None, limit: int = 100) -> List[AuditEntry]:
        items = self._entries
        if mission_id:
            items = [e for e in items if e.mission_id == mission_id]
        return items[-limit:]


# Global Singleton
audit_engine = AuditEngine()
