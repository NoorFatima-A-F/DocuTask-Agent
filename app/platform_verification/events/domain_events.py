"""
Versioned Domain Events.
"""
from dataclasses import dataclass
from app.platform_verification.shared_kernel.events import DomainEvent

@dataclass(frozen=True)
class VerificationStartedDomainEvent(DomainEvent):
    event_name: str = "VerificationStarted"


@dataclass(frozen=True)
class VerificationCompletedDomainEvent(DomainEvent):
    event_name: str = "VerificationCompleted"


@dataclass(frozen=True)
class EvidenceSealedDomainEvent(DomainEvent):
    event_name: str = "EvidenceSealed"


@dataclass(frozen=True)
class QualityGateEvaluatedDomainEvent(DomainEvent):
    event_name: str = "QualityGateEvaluated"


@dataclass(frozen=True)
class CertificateIssuedDomainEvent(DomainEvent):
    event_name: str = "CertificateIssued"


@dataclass(frozen=True)
class InvariantFailedDomainEvent(DomainEvent):
    event_name: str = "InvariantFailed"
