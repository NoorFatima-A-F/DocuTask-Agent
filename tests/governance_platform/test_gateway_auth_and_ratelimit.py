"""Tests for Gateway Authentication, Scopes, and Rate Limiting."""

import pytest
from app.governance.platform.gateway.authentication import (
    AuthenticationManager,
    AuthScheme,
)
from app.governance.platform.gateway.rate_limit import (
    RateLimiter,
    RateLimitPolicy,
    TokenBucket,
)
from app.governance.platform.gateway.middleware import GatewayMiddleware
from app.governance.platform.gateway.router import GatewayRouter


def test_api_key_lifecycle_and_authentication():
    auth_mgr = AuthenticationManager()
    raw_key, record = auth_mgr.create_api_key(
        name="Test Integration Key",
        tenant_id="tenant_acme",
        scopes={"governance:read", "governance:evaluate"},
    )

    assert raw_key.startswith("gov_live_")
    assert record.tenant_id == "tenant_acme"

    # Authenticate via Bearer header
    ctx = auth_mgr.authenticate_request(authorization_header=f"Bearer {raw_key}")
    assert ctx.tenant_id == "tenant_acme"
    assert ctx.auth_scheme == AuthScheme.API_KEY
    assert ctx.has_scope("governance:read")
    assert not ctx.has_scope("governance:admin")

    # Revoke key
    assert auth_mgr.revoke_api_key(record.key_id) is True
    with pytest.raises(PermissionError, match="revoked or disabled"):
        auth_mgr.authenticate_request(authorization_header=f"Bearer {raw_key}")


def test_service_account_and_internal_bypass():
    auth_mgr = AuthenticationManager()
    sa = auth_mgr.register_service_account(
        name="Workflow Engine SA",
        tenant_id="tenant_system",
        scopes={"governance:internal", "governance:evaluate"},
    )
    assert sa.account_id.startswith("sa_")

    # Internal token authentication
    ctx = auth_mgr.authenticate_request(authorization_header="Bearer gov_internal_master_token")
    assert ctx.tenant_id == "tenant_system"
    assert ctx.auth_scheme == AuthScheme.INTERNAL_SYSTEM
    assert ctx.has_scope("any:scope")


def test_rate_limiter_token_bucket():
    bucket = TokenBucket(rate_per_minute=60, burst_capacity=5)
    # Burst 5 tokens
    for _ in range(5):
        assert bucket.consume(1) is True

    # 6th token should fail
    assert bucket.consume(1) is False


def test_rate_limiter_multi_dimensional():
    limiter = RateLimiter()
    limiter.set_policy(
        RateLimitPolicy(dimension="tenant", limit_key="tenant_small", rate_per_minute=60, burst_capacity=2)
    )

    # 2 requests succeed
    allowed1, _ = limiter.check_rate_limit(tenant_id="tenant_small", client_id="client_1")
    allowed2, _ = limiter.check_rate_limit(tenant_id="tenant_small", client_id="client_1")
    assert allowed1 is True
    assert allowed2 is True

    # 3rd request fails
    allowed3, info = limiter.check_rate_limit(tenant_id="tenant_small", client_id="client_1")
    assert allowed3 is False
    assert info["dimension"] == "tenant"
    assert len(limiter.get_violations("tenant_small")) == 1


def test_gateway_router_and_middleware():
    auth_mgr = AuthenticationManager()
    raw_key, _ = auth_mgr.create_api_key(name="Dev Key", tenant_id="tenant_test", scopes={"*"})
    router = GatewayRouter(auth_manager=auth_mgr)

    # Register test route
    router.add_route(
        method="GET",
        path="/api/v1/test",
        handler=lambda ctx: {"status": "ok", "tenant": ctx.tenant_id},
        description="Test endpoint",
    )

    # Dispatch with valid key
    res = router.dispatch("GET", "/api/v1/test", headers={"Authorization": f"Bearer {raw_key}"})
    assert res == {"status": "ok", "tenant": "tenant_test"}

    # Dispatch with invalid key
    err_res = router.dispatch("GET", "/api/v1/test", headers={"Authorization": "Bearer invalid_key"})
    assert "error" in err_res
    assert err_res["error"]["code"] == "FORBIDDEN"

    # OpenAPI spec generation
    spec = router.generate_openapi_spec()
    assert spec["openapi"] == "3.0.0"
    assert "/api/v1/test" in spec["paths"]
