from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Dict
import hashlib
import hmac
import uuid

@dataclass(frozen=True)
class VerificationCertificate:
    certificate_id: str
    specification_id: str
    execution_id: str
    target_subsystem: str
    target_version: str
    digital_signature: str
    issued_at: str
    expires_at: str
    is_revoked: bool = False
    certification_level: str = "ENTERPRISE_CERTIFIED"

class CertificationAuthorityWorkflow:
    def __init__(self, signing_secret: str = "cert_secret_key_123"):
        self._secret = signing_secret
        self._issued_certificates: Dict[str, VerificationCertificate] = {}

    def issue_certificate(
        self,
        specification_id: str,
        execution_id: str,
        target_subsystem: str,
        target_version: str,
        level: str = "ENTERPRISE_CERTIFIED",
        valid_days: int = 90
    ) -> VerificationCertificate:
        cert_id = f"cert_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc)
        issued_at = now.isoformat()
        expires_at = (now + timedelta(days=valid_days)).isoformat()

        payload = f"{cert_id}:{specification_id}:{execution_id}:{target_subsystem}:{target_version}:{level}:{issued_at}"
        signature = hmac.new(self._secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()

        cert = VerificationCertificate(
            certificate_id=cert_id,
            specification_id=specification_id,
            execution_id=execution_id,
            target_subsystem=target_subsystem,
            target_version=target_version,
            digital_signature=signature,
            issued_at=issued_at,
            expires_at=expires_at,
            certification_level=level
        )
        self._issued_certificates[cert_id] = cert
        return cert

    def verify_certificate(self, cert: VerificationCertificate) -> bool:
        if cert.is_revoked:
            return False
        payload = f"{cert.certificate_id}:{cert.specification_id}:{cert.execution_id}:{cert.target_subsystem}:{cert.target_version}:{cert.certification_level}:{cert.issued_at}"
        expected = hmac.new(self._secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, cert.digital_signature)
