"""Domain models for Enterprise Audit Certification Authority."""

from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field, ConfigDict


class CertificationStatus(str, Enum):
    """Permitted certification lifecycle statuses."""
    PENDING = "PENDING"
    VALID = "VALID"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"
    FAILED_VERIFICATION = "FAILED_VERIFICATION"


class RevocationReason(str, Enum):
    """Strictly categorized reasons for certificate revocation."""
    EVIDENCE_TAMPERING = "EVIDENCE_TAMPERING"
    SECURITY_VULNERABILITY = "SECURITY_VULNERABILITY"
    INVALID_AUDIT = "INVALID_AUDIT"
    EXPIRED_CERTIFICATION = "EXPIRED_CERTIFICATION"
    FALSE_CLAIM_DISCOVERY = "FALSE_CLAIM_DISCOVERY"


class RevocationRecord(BaseModel):
    """Cryptographically attributable revocation record."""
    certificate_id: str
    revocation_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    reason: RevocationReason
    details: str
    revoked_by: str = "Enterprise-Audit-Certification-Authority"
    signature: str = ""


class EQIBreakdown(BaseModel):
    """Detailed formula components of the Evidence Quality Index."""
    evidence_coverage_score: float  # max 25
    verification_depth_score: float  # max 25
    reproducibility_score: float     # max 20
    integrity_score: float           # max 15
    freshness_score: float           # max 15
    total_eqi: float                 # max 100
    rating: str                      # ENTERPRISE_GRADE, ACCEPTABLE, DEGRADED


class CertificationRecord(BaseModel):
    """Formal, cryptographically signed certification artifact."""
    model_config = ConfigDict(frozen=True)

    certificate_id: str
    system_name: str = "DocuTask Agent"
    release_version: str = "1.0.0"
    audit_engine_version: str = "2.1.0"
    audit_execution_id: str
    issued_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expiry_timestamp: str
    verification_depth: Dict[str, float] = Field(default_factory=dict)
    evidence_root_hash: str
    merkle_root: str
    classification_summary: Dict[str, str] = Field(default_factory=dict)
    critical_findings: List[str] = Field(default_factory=list)
    eqi_score: float = 0.0
    eqi_breakdown: Optional[EQIBreakdown] = None
    policy_name: str = "enterprise_grade"
    policy_compliance: bool = True
    issuer: str = "Enterprise Audit Certification Authority"
    algorithm: str = "Ed25519"
    public_key_pem: str = ""
    signature: str = ""
    status: CertificationStatus = CertificationStatus.VALID
    revocation_info: Optional[RevocationRecord] = None

    @classmethod
    def create_pending(
        cls,
        certificate_id: str,
        system_name: str,
        release_version: str,
        audit_engine_version: str,
        audit_execution_id: str,
        merkle_root: str,
        evidence_root_hash: str,
        validity_days: int = 180,
        **kwargs,
    ) -> "CertificationRecord":
        now = datetime.now(timezone.utc)
        expiry = (now + timedelta(days=validity_days)).isoformat()
        return cls(
            certificate_id=certificate_id,
            system_name=system_name,
            release_version=release_version,
            audit_engine_version=audit_engine_version,
            audit_execution_id=audit_execution_id,
            issued_timestamp=now.isoformat(),
            expiry_timestamp=expiry,
            merkle_root=merkle_root,
            evidence_root_hash=evidence_root_hash,
            status=CertificationStatus.PENDING,
            **kwargs,
        )

    def canonical_payload_for_signing(self) -> str:
        """Produces deterministic JSON representation for digital signature calculation."""
        import json
        payload = {
            "certificate_id": self.certificate_id,
            "system_name": self.system_name,
            "release_version": self.release_version,
            "audit_engine_version": self.audit_engine_version,
            "audit_execution_id": self.audit_execution_id,
            "issued_timestamp": self.issued_timestamp,
            "expiry_timestamp": self.expiry_timestamp,
            "merkle_root": self.merkle_root,
            "evidence_root_hash": self.evidence_root_hash,
            "eqi_score": self.eqi_score,
            "policy_name": self.policy_name,
            "issuer": self.issuer,
            "algorithm": self.algorithm,
        }
        return json.dumps(payload, sort_keys=True)
