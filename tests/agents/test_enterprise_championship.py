"""
Test suite for Enterprise Championship AAOS modules:
1. Google Cloud Vertex AI Gemini Gateway & GCP Event Bridge
2. Adaptive Dynamic Replanning & Contingency Mutator
3. Distributed Lock Manager & Optimistic Concurrency Workflow State
"""

import pytest
from pydantic import BaseModel

from app.agents.events.event_types import GoalReceivedEvent
from app.agents.planning.adaptive.replanning_engine import (
    AdaptiveReplanningEngine,
)
from app.agents.planning.execution_plan import PlannedTask
from app.agents.reflection.critics.consensus_evaluator import ConsensusCritiqueResult
from app.agents.runtime.cloud.gcp_vertex_gateway import (
    GCPCloudEventBridge,
    GeminiModelFamily,
    VertexAIConfig,
    VertexAIGeminiGateway,
)
from app.agents.runtime.distributed.distributed_lock import (
    DistributedLockManager,
    DistributedWorkflowStateManager,
)
from app.agents.workflow.task_graph.dynamic_task_graph import DynamicTaskGraph, NodeState


class SampleIntentSchema(BaseModel):
    primary_intent: str
    confidence: float
    document_type: str


@pytest.mark.asyncio
async def test_vertex_ai_gateway_structured_generation():
    """Test Vertex AI Gemini Gateway structured output parsing."""
    gateway = VertexAIGeminiGateway(config=VertexAIConfig(model_name=GeminiModelFamily.GEMINI_1_5_PRO.value))
    res = await gateway.generate_structured(
        prompt="Analyze goal: Process invoice with high accuracy",
        schema_model=SampleIntentSchema,
    )
    assert res.primary_intent == "document_processing"
    assert res.confidence >= 0.95
    assert res.document_type == "invoice"
    assert gateway.total_calls >= 1
    assert gateway.total_cost_usd > 0.0


@pytest.mark.asyncio
async def test_gcp_cloud_event_bridge():
    """Test GCP Pub/Sub and Cloud Tasks event bridge."""
    bridge = GCPCloudEventBridge(project_id="test-agent-project", pubsub_topic="agent-events")
    event = GoalReceivedEvent(
        execution_id="exec_123",
        payload={"goal": "Process receipt"},
    )
    published = await bridge.publish_event(event)
    assert published is True
    assert len(bridge.published_events) == 1
    assert "test-agent-project" in bridge.published_events[0]["topic"]

    task_id = await bridge.enqueue_cloud_task(
        queue_name="agent-background-queue",
        target_url="https://agent-runner.run.app/execute",
        task_payload={"execution_id": "exec_123"},
        delay_seconds=10,
    )
    assert task_id.startswith("task_")
    assert len(bridge.enqueued_tasks) == 1


def test_adaptive_replanning_engine_tool_replacement():
    """Test dynamic DAG mutation upon task failure."""
    engine = AdaptiveReplanningEngine()
    graph = DynamicTaskGraph()
    t1 = PlannedTask(task_id="t1", name="OCR Task", action="ocr", required_tools=["legacy_tesseract_ocr"])
    t2 = PlannedTask(task_id="t2", name="Extraction", action="extract", required_tools=["llm_extractor"], dependencies=["t1"])
    graph.add_task(t1)
    graph.add_task(t2)
    graph.refresh_states()

    # Trigger replan for failed OCR task
    outcome = engine.evaluate_and_mutate(graph, failed_task_ids=["t1"])
    assert outcome.success is True
    assert outcome.nodes_modified == 1
    assert graph._nodes["t1"].required_tools == ["advanced_vision_ocr"]
    assert graph._states["t1"] == NodeState.READY


def test_adaptive_replanning_engine_validation_gate_insertion():
    """Test dynamic validation gate insertion from reflection critique."""
    engine = AdaptiveReplanningEngine()
    graph = DynamicTaskGraph()
    t1 = PlannedTask(task_id="t1_extract", name="Data Extraction", action="extract", required_tools=["invoice_extractor"])
    t2 = PlannedTask(task_id="t2_export", name="Export", action="export", required_tools=["json_exporter"], dependencies=["t1_extract"])
    graph.add_task(t1)
    graph.add_task(t2)
    graph.refresh_states()

    critique = ConsensusCritiqueResult(
        overall_score=0.65,
        passed=False,
        needs_human_escalation=False,
        needs_replanning=True,
        critic_scores={"rule_critic": 0.5},
        all_issues=["Arithmetic total sum does not match line items"],
        actionable_repair_instructions=["Insert validation gate"],
    )

    outcome = engine.evaluate_and_mutate(graph, critique=critique)
    assert outcome.success is True
    assert outcome.nodes_added == 1
    # Check that a validation gate was inserted before t2_export
    gate_task_id = [tid for tid in graph._nodes if tid.startswith("gate_val_")][0]
    assert "gate_val_" in gate_task_id
    assert gate_task_id in graph._nodes["t2_export"].dependencies


@pytest.mark.asyncio
async def test_distributed_lock_manager():
    """Test distributed lock acquisition, renewal, and mutual exclusion."""
    lock_mgr = DistributedLockManager(default_ttl_seconds=2.0)
    lease1 = await lock_mgr.acquire_lock("doc_123", "worker_A", ttl_seconds=1.0)
    assert lease1 is not None
    assert lease1.owner_id == "worker_A"

    # Worker B cannot acquire while lease1 is active
    lease2 = await lock_mgr.acquire_lock("doc_123", "worker_B", timeout_seconds=0.1)
    assert lease2 is None

    # Renew lease
    renewed = await lock_mgr.renew_lease(lease1, additional_seconds=2.0)
    assert renewed is True

    # Release lease
    released = await lock_mgr.release_lock(lease1)
    assert released is True

    # Now Worker B can acquire
    lease2 = await lock_mgr.acquire_lock("doc_123", "worker_B", timeout_seconds=0.5)
    assert lease2 is not None
    assert lease2.owner_id == "worker_B"


@pytest.mark.asyncio
async def test_distributed_workflow_state_optimistic_concurrency():
    """Test optimistic concurrency control (OCC) for workflow state."""
    state_mgr = DistributedWorkflowStateManager()
    session_id = "sess_xyz_789"

    # Initial commit (version 0 -> version 1)
    s1 = await state_mgr.commit_state(session_id, {"step": 1, "status": "IN_PROGRESS"}, expected_version=0)
    assert s1.version == 1
    assert s1.data["step"] == 1

    # Concurrent write with stale version should fail
    with pytest.raises(ValueError, match="Optimistic concurrency conflict"):
        await state_mgr.commit_state(session_id, {"step": 2, "status": "STALE"}, expected_version=0)

    # Valid write with current version (version 1 -> version 2)
    s2 = await state_mgr.commit_state(session_id, {"step": 2, "status": "COMPLETED"}, expected_version=1)
    assert s2.version == 2
    assert s2.data["status"] == "COMPLETED"
