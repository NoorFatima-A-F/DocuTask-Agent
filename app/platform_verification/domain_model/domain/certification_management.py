"""
Certification Domain: 5 Certification Levels, Digital Sealing, and Expiration Lifecycles.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
import uuid


class CertificationLevel(str, Enum):
    ENTERPRISE_CERTIFIED = "ENTERPRISE_CERTIFIED"  # Highest (Zero defect, 99.99% fidelity)
    PRODUCTION_READY = "PRODUCTION_READY"          # Production compliant
    CONDITIONALLY_READY = "CONDITIONALLY_READY"    # Canary / Controlled rollout
    DEVELOPMENT_QUALITY = "DEVELOPMENT_QUALITY"    # Non-production build
    REJECTED = "REJECTED"                          # Hard failure


class Certification(BaseModel):
    certification_id: str = Field(default_factory=lambda: f"cert_{uuid.uuid4().hex[:8]}")
    execution_id: str
    verification_definition_id: str
    level: CertificationLevel
    composite_quality_score: float
    evidence_bundle_hash: str
    approved_by: str = "Enterprise Certification Authority"
    is_active: bool = True
    issued_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expiration_date: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    revocation_reason: Optional[str] = None

    def revoke(self, reason: str) -> None:
        self.is_active = False
        self.revocation_reason = reason
