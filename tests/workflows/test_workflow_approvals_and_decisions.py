"""
Tests for Human Approvals Gate, Suspension, and Decision Engine.
"""

import pytest
import asyncio
from app.workflows.domain.models import ExecutionState, TaskDefinition, TaskType, WorkflowDefinition
from app.workflows.runtime.runtime import WorkflowRuntime
from app.workflows.approvals.models import ApprovalStatus
from app.workflows.decision.engine import DecisionEngine


def test_decision_engine_conditions():
    vars_ctx = {"amount": 2500, "status": "verified", "flag": True}

    assert DecisionEngine.evaluate_condition("amount > 1000", vars_ctx) is True
    assert DecisionEngine.evaluate_condition("amount < 1000", vars_ctx) is False
    assert DecisionEngine.evaluate_condition("status == 'verified'", vars_ctx) is True
    assert DecisionEngine.evaluate_condition("status != 'rejected'", vars_ctx) is True


def test_human_approval_suspends_and_resumes():
    runtime = WorkflowRuntime()

    defn = WorkflowDefinition(
        id="approval_wf",
        name="Approval Workflow",
        tasks=[
            TaskDefinition(id="extract", name="Extract", type=TaskType.SYSTEM),
            TaskDefinition(id="manager_approval", name="Manager Approval", type=TaskType.APPROVAL, dependencies=["extract"]),
            TaskDefinition(id="finalize", name="Finalize", type=TaskType.SYSTEM, dependencies=["manager_approval"]),
        ],
    )

    # 1. Execute: should suspend at manager_approval
    record = asyncio.run(runtime.execute_workflow(defn))
    assert record.status == ExecutionState.SUSPENDED

    pending = runtime.approval_engine.get_pending_for_execution(record.execution_id)
    assert len(pending) == 1
    req = pending[0]
    assert req.task_id == "manager_approval"

    # 2. Human Approver approves the request
    runtime.approval_engine.submit_vote(
        request_id=req.request_id,
        approver="alice_manager",
        decision=ApprovalStatus.APPROVED,
        comment="Approved by finance manager",
    )
    assert req.status == ApprovalStatus.APPROVED

    # 3. Resume workflow execution
    resumed_rec = asyncio.run(runtime.resume_execution(
        execution_id=record.execution_id,
        definition=defn,
        resumed_variables={"approved_by": "alice_manager"},
    ))

    assert resumed_rec.status == ExecutionState.COMPLETED
