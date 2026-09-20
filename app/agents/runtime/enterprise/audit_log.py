"""
Immutable Runtime Audit Log.
Maintains tamper-evident append-only log with SHA-256 cryptographic hash chaining for regulatory compliance.
"""

import hashlib
import json
from typing import Any, Dict, List, Optional
from app.agents.runtime.enterprise.audit_event import AuditEventType, RuntimeAuditEvent


class ImmutableRuntimeAuditLog:
    """Tamper-evident audit log with hash chain verification."""

    GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

    def __init__(self) -> None:
        self._events: List[RuntimeAuditEvent] = []
        self._last_hash: str = self.GENESIS_HASH

    def append(
        self,
        event_type: AuditEventType,
        actor: str,
        details: Dict[str, Any],
        tenant_id: str = "default",
    ) -> RuntimeAuditEvent:
        """Appends an event into the chain, computing its cryptographic hash."""
        prev_hash = self._last_hash
        data_to_hash = json.dumps(
            {
                "prev_hash": prev_hash,
                "event_type": event_type.value,
                "actor": actor,
                "tenant_id": tenant_id,
                "details": details,
            },
            sort_keys=True,
            default=str,
        )
        event_hash = hashlib.sha256(data_to_hash.encode("utf-8")).hexdigest()

        event = RuntimeAuditEvent(
            event_type=event_type,
            actor=actor,
            tenant_id=tenant_id,
            details=details,
            prev_hash=prev_hash,
            event_hash=event_hash,
        )

        self._events.append(event)
        self._last_hash = event_hash
        return event

    def verify_integrity(self) -> bool:
        """Traverses the audit chain from genesis and verifies that no tampering has occurred."""
        expected_prev = self.GENESIS_HASH
        for event in self._events:
            if event.prev_hash != expected_prev:
                return False
            data_to_hash = json.dumps(
                {
                    "prev_hash": event.prev_hash,
                    "event_type": event.event_type.value,
                    "actor": event.actor,
                    "tenant_id": event.tenant_id,
                    "details": event.details,
                },
                sort_keys=True,
                default=str,
            )
            recomputed = hashlib.sha256(data_to_hash.encode("utf-8")).hexdigest()
            if event.event_hash != recomputed:
                return False
            expected_prev = event.event_hash
        return True

    def list_events(self) -> List[RuntimeAuditEvent]:
        return list(self._events)
