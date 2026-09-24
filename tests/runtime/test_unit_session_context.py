"""
Unit test suite for Runtime Session and Distributed Context Propagation.
Validates:
- Complete enterprise ID suite (tenant_id, workspace_id, runtime_id, workflow_id,
  execution_id, agent_id, request_id, correlation_id, trace_id, span_id)
- W3C traceparent formatting and parsing
- Child context derivation and span generation
- Carrier encoding/decoding roundtrip
- ContextPropagationMiddleware injection & extraction
- RuntimeSession hierarchy and multi-session bindings (workflow, execution, recovery, reflection)
"""

from uuid import uuid4
from app.agents.runtime.runtime_context import ContextPropagationMiddleware, RuntimeContext
from app.agents.runtime.runtime_session import RuntimeSession


def test_runtime_context_default_generation():
    ctx = RuntimeContext(tenant_id="tenant-corp-1", workspace_id="ws-alpha")
    assert ctx.tenant_id == "tenant-corp-1"
    assert ctx.workspace_id == "ws-alpha"
    assert ctx.runtime_id
    assert ctx.request_id
    assert ctx.correlation_id
    assert ctx.trace_id
    assert ctx.span_id
    assert len(ctx.span_id) == 16
    assert ctx.traceparent == f"00-{ctx.trace_id}-{ctx.span_id}-01"


def test_child_context_spawning():
    parent = RuntimeContext(
        tenant_id="tenant-123",
        workspace_id="ws-456",
        workflow_id="wf-001",
    )
    child = parent.spawn_child_context(
        new_span=True,
        agent_id="agent-worker-1",
        execution_id="exec-999",
    )

    # Invariants preserved
    assert child.tenant_id == parent.tenant_id
    assert child.workspace_id == parent.workspace_id
    assert child.trace_id == parent.trace_id
    assert child.correlation_id == parent.correlation_id
    assert child.workflow_id == parent.workflow_id

    # New child properties
    assert child.agent_id == "agent-worker-1"
    assert child.execution_id == "exec-999"
    assert child.span_id != parent.span_id


def test_carrier_roundtrip():
    original = RuntimeContext(
        tenant_id="acme-corp",
        workspace_id="acme-prod",
        workflow_id="wf-100",
        execution_id="exec-200",
        agent_id="agent-300",
    )
    carrier = original.to_carrier()

    assert carrier["x-tenant-id"] == "acme-corp"
    assert carrier["x-workspace-id"] == "acme-prod"
    assert carrier["x-workflow-id"] == "wf-100"
    assert carrier["x-execution-id"] == "exec-200"
    assert carrier["x-agent-id"] == "agent-300"
    assert carrier["traceparent"] == original.traceparent

    restored = RuntimeContext.from_carrier(carrier)
    assert restored.tenant_id == original.tenant_id
    assert restored.workspace_id == original.workspace_id
    assert restored.workflow_id == original.workflow_id
    assert restored.execution_id == original.execution_id
    assert restored.agent_id == original.agent_id
    assert restored.trace_id == original.trace_id
    assert restored.span_id == original.span_id


def test_context_propagation_middleware():
    ctx = RuntimeContext(tenant_id="t-abc", workspace_id="ws-xyz")
    headers = {"Content-Type": "application/json"}

    ContextPropagationMiddleware.inject(ctx, headers)
    assert headers["x-tenant-id"] == "t-abc"
    assert "traceparent" in headers

    extracted = ContextPropagationMiddleware.extract(headers)
    assert extracted.tenant_id == "t-abc"
    assert extracted.workspace_id == "ws-xyz"


def test_runtime_session_hierarchy():
    root_session = RuntimeSession()
    assert root_session.status == "ACTIVE"
    assert root_session.parent_session_id is None

    child_session = root_session.spawn_child_session(
        agent_id="sub-agent-1",
        execution_id="exec-sub",
    )
    assert child_session.parent_session_id == root_session.session_id
    assert child_session.context.agent_id == "sub-agent-1"
    assert child_session.context.execution_id == "exec-sub"


def test_runtime_session_bindings():
    session = RuntimeSession()
    wf_id = uuid4()
    exec_id = uuid4()
    rec_id = uuid4()
    refl_id = uuid4()

    s1 = session.bind_workflow_session(wf_id)
    assert s1.workflow_session_id == wf_id
    assert s1.context.workflow_id == str(wf_id)

    s2 = s1.bind_execution_session(exec_id)
    assert s2.execution_session_id == exec_id
    assert s2.context.execution_id == str(exec_id)

    s3 = s2.bind_recovery_session(rec_id)
    assert s3.recovery_session_id == rec_id

    s4 = s3.bind_reflection_session(refl_id)
    assert s4.reflection_session_id == refl_id

    closed = s4.close(status="COMPLETED")
    assert closed.status == "COMPLETED"
    assert closed.closed_at is not None
