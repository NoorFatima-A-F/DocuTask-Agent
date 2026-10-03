"""Test Tenant Context & Resolver Infrastructure."""

import pytest
from app.tenancy.core.models import TenantContext, Region, SubscriptionTier, ComplianceProfileType
from app.tenancy.context.context import (
    TenantContextScope,
    get_current_tenant_context,
)
from app.tenancy.context.resolver import TenantContextResolver
from app.tenancy.core.exceptions import TenantNotFoundError


def test_tenant_context_creation_and_scope():
    """Verify TenantContext model and scoped context manager."""
    ctx = TenantContext(
        organization_id="org_123",
        workspace_id="ws_456",
        user_id="user_789",
        region=Region.EU_WEST,
        subscription_plan=SubscriptionTier.ENTERPRISE,
    )

    assert get_current_tenant_context() is None

    with TenantContextScope(ctx) as active_ctx:
        assert active_ctx.organization_id == "org_123"
        assert get_current_tenant_context() == ctx

    assert get_current_tenant_context() is None


def test_tenant_context_resolver_from_headers():
    """Verify resolving tenant context from HTTP headers."""
    resolver = TenantContextResolver()

    headers = {
        "X-Organization-Id": "org_acme",
        "X-Workspace-Id": "ws_finance",
        "X-Environment-Id": "production",
        "X-User-Id": "user_alice",
        "X-Request-Id": "req_999",
    }

    ctx = resolver.resolve_from_headers(headers)
    assert ctx.organization_id == "org_acme"
    assert ctx.workspace_id == "ws_finance"
    assert ctx.environment_id == "production"
    assert ctx.user_id == "user_alice"
    assert ctx.request_id == "req_999"


def test_tenant_context_resolver_missing_org_raises():
    """Verify missing organization ID raises TenantNotFoundError."""
    resolver = TenantContextResolver()
    with pytest.raises(TenantNotFoundError):
        resolver.resolve_from_headers({"X-User-Id": "user_1"})


def test_tenant_context_resolver_from_task_metadata():
    """Verify resolving tenant context for background worker jobs."""
    resolver = TenantContextResolver()

    metadata = {
        "organization_id": "org_worker_test",
        "workspace_id": "ws_batch",
        "user_id": "worker_daemon",
        "subscription_plan": "ENTERPRISE",
        "region": "eu-central-1",
        "compliance_profile": "GDPR",
    }

    ctx = resolver.resolve_from_task_metadata(metadata)
    assert ctx.organization_id == "org_worker_test"
    assert ctx.workspace_id == "ws_batch"
    assert ctx.subscription_plan == SubscriptionTier.ENTERPRISE
    assert ctx.region == Region.EU_CENTRAL
    assert ctx.compliance_profile == ComplianceProfileType.GDPR
