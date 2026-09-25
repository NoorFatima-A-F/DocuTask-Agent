"""Invitation Lifecycle Platform (ESP-MOOS).

Governs:
CREATED -> SENT -> ACCEPTED -> ACTIVE -> EXPIRED
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from app.tenancy.core.models import Invitation, InvitationState, MembershipRole
from app.tenancy.core.exceptions import TenancyError


class InvitationManager:
    """Manages secure member invitations and onboarding lifecycle."""

    def __init__(self):
        self._invitations: Dict[str, Invitation] = {}
        self._token_index: Dict[str, str] = {}

    def create_invitation(
        self,
        invitation_id: str,
        email: str,
        organization_id: str,
        inviter_user_id: str,
        workspace_id: Optional[str] = None,
        role: MembershipRole = MembershipRole.MEMBER,
        expires_in_days: int = 7,
    ) -> Invitation:
        """Create a new pending invitation."""
        token = str(uuid.uuid4()).replace("-", "")
        expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)

        inv = Invitation(
            invitation_id=invitation_id,
            email=email,
            organization_id=organization_id,
            workspace_id=workspace_id,
            role=role,
            inviter_user_id=inviter_user_id,
            status=InvitationState.CREATED,
            token=token,
            expires_at=expires_at,
        )
        self._invitations[invitation_id] = inv
        self._token_index[token] = invitation_id
        return inv

    def mark_sent(self, invitation_id: str) -> Invitation:
        """Mark invitation as dispatched to user."""
        inv = self._invitations.get(invitation_id)
        if not inv:
            raise TenancyError(f"Invitation '{invitation_id}' not found")
        inv.status = InvitationState.SENT
        return inv

    def accept_invitation(self, token: str) -> Invitation:
        """Accept invitation using secret token."""
        inv_id = self._token_index.get(token)
        if not inv_id:
            raise TenancyError("Invalid invitation token")

        inv = self._invitations[inv_id]
        if datetime.now(timezone.utc) > inv.expires_at:
            inv.status = InvitationState.EXPIRED
            raise TenancyError("Invitation has expired")

        if inv.status in (InvitationState.EXPIRED, InvitationState.ACTIVE):
            raise TenancyError(f"Cannot accept invitation in status {inv.status.value}")

        inv.status = InvitationState.ACCEPTED
        return inv

    def activate_invitation(self, invitation_id: str) -> Invitation:
        """Transition accepted invitation to active."""
        inv = self._invitations.get(invitation_id)
        if not inv or inv.status != InvitationState.ACCEPTED:
            raise TenancyError(f"Cannot activate invitation in current state")
        inv.status = InvitationState.ACTIVE
        return inv

    def list_invitations(self, organization_id: str) -> List[Invitation]:
        """List all invitations for an organization."""
        return [i for i in self._invitations.values() if i.organization_id == organization_id]
