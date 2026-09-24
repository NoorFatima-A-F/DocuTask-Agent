"""Enterprise SaaS Developer SDK & Client Interface (ESP-MOOS)."""

from __future__ import annotations

from typing import Any, Dict, Optional
from app.tenancy.core.models import (
    Organization,
    Workspace,
    SubscriptionTier,
    Region,
    MembershipRole,
)
from app.tenancy.organizations.manager import OrganizationManager
from app.tenancy.workspaces.manager import WorkspaceManager
from app.tenancy.teams.membership_manager import MembershipManager
from app.tenancy.teams.invitation_manager import InvitationManager
from app.tenancy.provisioning.engine import TenantProvisioningEngine
from app.tenancy.policies.engine import TenantPolicyEngine, TenantPolicyRule
from app.tenancy.quotas.manager import QuotaManager
from app.tenancy.metering.engine import UsageMeteringPlatform
from app.tenancy.subscriptions.engine import SubscriptionEngine
from app.tenancy.entitlements.service import FeatureEntitlementService
from app.tenancy.migration.engine import TenantMigrationEngine
from app.tenancy.backup.engine import TenantBackupRestoreEngine


class SaaSSDK:
    """Unified SaaS Platform Client SDK."""

    def __init__(
        self,
        org_manager: Optional[OrganizationManager] = None,
        workspace_manager: Optional[WorkspaceManager] = None,
        membership_manager: Optional[MembershipManager] = None,
        invitation_manager: Optional[InvitationManager] = None,
        provisioning_engine: Optional[TenantProvisioningEngine] = None,
        policy_engine: Optional[TenantPolicyEngine] = None,
        quota_manager: Optional[QuotaManager] = None,
        metering_platform: Optional[UsageMeteringPlatform] = None,
        subscription_engine: Optional[SubscriptionEngine] = None,
        entitlement_service: Optional[FeatureEntitlementService] = None,
        migration_engine: Optional[TenantMigrationEngine] = None,
        backup_engine: Optional[TenantBackupRestoreEngine] = None,
    ):
        self.orgs = org_manager or OrganizationManager()
        self.workspaces = workspace_manager or WorkspaceManager()
        self.memberships = membership_manager or MembershipManager()
        self.invitations = invitation_manager or InvitationManager()
        self.policies = policy_engine or TenantPolicyEngine()
        self.quotas = quota_manager or QuotaManager()
        self.metering = metering_platform or UsageMeteringPlatform()
        self.subscriptions = subscription_engine or SubscriptionEngine()
        self.entitlements = entitlement_service or FeatureEntitlementService(self.subscriptions)
        self.backups = backup_engine or TenantBackupRestoreEngine()
        self.migrations = migration_engine or TenantMigrationEngine(self.orgs, self.backups)

    def create_organization(
        self,
        org_id: str,
        name: str,
        owner_id: str,
        region: Region = Region.US_EAST,
        subscription_plan: SubscriptionTier = SubscriptionTier.FREE,
    ) -> Organization:
        """Create a new organization."""
        return self.orgs.create_organization(
            org_id=org_id,
            name=name,
            owner_id=owner_id,
            region=region,
            subscription_plan=subscription_plan,
        )

    def create_workspace(
        self,
        workspace_id: str,
        organization_id: str,
        name: str,
        department: str = "General",
    ) -> Workspace:
        """Create a new workspace."""
        return self.workspaces.create_workspace(
            workspace_id=workspace_id,
            organization_id=organization_id,
            name=name,
            department=department,
        )

    def invite_user(
        self,
        email: str,
        organization_id: str,
        inviter_user_id: str,
        workspace_id: Optional[str] = None,
        role: MembershipRole = MembershipRole.MEMBER,
    ) -> str:
        """Create and return invitation token."""
        inv = self.invitations.create_invitation(
            invitation_id=f"inv_{email.split('@')[0]}",
            email=email,
            organization_id=organization_id,
            inviter_user_id=inviter_user_id,
            workspace_id=workspace_id,
            role=role,
        )
        return inv.token

    def assign_role(
        self,
        user_id: str,
        organization_id: str,
        role: MembershipRole,
        workspace_id: Optional[str] = None,
    ):
        """Assign role to user."""
        return self.memberships.assign_membership(
            membership_id=f"mem_{user_id}_{organization_id}",
            user_id=user_id,
            organization_id=organization_id,
            workspace_id=workspace_id,
            role=role,
        )

    def configure_policy(self, organization_id: str, policy: TenantPolicyRule) -> None:
        """Set tenant policy."""
        self.policies.set_policy(organization_id, policy)

    def export_tenant(self, organization_id: str) -> Dict[str, Any]:
        """Export tenant snapshot."""
        return self.migrations.export_tenant(organization_id)

    def restore_tenant(self, snapshot_id: str) -> Dict[str, Any]:
        """Restore tenant from backup snapshot."""
        return self.backups.restore_snapshot(snapshot_id)
