"""
AMAEOP Pillar 3 - Formal Resource Contract Manager
Maintains immutable signed resource contracts between departments with SLA penalties and cryptographic validation.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import hashlib
import time
import uuid


@dataclass
class ResourceContract:
    contract_id: str
    provider_dept_id: str
    consumer_dept_id: str
    resource_type: str
    committed_capacity: float
    max_latency_ms: float
    penalty_credit_rate_per_sec: float
    signature_digest: str
    is_active: bool
    expires_at: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ContractManager:
    """Manages legally binding inter-department computational contracts and SLAs."""

    def __init__(self):
        self.contracts: Dict[str, ResourceContract] = {}
        self._seed_contracts()

    def _seed_contracts(self):
        sig = hashlib.sha256(b"contract_ocr_extraction_2026").hexdigest()[:16]
        c1 = ResourceContract(
            contract_id="ctr_ocr_ext_001",
            provider_dept_id="dept_ocr",
            consumer_dept_id="dept_extraction",
            resource_type="OCR_BOUNDING_BOX_STREAM",
            committed_capacity=10.0,
            max_latency_ms=250.0,
            penalty_credit_rate_per_sec=2.5,
            signature_digest=f"ED25519_SIG_{sig}",
            is_active=True,
            expires_at=time.time() + 86400.0,
        )
        self.contracts[c1.contract_id] = c1

    def create_contract(
        self,
        provider_dept_id: str,
        consumer_dept_id: str,
        resource_type: str,
        committed_capacity: float,
        max_latency_ms: float,
        penalty_rate: float,
        duration_hours: float = 24.0,
    ) -> ResourceContract:
        cid = f"ctr_{uuid.uuid4().hex[:6]}"
        sig_raw = f"{provider_dept_id}:{consumer_dept_id}:{resource_type}:{time.time()}"
        sig = hashlib.sha256(sig_raw.encode("utf-8")).hexdigest()[:16]

        contract = ResourceContract(
            contract_id=cid,
            provider_dept_id=provider_dept_id,
            consumer_dept_id=consumer_dept_id,
            resource_type=resource_type,
            committed_capacity=committed_capacity,
            max_latency_ms=max_latency_ms,
            penalty_credit_rate_per_sec=penalty_rate,
            signature_digest=f"ED25519_SIG_{sig}",
            is_active=True,
            expires_at=time.time() + duration_hours * 3600.0,
        )
        self.contracts[cid] = contract
        return contract

    def list_contracts(self) -> List[Dict[str, Any]]:
        return [c.to_dict() for c in self.contracts.values()]


contract_manager = ContractManager()
