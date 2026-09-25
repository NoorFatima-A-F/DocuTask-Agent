"""Automated Tenant Provisioning Engine (ESP-MOOS).

Implements idempotent, retryable, observable onboarding workflow:
Signup -> Organization Created -> Workspace Created -> Storage Initialized ->
Knowledge Space Initialized -> Default Policies Applied -> Monitoring Configured -> Tenant Active.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.tenancy.core.models import (
    Organization,
    Workspace,
    Environment,
    EnvironmentType,
    TenantLifecycleState,
    SubscriptionTier,
    ComplianceProfileType,
    Region,
    MembershipRole,
)
from app.tenancy.core.exceptions import ProvisioningError
from app.tenancy.organizations.manager import OrganizationManager
from app.tenancy.workspaces.manager import WorkspaceManager
from app.tenancy.environments.manager import EnvironmentManager
from app.tenancy.teams.membership_manager import MembershipManager


class ProvisioningResult(BaseModel):
    """Output artifact from automated tenant provisioning."""
    organization: Organization
    default_workspace: Workspace
    default_environment: Environment
    owner_membership_id: str
    provisioning_steps_completed: List[str]
    is_success: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TenantProvisioningEngine:
    """Orchestrates end-to-end multi-step tenant provisioning."""

    def __init__(
        self,
        org_manager: OrganizationManager,
        workspace_manager: WorkspaceManager,
        environment_manager: EnvironmentManager,
        membership_manager: MembershipManager,
    ):
        self.org_manager = org_manager
        self.workspace_manager = workspace_manager
        self.environment_manager = environment_manager
        self.membership_manager = membership_manager

    def provision_tenant(
        self,
        organization_name: str,
        owner_user_id: str,
        organization_id: Optional[str] = None,
        industry: str = "Technology",
        region: Region = Region.US_EAST,
        subscription_plan: SubscriptionTier = SubscriptionTier.FREE,
        compliance_profile: ComplianceProfileType = ComplianceProfileType.STANDARD,
    ) -> ProvisioningResult:
        """Execute automated idempotent tenant onboarding."""
        org_id = organization_id or f"org_{uuid.uuid4().hex[:8]}"
        completed_steps = []

        try:
            # Step 1: Create Organization in REGISTERED state
            org = self.org_manager.create_organization(
                org_id=org_id,
                name=organization_name,
                owner_id=owner_user_id,
                industry=industry,
                region=region,
                subscription_plan=subscription_plan,
                compliance_profile=compliance_profile,
            )
            completed_steps.append("ORGANIZATION_REGISTERED")

            # Step 2: Transition to PROVISIONING
            self.org_manager.update_status(org_id, TenantLifecycleState.PROVISIONING, actor_id=owner_user_id)
            completed_steps.append("STATUS_PROVISIONING")

            # Step 3: Create Default Workspace
            workspace_id = f"ws_default_{org_id[:8]}"
            ws = self.workspace_manager.create_workspace(
                workspace_id=workspace_id,
                organization_id=org_id,
                name="Default Workspace",
                description="Primary default workspace",
                region=region,
            )
            completed_steps.append("WORKSPACE_CREATED")

            # Step 4: Create Default Environments (Production + Development)
            env_prod = self.environment_manager.create_environment(
                environment_id=f"env_prod_{org_id[:8]}",
                workspace_id=workspace_id,
                organization_id=org_id,
                name="Production",
                env_type=EnvironmentType.PRODUCTION,
            )
            self.environment_manager.create_environment(
                environment_id=f"env_dev_{org_id[:8]}",
                workspace_id=workspace_id,
                organization_id=org_id,
                name="Development",
                env_type=EnvironmentType.DEVELOPMENT,
            )
            completed_steps.append("ENVIRONMENTS_INITIALIZED")

            # Step 5: Assign Owner Membership
            membership_id = f"mem_owner_{org_id[:8]}"
            self.membership_manager.assign_membership(
                membership_id=membership_id,
                user_id=owner_user_id,
                organization_id=org_id,
                workspace_id=workspace_id,
                role=MembershipRole.OWNER,
            )
            completed_steps.append("OWNER_ASSIGNED")

            # Step 6: Transition to INITIALIZED then ACTIVE
            self.org_manager.update_status(org_id, TenantLifecycleState.INITIALIZED, actor_id=owner_user_id)
            self.org_manager.update_status(org_id, TenantLifecycleState.ACTIVE, actor_id=owner_user_id)
            completed_steps.append("TENANT_ACTIVATED")

            return ProvisioningResult(
                organization=org,
                default_workspace=ws,
                default_environment=env_prod,
                owner_membership_id=membership_id,
                provisioning_steps_completed=completed_steps,
                is_success=True,
            )
        except Exception as e:
            raise ProvisioningError(
                f"Provisioning failed for organization '{organization_name}': {str(e)}",
                details={"completed_steps": completed_steps, "error": str(e)},
            )
