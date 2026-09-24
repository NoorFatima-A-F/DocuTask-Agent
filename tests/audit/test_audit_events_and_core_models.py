"""Tests for AuditEvent Core Domain Models, Enums, and Contexts."""

from app.audit.core.events import (
    AuditEvent,
    ActorType,
    AuditSeverity,
    OutcomeType,
    EventCategory,
)
from app.audit.core.models import (
    AIExecutionAuditContext,
)
from app.audit.core.context import AuditContext


def test_audit_event_creation_and_defaults():
    event = AuditEvent(
        event_type="workflow.execute",
        category=EventCategory.WORKFLOW,
        tenant_id="tenant_alpha",
        actor_id="usr_001",
        actor_type=ActorType.USER,
        action="execute",
        resource_type="workflow",
        resource_id="wf_invoice_01",
    )
    assert event.event_id.startswith("aud_evt_")
    assert event.tenant_id == "tenant_alpha"
    assert event.category == EventCategory.WORKFLOW
    assert event.severity == AuditSeverity.INFO
    assert event.outcome == OutcomeType.SUCCESS
    assert event.environment == "production"


def test_audit_context_and_child_derivation():
    ctx = AuditContext(
        tenant_id="tenant_beta",
        actor_id="agent_supervisor",
        actor_type="AGENT",
        workflow_id="wf_100",
    )
    assert ctx.request_id.startswith("req_")
    assert ctx.correlation_id.startswith("corr_")

    child_ctx = ctx.child_context(event_id="aud_parent_123")
    assert child_ctx.parent_event_id == "aud_parent_123"
    assert child_ctx.correlation_id == ctx.correlation_id
    assert child_ctx.workflow_id == "wf_100"


def test_ai_execution_audit_context():
    ai_ctx = AIExecutionAuditContext(
        model_id="gemini-1.5-pro",
        model_version="1.0.0",
        prompt_id="invoice_parser",
        prompt_version="2.1.0",
        prompt_tokens=450,
        completion_tokens=120,
        grounding_score=0.95,
        tool_calls=["view_file", "extract_table"],
    )
    assert ai_ctx.model_id == "gemini-1.5-pro"
    assert len(ai_ctx.tool_calls) == 2
    assert ai_ctx.grounding_score == 0.95
