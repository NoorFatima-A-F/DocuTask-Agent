"""
Tests for Workflow Retry Engine and Timeout Engine.
"""

import asyncio
from app.workflows.retry.engine import RetryEngine
from app.workflows.domain.models import ExecutionState, TaskDefinition, WorkflowDefinition
from app.workflows.runtime.runtime import WorkflowRuntime


def test_retry_engine_delay_calculation():
    policy = {"backoff": "exponential", "base_delay_seconds": 1.0, "max_delay_seconds": 30.0, "jitter": False}
    d1 = RetryEngine.calculate_delay(1, policy)
    d2 = RetryEngine.calculate_delay(2, policy)
    d3 = RetryEngine.calculate_delay(3, policy)

    assert d1 == 1.0
    assert d2 == 2.0
    assert d3 == 4.0


def test_retry_engine_non_retryable_classification():
    class CustomValidationError(Exception):
        error_code = "VALIDATION_FAILED"

    assert RetryEngine.is_retryable(CustomValidationError()) is False
    assert RetryEngine.is_retryable(RuntimeError("Temporary timeout"), "NETWORK_ERROR") is True


def test_runtime_retries_flaky_task():
    runtime = WorkflowRuntime()
    attempts = {"count": 0}

    def flaky_task(task, ctx):
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise RuntimeError("Transient network error")
        return {"status": "SUCCESS"}

    runtime.task_executor.register_handler("flaky_api_call", flaky_task)

    defn = WorkflowDefinition(
        id="retry_wf",
        name="Retry Workflow",
        tasks=[
            TaskDefinition(
                id="flaky_api_call",
                name="Flaky API Call",
                retry_policy={"max_attempts": 3, "backoff": "fixed", "base_delay_seconds": 0.01},
            ),
        ],
    )

    record = asyncio.run(runtime.execute_workflow(defn))
    assert record.status == ExecutionState.COMPLETED
    assert attempts["count"] == 2
