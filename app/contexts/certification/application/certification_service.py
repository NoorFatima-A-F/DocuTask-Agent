from typing import Dict, Any, Optional
import hashlib
import json
from ..domain.certification_domain import ComplianceCertificateAggregate, CertificateIssued
from app.shared_kernel import Result, Ok, get_event_bus

class CertificationService:
    def __init__(self, repo):
        self.repo = repo

    async def issue_certificate(self, cert_id: str, run_id: str, level: str = "PRODUCTION_READY", metadata: Optional[Dict[str, Any]] = None) -> Result[ComplianceCertificateAggregate, str]:
        sig_data = f"{cert_id}:{run_id}:{level}:{json.dumps(metadata or {}, sort_keys=True)}"
        sig = hashlib.sha256(sig_data.encode("utf-8")).hexdigest()
        agg = ComplianceCertificateAggregate(id=cert_id, run_id=run_id, level=level, status="ACTIVE", digital_signature_hash=sig)
        self.repo.save(agg)
        await get_event_bus().publish(CertificateIssued(certificate_id=cert_id, level=level))
        return Ok(agg)
