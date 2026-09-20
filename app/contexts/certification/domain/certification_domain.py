from dataclasses import dataclass
from typing import Dict, Any
from app.shared_kernel import BaseEntity, DomainEvent

@dataclass
class CertificateIssued(DomainEvent):
    certificate_id: str = ""
    level: str = "PRODUCTION_READY"

@dataclass
class ComplianceCertificateAggregate(BaseEntity):
    run_id: str = ""
    level: str = "PRODUCTION_READY"
    status: str = "ACTIVE"
    digital_signature_hash: str = ""
