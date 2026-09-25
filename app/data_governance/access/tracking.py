"""Data Access Tracking Platform (Phase 8B).

Maintains immutable audit records for every data read, transformation, export, or deletion.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DataActionType(str, enum.Enum):
    """Governed actions performed against data assets."""
    READ = "READ"
    WRITE = "WRITE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    EXPORT = "EXPORT"
    SHARE = "SHARE"
    PROCESS = "PROCESS"


class DataAccessEvent(BaseModel):
    """Immutable record of an access or processing event."""
    event_id: str
    asset_id: str
    organization_id: str
    user_id: str
    action: DataActionType
    purpose: str = "Operational Task"
    workflow_id: Optional[str] = None
    agent_id: Optional[str] = None
    connector_id: Optional[str] = None
    decision_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DataAccessTracker:
    """Records and queries data access events for compliance audits."""

    def __init__(self):
        self._events: List[DataAccessEvent] = []

    def record_access(
        self,
        asset_id: str,
        organization_id: str,
        user_id: str,
        action: DataActionType,
        purpose: str = "Operational Task",
        workflow_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        connector_id: Optional[str] = None,
        decision_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> DataAccessEvent:
        """Log a data access event."""
        event = DataAccessEvent(
            event_id=f"acc_{uuid.uuid4().hex[:12]}",
            asset_id=asset_id,
            organization_id=organization_id,
            user_id=user_id,
            action=action,
            purpose=purpose,
            workflow_id=workflow_id,
            agent_id=agent_id,
            connector_id=connector_id,
            decision_id=decision_id,
            metadata=metadata or {},
        )
        self._events.append(event)
        return event

    def get_asset_access_history(self, asset_id: str) -> List[DataAccessEvent]:
        """Get chronological access history for an asset."""
        return [e for e in self._events if e.asset_id == asset_id]

    def get_organization_access_history(self, organization_id: str) -> List[DataAccessEvent]:
        """Get all access events for an organization."""
        return [e for e in self._events if e.organization_id == organization_id]
