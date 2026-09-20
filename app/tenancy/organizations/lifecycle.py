"""Organization 7-State Lifecycle State Machine (ESP-MOOS).

Governs:
REGISTERED -> PROVISIONING -> INITIALIZED -> ACTIVE -> SUSPENDED -> ARCHIVED -> DELETED
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field
from app.tenancy.core.models import TenantLifecycleState, Organization
from app.tenancy.core.exceptions import InvalidTenantStateError


class LifecycleAuditEvent(BaseModel):
    """Audit log entry for organization lifecycle transitions."""
    organization_id: str
    from_state: TenantLifecycleState
    to_state: TenantLifecycleState
    reason: str
    actor_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, str] = Field(default_factory=dict)


class OrganizationLifecycleManager:
    """Manages the 7-state lifecycle finite state machine for organizations."""

    # Explicit allowed transitions
    VALID_TRANSITIONS: Dict[TenantLifecycleState, Set[TenantLifecycleState]] = {
        TenantLifecycleState.REGISTERED: {TenantLifecycleState.PROVISIONING, TenantLifecycleState.DELETED},
        TenantLifecycleState.PROVISIONING: {TenantLifecycleState.INITIALIZED, TenantLifecycleState.REGISTERED, TenantLifecycleState.DELETED},
        TenantLifecycleState.INITIALIZED: {TenantLifecycleState.ACTIVE, TenantLifecycleState.SUSPENDED, TenantLifecycleState.DELETED},
        TenantLifecycleState.ACTIVE: {TenantLifecycleState.SUSPENDED, TenantLifecycleState.ARCHIVED, TenantLifecycleState.DELETED},
        TenantLifecycleState.SUSPENDED: {TenantLifecycleState.ACTIVE, TenantLifecycleState.ARCHIVED, TenantLifecycleState.DELETED},
        TenantLifecycleState.ARCHIVED: {TenantLifecycleState.ACTIVE, TenantLifecycleState.DELETED},
        TenantLifecycleState.DELETED: set(),  # Terminal state
    }

    def __init__(self):
        self._audit_log: List[LifecycleAuditEvent] = []

    def can_transition(self, current: TenantLifecycleState, target: TenantLifecycleState) -> bool:
        """Check if transition from current to target state is valid."""
        return target in self.VALID_TRANSITIONS.get(current, set())

    def transition(
        self,
        org: Organization,
        target_state: TenantLifecycleState,
        actor_id: str = "system",
        reason: str = "Automated state transition",
        metadata: Optional[Dict[str, str]] = None,
    ) -> Organization:
        """Execute a state transition with validation and audit trail logging."""
        if not self.can_transition(org.status, target_state):
            raise InvalidTenantStateError(
                f"Cannot transition organization '{org.id}' from state '{org.status.value}' to '{target_state.value}'"
            )

        audit_entry = LifecycleAuditEvent(
            organization_id=org.id,
            from_state=org.status,
            to_state=target_state,
            reason=reason,
            actor_id=actor_id,
            metadata=metadata or {},
        )
        self._audit_log.append(audit_entry)

        org.status = target_state
        org.updated_at = datetime.now(timezone.utc)
        return org

    def get_audit_trail(self, organization_id: str) -> List[LifecycleAuditEvent]:
        """Retrieve audit history for a specific organization."""
        return [e for e in self._audit_log if e.organization_id == organization_id]
