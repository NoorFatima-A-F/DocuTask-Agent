"""Audit Trail Integrity Verifier."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from ..core.events import AuditEvent
from .hashing import HashChainCalculator
from .signatures import AuditSigner


class IntegrityVerificationResult(BaseModel):
    is_valid: bool
    total_events_checked: int
    tampered_event_ids: List[str] = Field(default_factory=list)
    broken_chain_at: Optional[str] = None
    signature_failures: List[str] = Field(default_factory=list)
    details: Dict[str, Any] = Field(default_factory=dict)


class AuditIntegrityVerifier:
    """Verifies cryptographic hash chains and signature authenticity across audit logs."""

    def __init__(self, signer: Optional[AuditSigner] = None):
        self.calculator = HashChainCalculator()
        self.signer = signer or AuditSigner()

    def verify_chain(self, events: List[AuditEvent]) -> IntegrityVerificationResult:
        if not events:
            return IntegrityVerificationResult(
                is_valid=True,
                total_events_checked=0,
            )

        tampered_event_ids: List[str] = []
        signature_failures: List[str] = []
        broken_chain_at: Optional[str] = None

        expected_previous_hash = HashChainCalculator.GENESIS_HASH

        for idx, event in enumerate(events):
            # 1. Check previous_hash link
            if event.previous_hash != expected_previous_hash:
                broken_chain_at = event.event_id
                tampered_event_ids.append(event.event_id)
                break

            # 2. Re-compute hash
            recomputed_hash = self.calculator.compute_event_hash(event, previous_hash=expected_previous_hash)
            if event.integrity_hash != recomputed_hash:
                tampered_event_ids.append(event.event_id)
                broken_chain_at = event.event_id
                break

            # 3. Check digital signature if present
            if event.signature:
                if not self.signer.verify_signature(event.integrity_hash, event.signature):
                    signature_failures.append(event.event_id)
                    tampered_event_ids.append(event.event_id)

            expected_previous_hash = event.integrity_hash

        is_valid = len(tampered_event_ids) == 0 and len(signature_failures) == 0

        return IntegrityVerificationResult(
            is_valid=is_valid,
            total_events_checked=len(events),
            tampered_event_ids=tampered_event_ids,
            broken_chain_at=broken_chain_at,
            signature_failures=signature_failures,
            details={
                "last_verified_hash": expected_previous_hash if is_valid else None,
            },
        )
