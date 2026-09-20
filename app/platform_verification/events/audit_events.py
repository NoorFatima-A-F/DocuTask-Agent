"""
Cryptographic Audit Ledger Events.
"""
from dataclasses import dataclass
from app.platform_verification.shared_kernel.events import BaseEvent

@dataclass(frozen=True)
class AuditLogGeneratedEvent(BaseEvent):
    event_name: str = "AuditLogGenerated"
