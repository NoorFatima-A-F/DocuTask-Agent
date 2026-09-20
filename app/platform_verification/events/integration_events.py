"""
Cross-Subsystem Integration Events.
"""
from dataclasses import dataclass
from app.platform_verification.shared_kernel.events import IntegrationEvent

@dataclass(frozen=True)
class VerificationRunInitiatedIntegrationEvent(IntegrationEvent):
    event_name: str = "VerificationRunInitiated"


@dataclass(frozen=True)
class VerificationRunFinalizedIntegrationEvent(IntegrationEvent):
    event_name: str = "VerificationRunFinalized"
