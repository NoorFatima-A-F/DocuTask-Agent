"""Tests for Public and Internal Governance Platform APIs."""

from app.governance.platform.api.public.policies import (
    handle_create_policy,
    handle_get_policy,
    handle_list_policies,
    handle_publish_policy,
)
from app.governance.platform.api.public.decisions import (
    handle_evaluate_action,
    handle_list_decisions,
)
from app.governance.platform.api.public.audits import (
    audit_api_service,
    handle_get_audit_proof,
    handle_list_audits,
)
from app.governance.platform.api.public.analytics import (
    handle_get_analytics_summary,
    handle_get_compliance_status,
    handle_get_risk_overview,
)
from app.governance.platform.api.public.approvals import (
    approval_api_service,
    handle_approve_request,
    handle_list_approvals,
    handle_reject_request,
)
from app.governance.platform.api.internal.services import (
    handle_internal_sync_agent,
    handle_internal_sync_workflow,
    handle_internal_system_health,
)
from app.governance.platform.api.internal.events import (
    handle_internal_publish_event,
    internal_event_bridge,
)
from app.governance.platform.gateway.authentication import APIRequestContext, AuthScheme


def test_public_policy_management_apis():
    ctx = APIRequestContext(client_id="c1", tenant_id="tenant_alpha", scopes={"*"})

    # Create policy
    create_body = {
        "name": "Model Safety Policy",
        "description": "Requires safe model calls",
        "policy_type": "security",
        "severity": "HIGH",
        "enforcement_action": "DENY",
        "rules": [{"check": "model_authorized"}],
    }
    created = handle_create_policy(ctx, create_body)
    assert created["name"] == "Model Safety Policy"
    assert created["status"] == "DRAFT"

    # List policies
    listed = handle_list_policies(ctx)
    assert listed["total_count"] >= 1

    # Get policy
    fetched = handle_get_policy(ctx, {"id": created["policy_id"]})
    assert fetched["policy_id"] == created["policy_id"]

    # Publish policy
    published = handle_publish_policy(ctx, {"id": created["policy_id"]}, {"version": "1.1.0"})
    assert published["status"] == "ACTIVE"
    assert published["version"] == "1.1.0"


def test_public_decision_evaluation_and_auditing():
    ctx = APIRequestContext(client_id="c1", tenant_id="tenant_alpha", scopes={"*"})

    # Standard allow action
    eval_res = handle_evaluate_action(
        ctx,
        {
            "action": "agent.execute",
            "resource": "invoice_agent",
            "context": {"risk_level": "low"},
        },
    )
    assert eval_res["allowed"] is True
    assert eval_res["decision"] == "ALLOW"

    # Blocked unauthorized model action
    blocked_res = handle_evaluate_action(
        ctx,
        {
            "action": "model.invoke",
            "resource": "unauthorized_model",
            "context": {"risk_level": "high"},
        },
    )
    assert blocked_res["allowed"] is False
    assert blocked_res["decision"] == "DENY"

    # Query decisions
    decisions = handle_list_decisions(ctx)
    assert decisions["total_count"] >= 2


def test_public_audits_and_evidence():
    ctx = APIRequestContext(client_id="c1", tenant_id="tenant_alpha", scopes={"*"})

    # Record audit event
    audit_rec = audit_api_service.record_event(
        tenant_id="tenant_alpha",
        actor="user_123",
        action="policy.create",
        resource="pol_test",
        decision="ALLOW",
    )
    assert audit_rec["integrity_hash"] != ""

    # List audits
    audits = handle_list_audits(ctx)
    assert audits["total_count"] >= 1

    # Verify proof
    proof = handle_get_audit_proof(ctx, {"id": audit_rec["audit_id"]})
    assert proof["verified"] is True
    assert proof["integrity_hash"] == audit_rec["integrity_hash"]


def test_public_analytics_and_approvals():
    ctx = APIRequestContext(client_id="c1", tenant_id="tenant_alpha", scopes={"*"})

    # Analytics
    summary = handle_get_analytics_summary(ctx)
    assert summary["governance_health_score"] > 90
    risk = handle_get_risk_overview(ctx)
    assert risk["overall_risk_level"] == "LOW"
    comp = handle_get_compliance_status(ctx)
    assert "SOC2_TYPE_II" in comp["frameworks"]

    # Approvals workflow
    appr_item = approval_api_service.submit_for_review(
        tenant_id="tenant_alpha",
        action="high_budget_run",
        resource="agent_fin",
    )
    assert appr_item["status"] == "PENDING"

    # Approve
    approved = handle_approve_request(ctx, {"id": appr_item["request_id"]}, {"reviewer_id": "rev_admin"})
    assert approved["status"] == "APPROVED"
    assert approved["reviewer_id"] == "rev_admin"


def test_internal_services_and_event_bridge():
    ctx = APIRequestContext(
        client_id="sys",
        tenant_id="tenant_system",
        auth_scheme=AuthScheme.INTERNAL_SYSTEM,
        scopes={"*"},
    )

    # Sync Agent State
    agent_sync = handle_internal_sync_agent(ctx, {"agent_id": "ag_1", "state": {"status": "busy"}})
    assert agent_sync["synced"] is True

    # Sync Workflow Checkpoint
    wf_sync = handle_internal_sync_workflow(ctx, {"workflow_id": "wf_1", "checkpoint": {"step_id": "s2"}})
    assert wf_sync["governance_checkpoint_valid"] is True

    # Health
    health = handle_internal_system_health(ctx)
    assert health["status"] == "OPERATIONAL"

    # Internal Events Bridge
    received = []
    internal_event_bridge.subscribe("TEST_EVENT", lambda evt: received.append(evt))
    handle_internal_publish_event(ctx, {"event_type": "TEST_EVENT", "payload": {"key": "val"}})
    assert len(received) == 1
    assert received[0]["payload"]["key"] == "val"
