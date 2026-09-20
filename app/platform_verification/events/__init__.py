"""
Unified Event Architecture for Enterprise Verification Platform.
"""
from app.platform_verification.events.bus import EnterpriseEventBus, verification_event_bus
from app.platform_verification.events.domain_events import (
    VerificationStartedDomainEvent, VerificationCompletedDomainEvent,
    EvidenceSealedDomainEvent, QualityGateEvaluatedDomainEvent,
    CertificateIssuedDomainEvent, InvariantFailedDomainEvent
)
from app.platform_verification.events.integration_events import (
    VerificationRunInitiatedIntegrationEvent, VerificationRunFinalizedIntegrationEvent
)
from app.platform_verification.events.audit_events import AuditLogGeneratedEvent

__all__ = [
    "EnterpriseEventBus", "verification_event_bus",
    "VerificationStartedDomainEvent", "VerificationCompletedDomainEvent",
    "EvidenceSealedDomainEvent", "QualityGateEvaluatedDomainEvent",
    "CertificateIssuedDomainEvent", "InvariantFailedDomainEvent",
    "VerificationRunInitiatedIntegrationEvent", "VerificationRunFinalizedIntegrationEvent",
    "AuditLogGeneratedEvent"
]
