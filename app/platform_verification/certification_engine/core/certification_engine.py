"""
Enterprise Certification Engine managing formal certification records, levels, and cryptographic signatures.
"""
from __future__ import annotations
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
import uuid
from app.platform_verification.certification_engine.domain.interfaces import ICertificationEngine
from app.platform_verification.certification_engine.domain.models import (
    CertificationLevel,
    CertificationRecord,
    CertificationStatus,
    QualityGateDecision,
    ReleaseDecisionType,
)


class EnterpriseCertificationEngine(ICertificationEngine):
    """Issues, cryptographically signs, validates, and manages lifecycle of system certifications."""

    def __init__(self, secret_key: str = "enterprise_verification_sec_key"):
        self.secret_key = secret_key
        self._certifications: Dict[str, CertificationRecord] = {}

    def issue_certification(
        self,
        decision: QualityGateDecision,
        evidence_package_id: str,
        approved_by: str,
        validity_days: int = 90,
    ) -> CertificationRecord:
        if decision.decision not in (ReleaseDecisionType.APPROVED, ReleaseDecisionType.CONDITIONAL_APPROVAL):
            raise ValueError(f"Cannot issue certification for decision with status '{decision.decision.value}'")

        cert_id = f"CERT-{decision.target_certification_level.value[:6]}-{uuid.uuid4().hex[:8].upper()}"
        issued_at = datetime.now(timezone.utc).isoformat()
        expires_at = (datetime.now(timezone.utc) + timedelta(days=validity_days)).isoformat()

        status = (
            CertificationStatus.ACTIVE
            if decision.decision == ReleaseDecisionType.APPROVED
            else CertificationStatus.PROVISIONAL
        )

        record = CertificationRecord(
            id=cert_id,
            system_id=decision.system_id,
            system_version=decision.system_version,
            model_version=decision.model_version,
            certification_level=decision.target_certification_level,
            score=decision.total_score,
            evidence_package_id=evidence_package_id,
            decision_id=decision.decision_id,
            approved_by=approved_by,
            issued_at=issued_at,
            expires_at=expires_at,
            status=status,
            tags={"risk_level": decision.risk_assessment.risk_level.value},
            audit_trail=[
                {
                    "action": "CertificationIssued",
                    "actor": approved_by,
                    "timestamp": issued_at,
                    "decision_id": decision.decision_id,
                }
            ],
        )

        record.signature = record.generate_signature(self.secret_key)
        self._certifications[record.id] = record
        return record

    def get_certification(self, certification_id: str) -> Optional[CertificationRecord]:
        return self._certifications.get(certification_id)

    def verify_certification_validity(self, certification_id: str) -> bool:
        record = self._certifications.get(certification_id)
        if not record:
            return False

        # 1. Check signature integrity
        if not record.verify_integrity(self.secret_key):
            return False

        # 2. Check status
        if record.status not in (CertificationStatus.ACTIVE, CertificationStatus.PROVISIONAL):
            return False

        # 3. Check expiration
        now_dt = datetime.now(timezone.utc)
        expires_dt = datetime.fromisoformat(record.expires_at)
        if now_dt > expires_dt:
            record.status = CertificationStatus.EXPIRED
            return False

        return True

    def revoke_certification(self, certification_id: str, reason: str, revoked_by: str) -> CertificationRecord:
        record = self._certifications.get(certification_id)
        if not record:
            raise KeyError(f"Certification '{certification_id}' not found.")

        record.status = CertificationStatus.REVOKED
        now_str = datetime.now(timezone.utc).isoformat()
        record.audit_trail.append(
            {
                "action": "CertificationRevoked",
                "actor": revoked_by,
                "timestamp": now_str,
                "reason": reason,
            }
        )
        record.signature = record.generate_signature(self.secret_key)
        return record

    def list_certifications(self, system_id: Optional[str] = None) -> List[CertificationRecord]:
        if system_id:
            return [c for c in self._certifications.values() if c.system_id == system_id]
        return list(self._certifications.values())
