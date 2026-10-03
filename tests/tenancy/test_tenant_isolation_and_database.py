"""Test Tenant Isolation & Database Row-Level Filtering."""

import pytest
from app.tenancy.core.models import TenantContext, ResourceType
from app.tenancy.core.exceptions import CrossTenantViolationError
from app.tenancy.context.context import TenantContextScope
from app.tenancy.isolation.database import TenantDatabaseManager
from app.tenancy.ownership.ownership import ResourceOwnershipManager


def test_tenant_database_row_level_isolation():
    """Verify shared database row-level query filtering prevents cross-tenant leaks."""
    db = TenantDatabaseManager()

    ctx_a = TenantContext(organization_id="org_alpha", workspace_id="ws_a", user_id="user_a")
    ctx_b = TenantContext(organization_id="org_beta", workspace_id="ws_b", user_id="user_b")

    # Insert records under Org Alpha
    with TenantContextScope(ctx_a):
        db.insert("documents", {"doc_id": "doc_1", "title": "Alpha Confidential Q3"})
        db.insert("documents", {"doc_id": "doc_2", "title": "Alpha Public Info"})

    # Insert records under Org Beta
    with TenantContextScope(ctx_b):
        db.insert("documents", {"doc_id": "doc_3", "title": "Beta Secret Strategy"})

    # Org Alpha query should see ONLY Org Alpha records
    with TenantContextScope(ctx_a):
        results_a = db.query("documents").all()
        assert len(results_a) == 2
        assert all(d["organization_id"] == "org_alpha" for d in results_a)

    # Org Beta query should see ONLY Org Beta records
    with TenantContextScope(ctx_b):
        results_b = db.query("documents").all()
        assert len(results_b) == 1
        assert results_b[0]["doc_id"] == "doc_3"
        assert results_b[0]["organization_id"] == "org_beta"


def test_resource_ownership_cross_tenant_access_blocked():
    """Verify ResourceOwnershipManager blocks unauthorized cross-tenant access."""
    ownership_mgr = ResourceOwnershipManager()

    ctx_a = TenantContext(organization_id="org_alpha", workspace_id="ws_a", user_id="user_a")
    ctx_b = TenantContext(organization_id="org_beta", workspace_id="ws_b", user_id="user_b")

    # Stamp workflow under Org Alpha
    with TenantContextScope(ctx_a):
        ownership_mgr.stamp_resource(
            resource_id="wf_invoice_proc",
            resource_type=ResourceType.WORKFLOW,
        )

    # Org Alpha can access its own workflow
    with TenantContextScope(ctx_a):
        assert ownership_mgr.verify_access("wf_invoice_proc") is True

    # Org Beta attempting to access Org Alpha workflow MUST raise CrossTenantViolationError
    with TenantContextScope(ctx_b):
        with pytest.raises(CrossTenantViolationError):
            ownership_mgr.verify_access("wf_invoice_proc")
