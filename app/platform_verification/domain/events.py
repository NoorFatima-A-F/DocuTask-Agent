"""
Verification Domain Events Catalog
"""
from __future__ import annotations
from typing import Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid

class VerificationDomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"vevt-{uuid.uuid4().hex[:12]}")
    event_type: str
    tenant_id: str = "default-tenant"
    run_id: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class VerificationCreatedEvent(VerificationDomainEvent):
    event_type: str = "VERIFICATION_CREATED"

class VerificationStartedEvent(VerificationDomainEvent):
    event_type: str = "VERIFICATION_STARTED"

class StageCompletedEvent(VerificationDomainEvent):
    event_type: str = "STAGE_COMPLETED"

class EvidenceSealedEvent(VerificationDomainEvent):
    event_type: str = "EVIDENCE_SEALED"

class MetricsCalculatedEvent(VerificationDomainEvent):
    event_type: str = "METRICS_CALCULATED"

class QualityGateEvaluatedEvent(VerificationDomainEvent):
    event_type: str = "QUALITY_GATE_EVALUATED"

class CertificationIssuedEvent(VerificationDomainEvent):
    event_type: str = "CERTIFICATION_ISSUED"

class VerificationCompletedEvent(VerificationDomainEvent):
    event_type: str = "VERIFICATION_COMPLETED"
