"""
Content-Addressable Append-Only Cryptographic Evidence Store
"""
import json
import hashlib
from typing import Dict, Any, Optional
from app.platform_verification.domain.models import ImmutableEvidenceRecord
from app.platform_verification.domain.interfaces import EvidenceStoreInterface

class ContentAddressableEvidenceStore(EvidenceStoreInterface):
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}
        self._records: Dict[str, ImmutableEvidenceRecord] = {}

    def seal_evidence(self, run_id: str, evidence_data: Dict[str, Any]) -> ImmutableEvidenceRecord:
        serialized = json.dumps(evidence_data, sort_keys=True)
        sha256_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        byte_size = len(serialized.encode("utf-8"))

        record = ImmutableEvidenceRecord(
            sha256_hash=sha256_hash,
            content_type="application/json",
            byte_size=byte_size,
            storage_uri=f"evidence://sha256/{sha256_hash}",
            tamper_verified=True
        )
        self._store[record.evidence_id] = evidence_data
        self._records[record.evidence_id] = record
        return record

    def get_evidence(self, evidence_id: str) -> Optional[Dict[str, Any]]:
        return self._store.get(evidence_id)

    def verify_integrity(self, evidence_id: str) -> bool:
        data = self._store.get(evidence_id)
        record = self._records.get(evidence_id)
        if not data or not record:
            return False
        serialized = json.dumps(data, sort_keys=True)
        current_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        return current_hash == record.sha256_hash

evidence_store = ContentAddressableEvidenceStore()
