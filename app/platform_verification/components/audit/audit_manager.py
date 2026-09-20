"""
Audit Manager: Immutable append-only hash-chained ledger: H_n = SHA256(H_{n-1} || Payload_n).
"""
from typing import Dict, Any, List, Optional
import hashlib
import json
from datetime import datetime, timezone
from ..interfaces import AuditManagerInterface
from ...crosscutting.observability import ComponentObservability
from ...domain.models import AuditEntry

GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

class AuditManager(AuditManagerInterface):
    """Cryptographic append-only audit ledger."""
    
    def __init__(self):
        self._chain: List[Dict[str, Any]] = []
        self._domain_entries: List[AuditEntry] = []
        self.observability = ComponentObservability("AuditManager")

    def record_event(self, event_type: str, entity_id: str, payload: Dict[str, Any]) -> AuditEntry:
        self.observability.record_operation(1.2)
        prev_hash = self._domain_entries[-1].sha256_entry_hash if self._domain_entries else GENESIS_HASH
        seq = len(self._domain_entries) + 1
        raw = f"{seq}:{event_type}:{entity_id}:{prev_hash}:{json.dumps(payload, sort_keys=True)}"
        entry_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        entry = AuditEntry(
            sequence_number=seq,
            event_type=event_type,
            entity_id=entity_id,
            actor="system_verifier",
            sha256_prev_hash=prev_hash,
            sha256_entry_hash=entry_hash,
            details=payload
        )
        self._domain_entries.append(entry)
        self._chain.append({
            "sequence": seq,
            "event_type": event_type,
            "actor": "system_verifier",
            "timestamp": entry.timestamp,
            "payload": payload,
            "previous_hash": prev_hash,
            "record_hash": entry_hash
        })
        return entry

    async def log_event(self, event_type: str, actor: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.observability.record_operation(1.2)
        prev_hash = self._chain[-1]["record_hash"] if self._chain else GENESIS_HASH
        seq = len(self._chain) + 1
        entry_payload = {
            "sequence": seq,
            "event_type": event_type,
            "actor": actor,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
            "previous_hash": prev_hash
        }
        serialized = json.dumps(entry_payload, sort_keys=True)
        h = hashlib.sha256((prev_hash + serialized).encode("utf-8")).hexdigest()
        entry_payload["record_hash"] = h
        self._chain.append(entry_payload)
        return entry_payload

    def verify_chain_integrity(self) -> bool:
        self.observability.record_operation(2.0)
        if self._domain_entries:
            for i, entry in enumerate(self._domain_entries):
                prev = GENESIS_HASH if i == 0 else self._domain_entries[i-1].sha256_entry_hash
                if entry.sha256_prev_hash != prev:
                    return False
        if self._chain:
            for i, entry in enumerate(self._chain):
                prev = GENESIS_HASH if i == 0 else self._chain[i-1]["record_hash"]
                if entry["previous_hash"] != prev:
                    return False
        return True

    def get_audit_trail(self) -> List[Dict[str, Any]]:
        self.observability.record_operation(0.8)
        return list(self._chain)
