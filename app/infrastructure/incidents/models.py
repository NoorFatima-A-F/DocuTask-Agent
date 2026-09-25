"""
Incident Domain Models & Enums.

Defines Incident entities, 6 severity levels (INFO, WARNING, MINOR, MAJOR, CRITICAL, CATASTROPHIC),
7 lifecycle states, and timeline audit logs.
"""

from __future__ import annotations

import enum
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.reliability.models import SeverityLevel


class IncidentStatus(str, enum.Enum):
    """Seven-stage incident lifecycle status."""
    DETECTED = "DETECTED"
    INVESTIGATING = "INVESTIGATING"
    IDENTIFIED = "IDENTIFIED"
    MITIGATING = "MITIGATING"
    RESOLVED = "RESOLVED"
    POSTMORTEM = "POSTMORTEM"
    CLOSED = "CLOSED"


class IncidentTimelineEntry(BaseModel):
    """Timestamped log entry within an incident timeline."""
    entry_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actor: str = "system"
    message: str
    status_change: Optional[IncidentStatus] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Incident(BaseModel):
    """First-class enterprise incident entity."""
    incident_id: str
    title: str
    severity: SeverityLevel
    status: IncidentStatus = IncidentStatus.DETECTED
    impacted_components: List[str] = Field(default_factory=list)
    impacted_tenants: List[str] = Field(default_factory=list)
    lead_responder: Optional[str] = None
    root_cause: Optional[str] = None
    mitigation_notes: Optional[str] = None
    timeline: List[IncidentTimelineEntry] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
