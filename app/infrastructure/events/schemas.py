"""Infrastructure Event Schemas and Audit Event Models."""

from datetime import datetime, timezone
import secrets
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class InfrastructureEventType(str):
    INFRASTRUCTURE_CREATED = "InfrastructureCreated"
    RESOURCE_ALLOCATED = "ResourceAllocated"
    SERVICE_STARTED = "ServiceStarted"
    SERVICE_STOPPED = "ServiceStopped"
    SERVICE_FAILED = "ServiceFailed"
    DEPLOYMENT_STARTED = "DeploymentStarted"
    DEPLOYMENT_COMPLETED = "DeploymentCompleted"
    HEALTH_CHANGED = "HealthChanged"
    RECOVERY_TRIGGERED = "RecoveryTriggered"


class InfrastructureEvent(BaseModel):
    """Canonical event emitted by the infrastructure runtime."""

    event_id: str = Field(default_factory=lambda: f"infevt_{secrets.token_hex(8)}")
    event_type: str
    service_name: Optional[str] = None
    resource_id: Optional[str] = None
    environment: str = "PRODUCTION"
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InfrastructureAuditEvent(BaseModel):
    """Compliance and security audit event for infrastructure actions."""

    audit_id: str = Field(default_factory=lambda: f"infaud_{secrets.token_hex(8)}")
    actor: str
    action: str
    resource: str
    environment: str
    result: str = "SUCCESS"  # SUCCESS or FAILURE
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
