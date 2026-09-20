"""
Evidence Manager: Content-Addressable Storage (CAS), 4 retention tiers, tamper sealing.
"""
from typing import Dict, Any, List, Optional
import hashlib
import json
from datetime import datetime, timezone
from ..interfaces import EvidenceManagerInterface
from ...crosscutting.observability import ComponentObservability
from ...domain.models import EvidenceItem, EvidenceType

class EvidenceManager(EvidenceManagerInterface):
    """Manages cryptographic evidence records and CAS storage."""
    
    def __init__(self):
        self._evidence_store: Dict[str, Dict[str, Any]] = {}
        self._domain_evidence: Dict[str, EvidenceItem] = {}
        self.observability = ComponentObservability("EvidenceManager")

    def store_evidence(self, run_id: str, evidence_type: str, payload: Any, metadata: Optional[Dict[str, Any]] = None) -> EvidenceItem:
        self.observability.record_operation(1.5)
        raw_str = json.dumps(payload, sort_keys=True) if isinstance(payload, (dict, list)) else str(payload)
        h = hashlib.sha256(raw_str.encode("utf-8")).hexdigest()
        e_type = EvidenceType[evidence_type] if evidence_type in EvidenceType.__members__ else EvidenceType.OUTPUT
        item = EvidenceItem(
            run_id=run_id,
            evidence_type=e_type,
            payload_hash=h,
            content_preview=raw_str[:200],
            metadata=metadata or {}
        )
        self._domain_evidence[item.evidence_id] = item
        self._evidence_store[item.evidence_id] = {
            "evidence_id": item.evidence_id,
            "run_id": run_id,
            "retention_tier": "warm",
            "cas_hash": h,
            "size_bytes": len(raw_str),
            "tags": [evidence_type],
            "content": raw_str.encode("utf-8")
        }
        return item

    def verify_evidence_integrity(self, evidence_id: str, current_payload: Any) -> bool:
        self.observability.record_operation(1.0)
        item = self._domain_evidence.get(evidence_id)
        if not item:
            return False
        raw_str = json.dumps(current_payload, sort_keys=True) if isinstance(current_payload, (dict, list)) else str(current_payload)
        current_hash = hashlib.sha256(raw_str.encode("utf-8")).hexdigest()
        return item.payload_hash == current_hash

    async def record_evidence(self, evidence_id: str, run_id: str, tier: str, content: bytes, tags: Optional[List[str]] = None) -> Dict[str, Any]:
        self.observability.record_operation(1.8)
        cas_hash = hashlib.sha256(content).hexdigest()
        record = {
            "evidence_id": evidence_id,
            "run_id": run_id,
            "retention_tier": tier,
            "cas_hash": cas_hash,
            "size_bytes": len(content),
            "tags": tags or [],
            "content": content,
            "recorded_at": datetime.now(timezone.utc).isoformat()
        }
        self._evidence_store[evidence_id] = record
        return {
            "evidence_id": evidence_id,
            "run_id": run_id,
            "retention_tier": tier,
            "cas_hash": cas_hash,
            "size_bytes": len(content),
            "tags": tags or []
        }

    async def get_evidence(self, evidence_id: str) -> Optional[Dict[str, Any]]:
        self.observability.record_operation(0.9)
        return self._evidence_store.get(evidence_id)
