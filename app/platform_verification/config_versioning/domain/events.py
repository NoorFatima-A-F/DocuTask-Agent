"""
Domain Events for Configuration, Versioning & Dependency Management.
"""
from dataclasses import dataclass
from app.platform_verification.shared_kernel.events import DomainEvent

@dataclass(frozen=True)
class ConfigurationSnapshotCreatedEvent(DomainEvent):
    event_name: str = "ConfigurationSnapshotCreated"


@dataclass(frozen=True)
class ConfigurationDriftDetectedEvent(DomainEvent):
    event_name: str = "ConfigurationDriftDetected"


@dataclass(frozen=True)
class ChangeRequestApprovedEvent(DomainEvent):
    event_name: str = "ChangeRequestApproved"


@dataclass(frozen=True)
class RollbackExecutedEvent(DomainEvent):
    event_name: str = "RollbackExecuted"


@dataclass(frozen=True)
class SBOMGeneratedEvent(DomainEvent):
    event_name: str = "SBOMGenerated"
