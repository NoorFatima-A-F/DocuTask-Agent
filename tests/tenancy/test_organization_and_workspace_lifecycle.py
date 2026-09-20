"""Test Organization & Workspace Lifecycle Management."""

import pytest
from app.tenancy.core.models import TenantLifecycleState, EnvironmentType, Region
from app.tenancy.core.exceptions import InvalidTenantStateError, WorkspaceNotFoundError, TenancyError
from app.tenancy.organizations.manager import OrganizationManager
from app.tenancy.organizations.lifecycle import OrganizationLifecycleManager
from app.tenancy.workspaces.manager import WorkspaceManager
from app.tenancy.environments.manager import EnvironmentManager
from app.tenancy.projects.manager import ProjectManager


def test_organization_7_state_lifecycle():
    """Verify 7-state Organization FSM transitions and audit trails."""
    lifecycle = OrganizationLifecycleManager()
    manager = OrganizationManager(lifecycle_manager=lifecycle)

    org = manager.create_organization(
        org_id="org_test_1",
        name="Acme Corp",
        owner_id="user_admin",
    )
    assert org.status == TenantLifecycleState.REGISTERED

    # Advance to PROVISIONING
    manager.update_status("org_test_1", TenantLifecycleState.PROVISIONING, actor_id="user_admin")
    assert org.status == TenantLifecycleState.PROVISIONING

    # Advance to INITIALIZED -> ACTIVE
    manager.update_status("org_test_1", TenantLifecycleState.INITIALIZED)
    manager.update_status("org_test_1", TenantLifecycleState.ACTIVE)
    assert org.status == TenantLifecycleState.ACTIVE

    # Suspend organization
    manager.update_status("org_test_1", TenantLifecycleState.SUSPENDED, reason="Billing overdue")
    assert org.status == TenantLifecycleState.SUSPENDED

    # Reactivate
    manager.update_status("org_test_1", TenantLifecycleState.ACTIVE, reason="Payment cleared")
    assert org.status == TenantLifecycleState.ACTIVE

    # Check audit log
    audit_trail = lifecycle.get_audit_trail("org_test_1")
    assert len(audit_trail) == 5
    assert audit_trail[-1].to_state == TenantLifecycleState.ACTIVE


def test_invalid_lifecycle_transition_rejected():
    """Verify illegal transitions are rejected."""
    manager = OrganizationManager()
    manager.create_organization(org_id="org_test_2", name="Beta Corp", owner_id="user_owner")

    # Cannot transition directly from REGISTERED to ACTIVE
    with pytest.raises(InvalidTenantStateError):
        manager.update_status("org_test_2", TenantLifecycleState.ACTIVE)


def test_workspace_and_environment_management():
    """Verify workspace boundaries and environment variable scoping."""
    ws_mgr = WorkspaceManager()
    env_mgr = EnvironmentManager()
    proj_mgr = ProjectManager()

    ws = ws_mgr.create_workspace(
        workspace_id="ws_fin_1",
        organization_id="org_test_1",
        name="Finance Workspace",
        department="Finance",
        region=Region.EU_WEST,
    )
    assert ws.department == "Finance"
    assert len(ws_mgr.list_workspaces("org_test_1")) == 1

    # Cross-tenant workspace retrieval check
    with pytest.raises(WorkspaceNotFoundError):
        ws_mgr.get_workspace("ws_fin_1", organization_id="org_different")

    # Create Environments
    env_prod = env_mgr.create_environment(
        environment_id="env_prod_1",
        workspace_id="ws_fin_1",
        organization_id="org_test_1",
        name="Production",
        env_type=EnvironmentType.PRODUCTION,
        variables={"API_URL": "https://api.acme.com"},
        secrets={"API_KEY": "vault://sec_prod_key"},
    )
    assert env_prod.variables["API_URL"] == "https://api.acme.com"

    # Create Project
    proj = proj_mgr.create_project(
        project_id="proj_inv_1",
        workspace_id="ws_fin_1",
        organization_id="org_test_1",
        name="Invoice Automation",
    )
    proj_mgr.add_resource("proj_inv_1", "workflow", "wf_extract_invoice")
    assert "wf_extract_invoice" in proj.workflows
