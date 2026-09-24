"""
Tests for Workflow Runtime Execution, Checkpointing, and State Transitions.
"""

import asyncio
from app.workflows.domain.models import ExecutionState, TaskDefinition, TaskType, WorkflowDefinition
from app.workflows.runtime.runtime import WorkflowRuntime


def test_runtime_executes_sequential_tasks():
    runtime = WorkflowRuntime()

    # Custom task logic
    runtime.task_executor.register_handler(
        "extract_data",
        lambda task, ctx: {"extracted_amount": 1500, "customer": "Acme Corp"},
    )
    runtime.task_executor.register_handler(
        "calculate_tax",
        lambda task, ctx: {"tax_amount": ctx.get("extracted_amount", 0) * 0.1},
    )

    defn = WorkflowDefinition(
        id="tax_calculator_wf",
        name="Tax Calculator Workflow",
        tasks=[
            TaskDefinition(id="extract_data", name="Extract Data", type=TaskType.SYSTEM),
            TaskDefinition(id="calculate_tax", name="Calculate Tax", type=TaskType.SYSTEM, dependencies=["extract_data"]),
        ],
    )

    record = asyncio.run(runtime.execute_workflow(defn, initial_variables={"doc_id": "123"}))

    assert record.status == ExecutionState.COMPLETED
    assert record.context.variables["extracted_amount"] == 1500
    assert record.context.variables["tax_amount"] == 150.0
    assert len(record.tasks) == 2
    assert record.tasks["extract_data"].status == ExecutionState.COMPLETED
    assert record.tasks["calculate_tax"].status == ExecutionState.COMPLETED

    # Checkpoint was created
    latest_chk = runtime.checkpoint_manager.get_latest_checkpoint(record.execution_id)
    assert latest_chk is not None
    assert "tax_amount" in latest_chk.variables
    assert "extract_data" in latest_chk.completed_tasks
