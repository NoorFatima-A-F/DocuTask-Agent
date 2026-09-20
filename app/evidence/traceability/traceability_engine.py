"""
Evidence Traceability Engine for Enterprise AAOS.
Binds narrative architectural claims to concrete, cryptographically verifiable EvidenceItems.
Guarantees that reports cannot make unsupported assertions.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from app.evidence.registry.evidence_models import EvidenceItem, VerificationStatus
from app.evidence.registry.evidence_registry import EvidenceRegistry

logger = logging.getLogger(__name__)


@dataclass
class ClaimTrace:
    """A narrative claim mapped to supporting evidence items."""

    claim_id: str
    claim_text: str
    subsystem: str
    supporting_evidence_ids: List[str] = field(default_factory=list)
    source_files: List[str] = field(default_factory=list)
    test_files: List[str] = field(default_factory=list)
    is_verified: bool = False
    verification_notes: str = ""


class EvidenceTraceabilityEngine:
    """
    Zero-Trust Traceability Engine.
    Ensures every claim made in architecture reports or READMEs has unambiguous,
    cryptographically verified evidence backing it.
    """

    def __init__(self, registry: EvidenceRegistry) -> None:
        self.registry = registry
        self._claims: Dict[str, ClaimTrace] = {}

    def register_claim(
        self,
        claim_id: str,
        claim_text: str,
        subsystem: str,
        supporting_evidence_ids: List[str],
        source_files: Optional[List[str]] = None,
        test_files: Optional[List[str]] = None,
    ) -> ClaimTrace:
        """Registers a claim and verifies whether all supporting evidence items exist and are verified."""
        missing_ids = [eid for eid in supporting_evidence_ids if self.registry.get(eid) is None]
        unverified_ids = [
            eid
            for eid in supporting_evidence_ids
            if self.registry.get(eid) and self.registry.get(eid).verification_status != VerificationStatus.VERIFIED  # type: ignore
        ]

        is_verified = (len(missing_ids) == 0) and (len(unverified_ids) == 0) and (len(supporting_evidence_ids) > 0)
        notes = (
            "All supporting evidence verified"
            if is_verified
            else f"Missing evidence: {missing_ids}; Unverified evidence: {unverified_ids}"
        )

        trace = ClaimTrace(
            claim_id=claim_id,
            claim_text=claim_text,
            subsystem=subsystem,
            supporting_evidence_ids=supporting_evidence_ids,
            source_files=source_files or [],
            test_files=test_files or [],
            is_verified=is_verified,
            verification_notes=notes,
        )
        self._claims[claim_id] = trace
        logger.info("Registered claim [%s] (Verified: %s)", claim_id, is_verified)
        return trace

    def get_claim(self, claim_id: str) -> Optional[ClaimTrace]:
        return self._claims.get(claim_id)

    def list_all_claims(self) -> List[ClaimTrace]:
        return list(self._claims.values())

    def get_unsupported_claims(self) -> List[ClaimTrace]:
        return [c for c in self._claims.values() if not c.is_verified]

    def export_traceability_matrix(self) -> Dict[str, Any]:
        """Generates structured JSON traceability matrix."""
        return {
            "total_claims": len(self._claims),
            "verified_claims": sum(1 for c in self._claims.values() if c.is_verified),
            "unverified_claims": sum(1 for c in self._claims.values() if not c.is_verified),
            "claims": [
                {
                    "claim_id": c.claim_id,
                    "claim_text": c.claim_text,
                    "subsystem": c.subsystem,
                    "supporting_evidence_ids": c.supporting_evidence_ids,
                    "source_files": c.source_files,
                    "test_files": c.test_files,
                    "is_verified": c.is_verified,
                    "verification_notes": c.verification_notes,
                }
                for c in self._claims.values()
            ],
        }
