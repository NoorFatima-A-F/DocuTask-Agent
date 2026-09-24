"""
Incident Domain Models.
Tracks operational incidents generated when automatic recovery escalates.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class IncidentSeverity(str, Enum):
    SEV1 = "SEV1_CRITICAL"
    SEV2 = "SEV2_MAJOR"
    SEV3 = "SEV3_MODERATE"
    SEV4 = "SEV4_LOW"


class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    MITIGATED = "MITIGATED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class Incident(BaseModel):
    """Operational incident aggregate representing an escalated unrecoverable fault."""
    incident_id: UUID = Field(default_factory=uuid4)
    execution_id: UUID
    failure_id: UUID
    title: str
    description: str
    severity: IncidentSeverity = Field(default=IncidentSeverity.SEV3)
    status: IncidentStatus = Field(default=IncidentStatus.OPEN)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None
    assignee: Optional[str] = None
    mitigation_notes: Optional[str] = None
    model_config = {"frozen": True}
