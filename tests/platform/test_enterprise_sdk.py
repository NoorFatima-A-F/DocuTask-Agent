"""Tests for Enterprise Agent SDK Base Classes and Protocols."""

import pytest
from app.sdk.agent_sdk import (
    AgentExecutionContext,
    AgentLifecycleState,
    AgentManifest,
    BaseAgent,
)
from app.sdk.planner_sdk import BasePlanner, CandidatePlan
from app.sdk.tool_sdk import BaseTool, ToolSchema
from app.sdk.worker_sdk import BaseWorker, WorkerResult, WorkerTask


class DummyAgent(BaseAgent):
    def execute(self, payload):
        return {"processed": True, "input_len": len(payload)}


class DummyWorker(BaseWorker):
    def process_task(self, task: WorkerTask) -> WorkerResult:
        return WorkerResult(
            task_id=task.task_id,
            status="SUCCESS",
            output_payload={"result": "ok"},
            latency_ms=10.0,
        )


def test_agent_sdk_lifecycle():
    manifest = AgentManifest(
        agent_id="agent.test.dummy",
        name="Dummy Test Agent",
        version="1.0.0",
        author="Tester",
        description="A test agent",
        permission_scopes=["ocr:read"],
    )
    agent = DummyAgent(manifest)
    assert agent.state == AgentLifecycleState.UNINITIALIZED

    agent.initialize()
    assert agent.state == AgentLifecycleState.IDLE
    assert agent.context.has_scope("ocr:read") is True
    assert agent.context.has_scope("admin:write") is False

    res = agent.execute({"a": 1, "b": 2})
    assert res["processed"] is True

    health = agent.get_health()
    assert health["healthy"] is True

    agent.terminate()
    assert agent.state == AgentLifecycleState.TERMINATED


def test_worker_sdk():
    worker = DummyWorker(worker_id="w-01", capability="perception.ocr")
    task = WorkerTask(task_id="t-01", capability_name="perception.ocr", input_payload={"img": "raw"})
    res = worker.process_task(task)
    assert res.status == "SUCCESS"
    assert res.latency_ms == 10.0
    assert worker.probe_health()["healthy"] is True
