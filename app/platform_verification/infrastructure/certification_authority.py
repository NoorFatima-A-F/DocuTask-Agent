"""
HMAC-SHA256 Cryptographic Certification Authority
"""
import hmac
import hashlib
from typing import Dict, Optional
from datetime import datetime, timezone
from app.platform_verification.domain.models import VerificationRun, CryptographicCertificate
from app.platform_verification.domain.interfaces import CertificationAuthorityInterface

class CryptographicCertificationAuthority(CertificationAuthorityInterface):
    def __init__(self, secret_key: str = "DocuTask-Enterprise-Root-Key-2026-Immutable"):
        self._secret_key = secret_key.encode("utf-8")
        self._certificates: Dict[str, CryptographicCertificate] = {}

    def issue_certificate(self, run: VerificationRun) -> CryptographicCertificate:
        payload = f"{run.id}:{run.tenant_id}:{run.status.value}:{run.overall_score}:{datetime.now(timezone.utc).date().isoformat()}"
        signature = hmac.new(self._secret_key, payload.encode("utf-8"), hashlib.sha256).hexdigest()

        cert = CryptographicCertificate(
            verification_run_id=run.id,
            tenant_id=run.tenant_id,
            status=run.status,
            score=run.overall_score,
            hmac_sha256_signature=signature,
            is_valid=(run.status.value == "PASSED")
        )
        self._certificates[cert.certificate_id] = cert
        return cert

    def verify_certificate(self, certificate: CryptographicCertificate) -> bool:
        issued_date_str = certificate.issued_at.date().isoformat() if hasattr(certificate.issued_at, "date") else str(certificate.issued_at)[:10]
        run_identifier = certificate.verification_run_id or certificate.run_id
        score_val = certificate.overall_score if certificate.overall_score is not None else certificate.score
        payload = f"{run_identifier}:{certificate.tenant_id}:{certificate.status.value}:{score_val}:{issued_date_str}"
        expected_sig = hmac.new(self._secret_key, payload.encode("utf-8"), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_sig, certificate.hmac_sha256_signature)

certification_authority = CryptographicCertificationAuthority()
