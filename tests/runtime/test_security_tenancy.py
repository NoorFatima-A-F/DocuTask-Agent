"""
Multi-Tenant Security, Isolation & Boundary Enforcement Test Suite.
Validates:
- Context isolation across distinct enterprise tenants
- Zero leakage of execution state across tenant sessions
- Strict per-tenant quota isolation and rate limits
- Cryptographic audit trail tenant attribution
- Plugin permission sandboxing preventing privilege escalation
"""

import pytest
from app.agents.runtime.enterprise.audit_event import AuditEventType
from app.agents.runtime.enterprise.audit_log import ImmutableRuntimeAuditLog
from app.agents.runtime.enterprise.quota_manager import QuotaManager, TenantQuota
from app.agents.runtime.exceptions import (
    PluginValidationError,
    TenantIsolationViolationError,
)
from app.agents.runtime.plugin_loader import PluginManifest
from app.agents.runtime.plugin_manager import PluginSandbox
from app.agents.runtime.runtime_context import RuntimeContext
from app.agents.runtime.runtime_session import RuntimeSession


def test_tenant_context_isolation():
    ctx_a = RuntimeContext(tenant_id="tenant_alpha", workspace_id="ws_alpha")
    ctx_b = RuntimeContext(tenant_id="tenant_beta", workspace_id="ws_beta")

    session_a = RuntimeSession(context=ctx_a)
    session_b = RuntimeSession(context=ctx_b)

    assert session_a.context.tenant_id == "tenant_alpha"
    assert session_b.context.tenant_id == "tenant_beta"
    assert session_a.context.tenant_id != session_b.context.tenant_id

    child_a = session_a.spawn_child_session()
    assert child_a.context.tenant_id == "tenant_alpha"
    assert child_a.context.tenant_id != session_b.context.tenant_id


def test_per_tenant_quota_independence():
    qm = QuotaManager()

    # Tenant Alpha gets 1000 tokens
    qm.set_quota("tenant_alpha", TenantQuota(max_tokens_per_minute=1000))
    # Tenant Beta gets 5000 tokens
    qm.set_quota("tenant_beta", TenantQuota(max_tokens_per_minute=5000))

    # Alpha consumes 1000 -> reaches limit
    qm.consume_tokens("tenant_alpha", 1000)
    with pytest.raises(TenantIsolationViolationError):
        qm.consume_tokens("tenant_alpha", 1)

    # Beta is completely unaffected and has full quota available
    assert qm.consume_tokens("tenant_beta", 4000)
    assert qm.get_quota("tenant_beta").tokens_consumed == 4000


def test_audit_log_tenant_attribution():
    log = ImmutableRuntimeAuditLog()

    e_alpha = log.append(
        event_type=AuditEventType.TENANT_ACTION,
        actor="user_alpha@acme.com",
        details={"workflow_name": "process_invoices"},
        tenant_id="tenant_alpha",
    )

    e_beta = log.append(
        event_type=AuditEventType.TENANT_ACTION,
        actor="user_beta@globex.com",
        details={"workflow_name": "process_contracts"},
        tenant_id="tenant_beta",
    )

    assert e_alpha.tenant_id == "tenant_alpha"
    assert e_beta.tenant_id == "tenant_beta"
    assert log.verify_integrity()


def test_plugin_sandbox_privilege_escalation_blocked():
    sandbox = PluginSandbox(allowed_permissions={"filesystem:read", "telemetry:emit"})

    malicious_manifest = PluginManifest(
        plugin_id="exploit_plugin",
        name="Exploit Plugin",
        entrypoint="exploit:attack",
        permissions=["root:execute", "network:all", "filesystem:delete"],
    )

    with pytest.raises(PluginValidationError) as exc_info:
        sandbox.verify_permissions(malicious_manifest)

    msg = str(exc_info.value)
    assert "root:execute" in msg
    assert "network:all" in msg
