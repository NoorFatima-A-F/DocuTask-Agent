"""
Tests for Workflow Simulator and Replay Engine.
"""

import pytest
import asyncio
from app.workflows.domain.models import ExecutionState, TaskDefinition, TaskType, WorkflowDefinition
from app.workflows.simulator.simulator import WorkflowSimulator
from app.workflows.runtime.runtime import WorkflowRuntime
from app.workflows.replay.replay_engine import WorkflowReplayEngine


def test_workflow_simulator_dry_run():
    defn = WorkflowDefinition(
        id="sim_wf",
        name="Simulation Test Workflow",
        tasks=[
            TaskDefinition(id="ocr", name="OCR Task", type=TaskType.SYSTEM),
            TaskDefinition(id="ai_reasoning", name="AI Reasoning", type=TaskType.AI, dependencies=["ocr"]),
            TaskDefinition(id="approval", name="Human Approval", type=TaskType.APPROVAL, dependencies=["ai_reasoning"]),
        ],
    )

    report = WorkflowSimulator.simulate(defn)
    assert report.is_valid is True
    assert report.total_tasks == 3
    assert report.estimated_cost_cents > 0
    assert len(report.potential_bottlenecks) >= 1


def test_workflow_replay_engine():
    runtime = WorkflowRuntime()
    runtime.task_executor.register_handler("add_ten", lambda t, ctx: {"val": ctx.get("val", 0) + 10})

    defn = WorkflowDefinition(
        id="add_wf",
        name="Add Workflow",
        tasks=[TaskDefinition(id="add_ten", name="Add Ten")],
    )

    # First execution
    rec = asyncio.run(runtime.execute_workflow(defn, initial_variables={"val": 5}))
    assert rec.status == ExecutionState.COMPLETED
    assert rec.context.variables["val"] == 15

    # Replay with override
    replay_engine = WorkflowReplayEngine(runtime)
    replayed_rec = asyncio.run(replay_engine.replay_execution(
        execution_id=rec.execution_id,
        definition=defn,
        override_variables={"val": 20},
    ))

    assert replayed_rec.status == ExecutionState.COMPLETED
    assert replayed_rec.context.variables["val"] == 30
