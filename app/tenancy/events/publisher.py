"""SaaS Multi-Tenancy Event Publisher (ESP-MOOS).

Emits structured events:
- OrganizationCreated
- WorkspaceCreated
- SubscriptionChanged
- QuotaExceeded
- TenantSuspended
- TenantRestored
- PolicyChanged
- CustomDomainVerified
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SaaSEvent(BaseModel):
    """Canonical SaaS lifecycle event."""
    event_type: str
    organization_id: str
    workspace_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SaaSEventPublisher:
    """Emits tenant lifecycle events to platform subscribers."""

    def __init__(self):
        self._emitted_events: List[SaaSEvent] = []

    def publish(
        self,
        event_type: str,
        organization_id: str,
        workspace_id: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> SaaSEvent:
        """Publish a tenant event."""
        event = SaaSEvent(
            event_type=event_type,
            organization_id=organization_id,
            workspace_id=workspace_id,
            payload=payload or {},
        )
        self._emitted_events.append(event)
        return event

    def get_events(self, organization_id: Optional[str] = None) -> List[SaaSEvent]:
        """Retrieve emitted event log."""
        if organization_id:
            return [e for e in self._emitted_events if e.organization_id == organization_id]
        return list(self._emitted_events)
