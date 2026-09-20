"""Membership & RBAC Authorization Manager (ESP-MOOS)."""

from __future__ import annotations

from typing import Dict, List, Optional, Set
from app.tenancy.core.models import Membership, MembershipRole
from app.tenancy.core.exceptions import TenancyError


class MembershipManager:
    """Manages user memberships, roles, and fine-grained permissions."""

    # Default role permission mappings
    ROLE_PERMISSIONS: Dict[MembershipRole, Set[str]] = {
        MembershipRole.OWNER: {"*"},
        MembershipRole.ADMIN: {
            "workspace:read", "workspace:write", "workspace:delete",
            "workflow:read", "workflow:write", "workflow:execute",
            "agent:read", "agent:write", "agent:execute",
            "knowledge:read", "knowledge:write",
            "connector:read", "connector:write",
            "user:invite", "user:manage", "billing:read",
        },
        MembershipRole.MEMBER: {
            "workspace:read",
            "workflow:read", "workflow:write", "workflow:execute",
            "agent:read", "agent:write", "agent:execute",
            "knowledge:read", "knowledge:write",
            "connector:read",
        },
        MembershipRole.VIEWER: {
            "workspace:read", "workflow:read", "agent:read",
            "knowledge:read", "connector:read",
        },
        MembershipRole.GUEST: {
            "workspace:read", "workflow:execute",
        },
        MembershipRole.AUDITOR: {
            "workspace:read", "audit:read", "compliance:read", "logs:read",
        },
    }

    def __init__(self):
        self._memberships: Dict[str, Membership] = {}

    def assign_membership(
        self,
        membership_id: str,
        user_id: str,
        organization_id: str,
        workspace_id: Optional[str] = None,
        role: MembershipRole = MembershipRole.MEMBER,
        custom_permissions: Optional[Set[str]] = None,
    ) -> Membership:
        """Assign role and permissions to a user within an org or workspace."""
        base_perms = set(self.ROLE_PERMISSIONS.get(role, set()))
        if custom_permissions:
            base_perms.update(custom_permissions)

        membership = Membership(
            membership_id=membership_id,
            user_id=user_id,
            organization_id=organization_id,
            workspace_id=workspace_id,
            role=role,
            permissions=base_perms,
        )
        self._memberships[membership_id] = membership
        return membership

    def get_membership(self, user_id: str, organization_id: str, workspace_id: Optional[str] = None) -> Optional[Membership]:
        """Find active membership for user in specific context."""
        for m in self._memberships.values():
            if m.user_id == user_id and m.organization_id == organization_id:
                if workspace_id is None or m.workspace_id == workspace_id or m.workspace_id is None:
                    return m
        return None

    def has_permission(
        self,
        user_id: str,
        organization_id: str,
        permission: str,
        workspace_id: Optional[str] = None,
    ) -> bool:
        """Check if user holds required permission."""
        membership = self.get_membership(user_id, organization_id, workspace_id)
        if not membership:
            return False
        if "*" in membership.permissions:
            return True
        return permission in membership.permissions

    def list_members(self, organization_id: str, workspace_id: Optional[str] = None) -> List[Membership]:
        """List members for an organization or workspace."""
        return [
            m for m in self._memberships.values()
            if m.organization_id == organization_id and (workspace_id is None or m.workspace_id == workspace_id)
        ]
