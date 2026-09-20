"""
Tests for Saga Distributed Compensation and Reverse Rollback.
"""

import pytest
import asyncio
from app.workflows.domain.models import ExecutionState, TaskDefinition, TaskType, WorkflowDefinition
from app.workflows.runtime.runtime import WorkflowRuntime


def test_saga_executes_reverse_compensations_on_failure():
    runtime = WorkflowRuntime()
    rollbacks = []

    # Forward handlers
    runtime.task_executor.register_handler(
        "create_account",
        lambda task, ctx: {"account_id": "acc_999"},
    )
    runtime.task_executor.register_handler(
        "allocate_credit",
        lambda task, ctx: {"credit_allocated": True},
    )
    runtime.task_executor.register_handler(
        "send_welcome_email",
        lambda task, ctx: (_ for _ in ()).throw(RuntimeError("SMTP Server down")),
    )

    # Compensation handlers
    runtime.compensation_engine.register_handler(
        "delete_account",
        lambda rec: rollbacks.append(f"delete_account:{rec.task_id}"),
    )
    runtime.compensation_engine.register_handler(
        "refund_credit",
        lambda rec: rollbacks.append(f"refund_credit:{rec.task_id}"),
    )

    defn = WorkflowDefinition(
        id="saga_onboarding_wf",
        name="Saga Onboarding",
        compensation_policy={"enabled": True},
        tasks=[
            TaskDefinition(
                id="create_account",
                name="Create Account",
                compensation_action="delete_account",
                retry_policy={"max_attempts": 1},
            ),
            TaskDefinition(
                id="allocate_credit",
                name="Allocate Credit",
                dependencies=["create_account"],
                compensation_action="refund_credit",
                retry_policy={"max_attempts": 1},
            ),
            TaskDefinition(
                id="send_welcome_email",
                name="Send Welcome Email",
                dependencies=["allocate_credit"],
                retry_policy={"max_attempts": 1},
            ),
        ],
    )

    record = asyncio.run(runtime.execute_workflow(defn))

    assert record.status in (ExecutionState.FAILED, ExecutionState.COMPENSATING)
    # Rollbacks must happen in strict REVERSE order: allocate_credit first, then create_account
    assert rollbacks == ["refund_credit:allocate_credit", "delete_account:create_account"]
