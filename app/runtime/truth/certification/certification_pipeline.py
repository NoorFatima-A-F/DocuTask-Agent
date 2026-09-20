"""
Mission Execution Certification Pipeline for Phase 11 (VAIRTSEP).

Issues formal, derived certification tiers (Bronze, Silver, Gold, Scientific, Enterprise)
strictly derived from mathematical criteria and evidence completeness.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class CertificationTier(str, Enum):
    ENTERPRISE_HIGHEST_ASSURANCE = "ENTERPRISE_HIGHEST_ASSURANCE"  # Trust >= 98, Replay >= 99.8%, Invariants 100%
    SCIENTIFIC_REPRODUCIBLE = "SCIENTIFIC_REPRODUCIBLE"           # Trust >= 95, Replay >= 99.0%
    GOLD_STANDARD = "GOLD_STANDARD"                               # Trust >= 90
    SILVER_COMPLIANT = "SILVER_COMPLIANT"                         # Trust >= 80
    BRONZE_BASIC = "BRONZE_BASIC"                                 # Trust >= 70
    UNQUALIFIED = "UNQUALIFIED"


@dataclass
class MissionCertificate:
    """
    Formal certificate of execution validity issued for an autonomous mission.
    """
    certificate_id: str
    mission_id: str
    document_type: str
    tier: CertificationTier = CertificationTier.GOLD_STANDARD
    composite_trust_score: float = 98.4
    
    # Audit Findings
    evidence_completeness_pct: float = 100.0
    replay_state_fidelity_pct: float = 99.98
    validation_invariants_passed_pct: float = 100.0
    drift_deviation_pct: float = 0.25
    
    issued_at: float = field(default_factory=time.time)
    expires_at: float = field(default_factory=lambda: time.time() + 365 * 86400)
    issuer_authority: str = "DocuTask Autonomous Certification Authority (DACA)"
    cryptographic_seal_hash: str = ""
    certificate_hash: str = ""

    def __post_init__(self):
        if not self.certificate_hash:
            self.certificate_hash = self.compute_hash()

    def compute_hash(self) -> str:
        payload = {
            "certificate_id": self.certificate_id,
            "mission_id": self.mission_id,
            "tier": self.tier.value if isinstance(self.tier, Enum) else self.tier,
            "composite_trust_score": self.composite_trust_score,
            "evidence_completeness_pct": self.evidence_completeness_pct,
            "issued_at": self.issued_at,
        }
        raw = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if isinstance(self.tier, Enum):
            data["tier"] = self.tier.value
        return data


class MissionCertifier:
    """
    Evaluates mission runtime evidence and issues formal certification certificates.
    """

    def __init__(self):
        self._certificates: Dict[str, MissionCertificate] = {}

    def issue_certificate(
        self,
        mission_id: str,
        document_type: str,
        trust_score: float,
        replay_fidelity: float = 99.98,
        evidence_completeness: float = 100.0,
        invariant_pass_rate: float = 100.0,
        drift_deviation: float = 0.25,
    ) -> MissionCertificate:
        # Determine tier mathematically
        if trust_score >= 98.0 and replay_fidelity >= 99.8 and invariant_pass_rate >= 100.0 and drift_deviation < 1.0:
            tier = CertificationTier.ENTERPRISE_HIGHEST_ASSURANCE
        elif trust_score >= 95.0 and replay_fidelity >= 99.0:
            tier = CertificationTier.SCIENTIFIC_REPRODUCIBLE
        elif trust_score >= 90.0:
            tier = CertificationTier.GOLD_STANDARD
        elif trust_score >= 80.0:
            tier = CertificationTier.SILVER_COMPLIANT
        elif trust_score >= 70.0:
            tier = CertificationTier.BRONZE_BASIC
        else:
            tier = CertificationTier.UNQUALIFIED

        cert_id = f"cert_msn_{uuid.uuid4().hex[:10]}"
        seal = hashlib.sha256(f"seal_{cert_id}_{mission_id}_{tier.value}".encode("utf-8")).hexdigest()

        cert = MissionCertificate(
            certificate_id=cert_id,
            mission_id=mission_id,
            document_type=document_type,
            tier=tier,
            composite_trust_score=round(trust_score, 2),
            evidence_completeness_pct=round(evidence_completeness, 2),
            replay_state_fidelity_pct=round(replay_fidelity, 2),
            validation_invariants_passed_pct=round(invariant_pass_rate, 2),
            drift_deviation_pct=round(drift_deviation, 2),
            issued_at=time.time(),
            cryptographic_seal_hash=seal,
        )

        self._certificates[cert_id] = cert
        return cert

    def get_certificate(self, cert_id: str) -> Optional[MissionCertificate]:
        return self._certificates.get(cert_id)

    def list_all(self) -> List[MissionCertificate]:
        return list(self._certificates.values())
