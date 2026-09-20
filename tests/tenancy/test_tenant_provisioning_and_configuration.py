"""Test Tenant Automated Provisioning & Configuration Precedence."""

import pytest
from app.tenancy.core.models import (
    TenantLifecycleState,
    SubscriptionTier,
    ComplianceProfileType,
    Region,
)
from app.tenancy.organizations.manager import OrganizationManager
from app.tenancy.workspaces.manager import WorkspaceManager
from app.tenancy.environments.manager import EnvironmentManager
from app.tenancy.teams.membership_manager import MembershipManager
from app.tenancy.provisioning.engine import TenantProvisioningEngine
from app.tenancy.configuration.hierarchy import ConfigurationHierarchyEngine


def test_automated_tenant_provisioning_workflow():
    """Verify complete end-to-end automated tenant onboarding."""
    org_mgr = OrganizationManager()
    ws_mgr = WorkspaceManager()
    env_mgr = EnvironmentManager()
    mem_mgr = MembershipManager()

    engine = TenantProvisioningEngine(
        org_manager=org_mgr,
        workspace_manager=ws_mgr,
        environment_manager=env_mgr,
        membership_manager=mem_mgr,
    )

    result = engine.provision_tenant(
        organization_name="Globex Corporation",
        owner_user_id="user_globex_owner",
        industry="Manufacturing",
        region=Region.EU_CENTRAL,
        subscription_plan=SubscriptionTier.BUSINESS,
        compliance_profile=ComplianceProfileType.ISO27001,
    )

    assert result.is_success is True
    assert result.organization.status == TenantLifecycleState.ACTIVE
    assert result.organization.subscription_plan == SubscriptionTier.BUSINESS
    assert result.default_workspace.name == "Default Workspace"
    assert result.default_environment.name == "Production"
    assert len(result.provisioning_steps_completed) == 6


def test_configuration_6_tier_hierarchy():
    """Verify configuration hierarchy precedence."""
    engine = ConfigurationHierarchyEngine(
        platform_defaults={"model": "gemini-flash", "temperature": 0.2, "timeout": 30}
    )

    # Org overrides temperature
    org_conf = {"temperature": 0.5}
    # Workspace overrides model
    ws_conf = {"model": "gemini-pro"}
    # Env overrides timeout
    env_conf = {"timeout": 120}
    # Execution overrides temperature
    exec_conf = {"temperature": 0.9}

    resolved = engine.resolve(
        org_config=org_conf,
        workspace_config=ws_conf,
        environment_config=env_conf,
        execution_config=exec_conf,
    )

    assert resolved["model"] == "gemini-pro"
    assert resolved["temperature"] == 0.9
    assert resolved["timeout"] == 120
