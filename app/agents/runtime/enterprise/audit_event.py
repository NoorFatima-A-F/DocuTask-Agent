"""
Runtime Audit Event Model.
Immutable audit record tracking security events, configuration modifications, plugin actions, and tenant operations.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class AuditEventType(str, Enum):
    """Categorization of audit events."""
    RUNTIME_LIFECYCLE = "RUNTIME_LIFECYCLE"
    PLUGIN_MODIFICATION = "PLUGIN_MODIFICATION"
    TENANT_ACTION = "TENANT_ACTION"
    CONFIGURATION_CHANGE = "CONFIGURATION_CHANGE"
    SECURITY_VIOLATION = "SECURITY_VIOLATION"


class RuntimeAuditEvent(BaseModel):
    """An individual immutable audit event with cryptographic hash chaining support."""
    event_id: UUID = Field(default_factory=uuid4)
    event_type: AuditEventType
    actor: str
    tenant_id: str = "default"
    details: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    prev_hash: Optional[str] = None
    event_hash: Optional[str] = None

    model_config = {"frozen": True}
