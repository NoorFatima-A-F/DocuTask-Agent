"""Certification Trust Score System.

Replaces binary certification stamps with a continuous, evidence-grounded Evidence Trust Score.
"""

from typing import Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class TrustScoreBreakdown(BaseModel):
    """Component breakdown of overall Trust Score."""
    evidence_integrity: float  # 0-100
    runtime_validation: float  # 0-100
    security_validation: float  # 0-100
    reproducibility: float  # 0-100
    external_verification: float  # 0-100


class EvidenceTrustScore(BaseModel):
    """Full Trust Score entity for a release."""
    target_system: str
    target_version: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    overall_trust_score: float  # 0.0 - 100.0
    trust_level: str  # ENTERPRISE_VERIFIED, COMMERCIALLY_VERIFIED, UNVERIFIED_REJECTED
    is_certified: bool
    breakdown: TrustScoreBreakdown
    rationale: str


class TrustScoreCalculator:
    """Calculates overall software assurance trust score from multi-source evaluations."""

    @classmethod
    def calculate_trust_score(
        cls,
        target_system: str,
        target_version: str,
        integrity_valid: bool,
        reality_result: Dict[str, Any],
        security_result: Dict[str, Any],
        reproducibility_deterministic: bool,
        auditor_consensus_score: float,
        has_contradictions: bool = False,
    ) -> EvidenceTrustScore:
        # Integrity (98 or 0)
        ev_integ = 98.0 if integrity_valid else 0.0

        # Runtime validation (API & DB checks)
        api_ok = reality_result.get("api", {}).get("is_valid", True)
        db_ok = reality_result.get("db", {}).get("is_valid", True)
        runtime_val = 95.0 if (api_ok and db_ok) else 40.0

        # Security validation (Penetration & attack probes)
        sec_rate = security_result.get("defense_rate_percentage", 100.0)
        sec_val = min(100.0, max(0.0, sec_rate))

        # Reproducibility (99 or 0)
        repro = 99.0 if reproducibility_deterministic else 0.0

        # External verification (Auditor simulation consensus)
        ext_ver = auditor_consensus_score

        # Weighted calculation
        overall = (
            0.20 * ev_integ +
            0.25 * runtime_val +
            0.25 * sec_val +
            0.15 * repro +
            0.15 * ext_ver
        )
        overall = round(overall, 1)

        # Critical constraint: If contradictions exist, force rejection
        if has_contradictions or not integrity_valid or not reproducibility_deterministic or sec_rate < 85.0:
            trust_lvl = "UNVERIFIED_REJECTED"
            is_cert = False
            rationale = "Certification rejected due to detected contradictions, integrity failure, or security escape."
        elif overall >= 90.0:
            trust_lvl = "ENTERPRISE_VERIFIED"
            is_cert = True
            rationale = "System achieved high empirical trust across integrity, runtime, security, and auditor consensus."
        elif overall >= 75.0:
            trust_lvl = "COMMERCIALLY_VERIFIED"
            is_cert = True
            rationale = "System meets commercial assurance standards with minor non-critical gaps."
        else:
            trust_lvl = "UNVERIFIED_REJECTED"
            is_cert = False
            rationale = "Overall assurance score falls below minimum threshold."

        breakdown = TrustScoreBreakdown(
            evidence_integrity=ev_integ,
            runtime_validation=runtime_val,
            security_validation=sec_val,
            reproducibility=repro,
            external_verification=ext_ver,
        )

        return EvidenceTrustScore(
            target_system=target_system,
            target_version=target_version,
            overall_trust_score=overall,
            trust_level=trust_lvl,
            is_certified=is_cert,
            breakdown=breakdown,
            rationale=rationale,
        )
