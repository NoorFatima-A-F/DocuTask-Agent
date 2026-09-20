"""
Governance Policy Engine for Phase 13.3 (ASCE-CGP).
Enforces enterprise confidence governance policies and guards against unverified outputs.
"""

from typing import Dict, Any, Tuple
from app.runtime.confidence.models.confidence_dimensions import ConfidenceStatus


class ConfidenceGovernancePolicy:
    """
    Evaluates confidence integrity, evidence completeness, and truth ledger commitment status.
    """

    @classmethod
    def evaluate_governance(
        cls,
        confidence_score: float,
        evidence_present: bool,
        truth_hash_valid: bool,
        minimum_threshold: float = 0.85,
    ) -> Tuple[ConfidenceStatus, str]:
        if not evidence_present:
            return ConfidenceStatus.REJECTED, "Rejected: Missing required runtime evidence signals."

        if not truth_hash_valid:
            return ConfidenceStatus.UNVERIFIED, "Unverified: Cryptographic truth ledger hash mismatch."

        if confidence_score < minimum_threshold:
            return ConfidenceStatus.DEGRADED, f"Degraded: Confidence score {confidence_score} below threshold {minimum_threshold}."

        return ConfidenceStatus.VERIFIED, "Governance Policy Satisfied: All cryptographic and evidence invariants verified."
