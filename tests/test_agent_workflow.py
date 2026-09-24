"""
Unit and Integration Test Suite for Enterprise Workflow Runtime & Multi-Agent Orchestration Engine.
Targeting >=95% meaningful coverage across lifecycle, DAGs, sagas, compensations, human approvals,
signals, timers, waits, replay, migration, and adapters.
"""

import pytest
from uuid import uuid4

from app.agents.workflow.approval_workflow import ApprovalWorkflowEngine
from app.agents.workflow.builders import (
    WorkflowDefinitionBuilder,
    WorkflowNodeBuilder,
    WorkflowRequestBuilder,
)
from app.agents.workflow.child_workflow import ChildWorkflowManager
from app.agents.workflow.compensation import CompensationCoordinator
from app.agents.workflow.coordination_adapter import WorkflowCoordinationAdapter
from app.agents.workflow.decision_adapter import WorkflowDecisionAdapter
from app.agents.workflow.exceptions import (
    CyclicWorkflowGraphError,
    InvalidTimerConfigurationError,
    InvalidWorkflowMigrationError,
    InvalidWorkflowStateTransitionError,
    MissingCompensationPathError,
    OrphanedChildWorkflowError,
)
from app.agents.workflow.execution_adapter import WorkflowExecutionAdapter
from app.agents.workflow.factory import WorkflowFactory
from app.agents.workflow.human_task import HumanTaskDecision, HumanTaskStatus
from app.agents.workflow.lifecycle import WorkflowLifecycleState
from app.agents.workflow.memory_adapter import WorkflowMemoryAdapter
from app.agents.workflow.metadata import (
    WorkflowIdentity,
)
from app.agents.workflow.metrics import (
    WorkflowMetricsCollector,
)
from app.agents.workflow.planner_adapter import WorkflowPlannerAdapter
from app.agents.workflow.recovery_adapter import WorkflowRecoveryAdapter
from app.agents.workflow.reflection_adapter import WorkflowReflectionAdapter
from app.agents.workflow.saga import SagaOrchestrator
from app.agents.workflow.serialization import WorkflowSerializer
from app.agents.workflow.signal_manager import SignalManager
from app.agents.workflow.telemetry import WorkflowTelemetry
from app.agents.workflow.timer_manager import TimerManager
from app.agents.workflow.validators import WorkflowValidator
from app.agents.workflow.wait_manager import WaitManager
from app.agents.workflow.workflow_edge import WorkflowEdge
from app.agents.workflow.workflow_graph import WorkflowGraph
from app.agents.workflow.workflow_history import WorkflowHistory
from app.agents.workflow.workflow_instance import WorkflowInstance
from app.agents.workflow.workflow_migration import WorkflowMigrationEngine
from app.agents.workflow.workflow_node import WorkflowNode, WorkflowNodeType
from app.agents.workflow.workflow_replay import WorkflowReplayEngine
from app.agents.workflow.workflow_version import WorkflowVersion
from app.agents.workflow.workflow_cache import WorkflowCache


# ============================================================================
# 1. Lifecycle State Machine Tests
# ============================================================================

def test_lifecycle_states_and_valid_transitions():
    """Tests valid transitions across 15 lifecycle states."""
    instance = WorkflowInstance(
        identity=WorkflowIdentity(instance_id=uuid4(), definition_id=uuid4()),
        definition_id=uuid4(),
        state=WorkflowLifecycleState.CREATED,
    )
    assert instance.state == WorkflowLifecycleState.CREATED

    # Transitions
    instance = instance.transition_to(WorkflowLifecycleState.REGISTERED)
    assert instance.state == WorkflowLifecycleState.REGISTERED

    instance = instance.transition_to(WorkflowLifecycleState.READY)
    assert instance.state == WorkflowLifecycleState.READY

    instance = instance.transition_to(WorkflowLifecycleState.SCHEDULED)
    assert instance.state == WorkflowLifecycleState.SCHEDULED

    instance = instance.transition_to(WorkflowLifecycleState.RUNNING)
    assert instance.state == WorkflowLifecycleState.RUNNING

    instance = instance.transition_to(WorkflowLifecycleState.WAITING)
    assert instance.state == WorkflowLifecycleState.WAITING

    instance = instance.transition_to(WorkflowLifecycleState.RUNNING)
    instance = instance.transition_to(WorkflowLifecycleState.PAUSED)
    assert instance.state == WorkflowLifecycleState.PAUSED

    instance = instance.transition_to(WorkflowLifecycleState.RUNNING)
    instance = instance.transition_to(WorkflowLifecycleState.COMPENSATING)
    assert instance.state == WorkflowLifecycleState.COMPENSATING

    instance = instance.transition_to(WorkflowLifecycleState.FAILED)
    assert instance.state == WorkflowLifecycleState.FAILED

    instance = instance.transition_to(WorkflowLifecycleState.ARCHIVED)
    assert instance.state == WorkflowLifecycleState.ARCHIVED


def test_invalid_state_transitions_raise_error():
    """Verifies that unauthorized state transitions raise InvalidWorkflowStateTransitionError."""
    instance = WorkflowInstance(
        identity=WorkflowIdentity(instance_id=uuid4(), definition_id=uuid4()),
        definition_id=uuid4(),
        state=WorkflowLifecycleState.CREATED,
    )
    with pytest.raises(InvalidWorkflowStateTransitionError):
        # Cannot jump straight from CREATED to COMPLETED
        instance.transition_to(WorkflowLifecycleState.COMPLETED)

    with pytest.raises(InvalidWorkflowStateTransitionError):
        # Cannot transition from ARCHIVED
        archived = instance.model_copy(update={"state": WorkflowLifecycleState.ARCHIVED})
        archived.transition_to(WorkflowLifecycleState.RUNNING)


# ============================================================================
# 2. DAG Graph & Cycle Detection Tests
# ============================================================================

def test_dag_graph_acyclic_and_topological_sort():
    """Validates acyclic DAG topological ordering."""
    node1 = WorkflowNode(node_id="n1", name="Step 1", handler="h1")
    node2 = WorkflowNode(node_id="n2", name="Step 2", handler="h2")
    node3 = WorkflowNode(node_id="n3", name="Step 3", handler="h3")

    graph = WorkflowGraph(
        nodes={"n1": node1, "n2": node2, "n3": node3},
        edges=[
            WorkflowEdge(from_node="n1", to_node="n2"),
            WorkflowEdge(from_node="n2", to_node="n3"),
        ],
    )
    assert not graph.has_cycles()
    order = graph.get_topological_order()
    assert order == ["n1", "n2", "n3"]


def test_dag_graph_cycle_detection():
    """Detects cycles in workflow graph."""
    node1 = WorkflowNode(node_id="n1", name="Step 1", handler="h1")
    node2 = WorkflowNode(node_id="n2", name="Step 2", handler="h2")

    graph = WorkflowGraph(
        nodes={"n1": node1, "n2": node2},
        edges=[
            WorkflowEdge(from_node="n1", to_node="n2"),
            WorkflowEdge(from_node="n2", to_node="n1"),
        ],
    )
    assert graph.has_cycles()
    with pytest.raises(CyclicWorkflowGraphError):
        WorkflowValidator.validate_graph(graph)


# ============================================================================
# 3. Fluent Builders Tests
# ============================================================================

def test_fluent_builders():
    """Tests node, graph, definition, and request builders."""
    node = (
        WorkflowNodeBuilder("extract", "Extract Document")
        .with_type(WorkflowNodeType.TASK)
        .with_handler("extract_handler")
        .with_parameters({"format": "pdf"})
        .with_compensating_handler("cleanup_extract")
        .with_timeout(120.0)
        .with_retry_limit(2)
        .build()
    )
    assert node.node_id == "extract"
    assert node.parameters["format"] == "pdf"
    assert node.compensating_handler == "cleanup_extract"

    def_id = uuid4()
    wf_def = (
        WorkflowDefinitionBuilder("DocumentProcessingPipeline")
        .with_id(def_id)
        .with_description("E2E Document Processing")
        .with_version(2, 1, 0)
        .add_node(node)
        .build()
    )
    assert wf_def.name == "DocumentProcessingPipeline"
    assert wf_def.version.major == 2
    assert "extract" in wf_def.graph.nodes

    req = (
        WorkflowRequestBuilder(def_id)
        .with_input("doc_path", "/tmp/doc.pdf")
        .with_tenant("tenant-alpha")
        .with_max_duration(3600.0)
        .build()
    )
    assert req.definition_id == def_id
    assert req.input_data["doc_path"] == "/tmp/doc.pdf"
    assert req.context.tenant_id == "tenant-alpha"


# ============================================================================
# 4. Saga Orchestrator & Compensation Tests
# ============================================================================

@pytest.mark.asyncio
async def test_saga_orchestrator_forward_and_rollback():
    """Tests Saga execution with forward recording and LIFO rollback upon failure."""
    coordinator = CompensationCoordinator()
    saga = SagaOrchestrator(coordinator=coordinator)
    wf_id = uuid4()

    forward_log = []
    comp_log = []

    async def step1(data):
        forward_log.append("step1")
        return {"status": "ok1"}

    async def step1_comp(data):
        comp_log.append("undo_step1")
        return {"undone": 1}

    async def step2(data):
        forward_log.append("step2")
        raise RuntimeError("Simulated crash in step 2")

    async def step2_comp(data):
        comp_log.append("undo_step2")
        return {"undone": 2}

    saga.register_handler("step1_action", step1)
    saga.register_handler("step1_undo", step1_comp)
    saga.register_handler("step2_action", step2)
    saga.register_handler("step2_undo", step2_comp)

    node1 = WorkflowNode(
        node_id="n1",
        name="Step 1",
        node_type=WorkflowNodeType.SAGA_TRANSACTION,
        handler="step1_action",
        compensating_handler="step1_undo",
    )
    node2 = WorkflowNode(
        node_id="n2",
        name="Step 2",
        node_type=WorkflowNodeType.SAGA_TRANSACTION,
        handler="step2_action",
        compensating_handler="step2_undo",
    )

    # Step 1 succeeds
    out1 = await saga.execute_saga_step(wf_id, node1, {"foo": "bar"})
    assert out1["status"] == "ok1"
    assert len(coordinator.get_journal(wf_id)) == 1

    # Step 2 fails and automatically triggers reverse compensation
    with pytest.raises(RuntimeError, match="Simulated crash"):
        await saga.execute_saga_step(wf_id, node2, {"foo": "baz"})

    # Check that compensation executed in reverse order
    assert comp_log == ["undo_step1"]
    assert len(coordinator.get_journal(wf_id)) == 0


def test_missing_compensation_strict_mode():
    """Strict mode raises MissingCompensationPathError when compensating handler is absent."""
    coordinator = CompensationCoordinator(strict_mode=True)
    wf_id = uuid4()
    coordinator.record_step(
        workflow_id=wf_id,
        node_id="n1",
        action_name="action",
        compensating_handler=None,
        input_data={},
        output_data={},
    )
    with pytest.raises(MissingCompensationPathError):
        import asyncio
        asyncio.run(coordinator.execute_compensation(wf_id, lambda name: None))


# ============================================================================
# 5. Child Workflow & Hierarchy Tests
# ============================================================================

def test_child_workflow_manager_and_cascading_cancellation():
    """Tests parent-child linkage and recursive cascade cancellation."""
    mgr = ChildWorkflowManager()
    parent_id = uuid4()
    child1_id = uuid4()
    child2_id = uuid4()
    subchild_id = uuid4()

    mgr.register_child(parent_id, child1_id, "child_node_1")
    mgr.register_child(parent_id, child2_id, "child_node_2")
    mgr.register_child(child1_id, subchild_id, "subchild_node")

    assert mgr.get_parent(child1_id) == parent_id
    assert mgr.get_parent(subchild_id) == child1_id
    assert set(mgr.get_children(parent_id)) == {child1_id, child2_id}

    # Cascade cancellation
    to_cancel = mgr.cascade_cancellation(parent_id)
    assert set(to_cancel) == {child1_id, child2_id, subchild_id}

    # Orphan test
    orphan_id = uuid4()
    with pytest.raises(OrphanedChildWorkflowError):
        mgr.get_parent(orphan_id)


# ============================================================================
# 6. Signals, Timers, Waits & Gateways Tests
# ============================================================================

def test_signals_and_waits():
    """Tests signal emission/consumption and wait barrier tracking."""
    sig_mgr = SignalManager()
    wf_id = uuid4()

    sig_mgr.send_signal(wf_id, "APPROVED", {"approver": "alice"})
    assert sig_mgr.has_signal(wf_id, "APPROVED")

    sig = sig_mgr.consume_signal(wf_id, "APPROVED")
    assert sig is not None
    assert sig.payload["approver"] == "alice"
    assert not sig_mgr.has_signal(wf_id, "APPROVED")

    wait_mgr = WaitManager()
    wait_mgr.register_wait(wf_id, ["SIG_A", "SIG_B"])
    assert not wait_mgr.is_satisfied(wf_id)

    wait_mgr.satisfy_condition(wf_id, "SIG_A")
    assert not wait_mgr.is_satisfied(wf_id)

    wait_mgr.satisfy_condition(wf_id, "SIG_B")
    assert wait_mgr.is_satisfied(wf_id)


def test_timer_manager():
    """Tests timer registration and validation."""
    tm = TimerManager()
    wf_id = uuid4()
    timer = tm.register_timer(wf_id, "timer_node", delay_seconds=10.0)
    assert timer.delay_seconds == 10.0
    assert not tm.has_expired(timer.timer_id)

    with pytest.raises(InvalidTimerConfigurationError):
        tm.register_timer(wf_id, "invalid_timer", delay_seconds=-5.0)


# ============================================================================
# 7. Human in the Loop Approval Tests
# ============================================================================

def test_human_approval_workflow():
    """Tests human approval workflow engine lifecycle."""
    engine = ApprovalWorkflowEngine()
    wf_id = uuid4()
    task = engine.create_human_task(
        workflow_id=wf_id,
        node_id="review_step",
        title="Review Document Extraction",
        approvers=["lead_reviewer"],
    )
    assert task.status == HumanTaskStatus.PENDING

    # Approve
    decided = engine.decide_task(
        task_id=task.task_id,
        decision=HumanTaskDecision.APPROVED,
        reviewer_id="lead_reviewer",
        notes="High confidence score",
    )
    assert decided.status == HumanTaskStatus.APPROVED
    assert decided.reviewer_id == "lead_reviewer"


# ============================================================================
# 8. Replay & Migration Tests
# ============================================================================

@pytest.mark.asyncio
async def test_workflow_replay_engine():
    """Tests deterministic replay of historical events."""
    wf_id = uuid4()
    history = WorkflowHistory(instance_id=wf_id)
    history = history.append_event("NODE_COMPLETED", node_id="step1", payload={"data": 123})
    history = history.append_event("VARIABLE_SET", payload={"status": "verified"})
    history = history.append_event("STATE_TRANSITION", payload={"target_state": "RUNNING"})

    replay_engine = WorkflowReplayEngine()
    result = await replay_engine.replay(history)
    assert result.instance_id == wf_id
    assert result.events_replayed == 3
    assert result.last_lifecycle_state == WorkflowLifecycleState.RUNNING
    assert result.final_state.variables["status"] == "verified"
    assert "step1" in result.final_state.completed_nodes


def test_workflow_migration_engine():
    """Tests in-flight version migration and compatibility guard."""
    migration = WorkflowMigrationEngine()
    v1_0 = WorkflowVersion(major=1, minor=0, patch=0)
    v1_1 = WorkflowVersion(major=1, minor=1, patch=0)
    v2_0 = WorkflowVersion(major=2, minor=0, patch=0)

    # Compatible minor bump
    assert migration.can_migrate(v1_0, v1_1)
    # Incompatible major breaking change
    assert not migration.can_migrate(v1_0, v2_0)

    # In-flight migration execution
    wf_id = uuid4()
    def_v1 = (
        WorkflowDefinitionBuilder("Pipeline")
        .with_version(1, 0, 0)
        .add_node(WorkflowNode(node_id="n1", name="N1", handler="h1"))
        .build()
    )
    def_v1_1 = (
        WorkflowDefinitionBuilder("Pipeline")
        .with_version(1, 1, 0)
        .add_node(WorkflowNode(node_id="n1", name="N1", handler="h1"))
        .build()
    )
    instance = WorkflowInstance(
        identity=WorkflowIdentity(instance_id=wf_id, definition_id=def_v1.definition_id, version=v1_0),
        definition_id=def_v1.definition_id,
        state=WorkflowLifecycleState.RUNNING,
    )

    migrated = migration.migrate_instance(instance, def_v1_1)
    assert migrated.identity.version.minor == 1
    assert migrated.state == WorkflowLifecycleState.RUNNING

    # Attempt invalid migration
    def_v2 = (
        WorkflowDefinitionBuilder("Pipeline")
        .with_version(2, 0, 0)
        .build()
    )
    with pytest.raises(InvalidWorkflowMigrationError):
        migration.migrate_instance(instance, def_v2)


# ============================================================================
# 9. Adapters Tests
# ============================================================================

@pytest.mark.asyncio
async def test_workflow_adapters():
    """Tests all 7 workflow bridges/adapters."""
    coord = WorkflowCoordinationAdapter()
    coord_res = await coord.coordinate_agents("Analyze Doc")
    assert coord_res["status"] == "COMPLETED"

    planner = WorkflowPlannerAdapter()
    plan_res = await planner.plan_goal("Formulate Plan")
    assert plan_res["status"] == "SUCCESS"

    execution = WorkflowExecutionAdapter()
    exec_res = await execution.execute_task("t1", "h1", {"in": 1})
    assert exec_res["status"] == "COMPLETED"

    recovery = WorkflowRecoveryAdapter()
    rec_res = await recovery.handle_workflow_failure(uuid4(), "Timeout")
    assert rec_res["status"] == "RECOVERED"

    reflection = WorkflowReflectionAdapter()
    ref_res = await reflection.reflect_on_workflow(uuid4(), {"latency": 50})
    assert ref_res["status"] == "EVALUATED"

    decision = WorkflowDecisionAdapter()
    dec_res = await decision.evaluate_workflow_policies("proc_wf", {})
    assert dec_res["is_authorized"] is True

    memory = WorkflowMemoryAdapter()
    wf_id = uuid4()
    await memory.store_workflow_summary(wf_id, {"summary": "done"})
    mem_ctx = await memory.retrieve_workflow_context(wf_id)
    assert isinstance(mem_ctx, dict)


# ============================================================================
# 10. Telemetry, Metrics, Serialization, & Cache Tests
# ============================================================================

def test_telemetry_and_metrics():
    """Tests OpenTelemetry trace context and Cloud Monitoring metrics."""
    ctx = WorkflowTelemetry.generate_trace_context("corr-123")
    assert "traceparent" in ctx
    assert ctx["correlation-id"] == "corr-123"

    extracted = WorkflowTelemetry.extract_trace_context(ctx)
    assert extracted["correlation-id"] == "corr-123"

    metrics = WorkflowMetricsCollector()
    metrics.record_workflow_started()
    metrics.record_workflow_completed(150.0)
    metrics.record_workflow_failed()
    metrics.record_saga_executed()
    metrics.record_compensation_executed()
    metrics.record_human_approval_requested()
    metrics.record_human_approval_completed()

    snap = metrics.get_snapshot()
    assert snap.total_workflows_started == 1
    assert snap.total_workflows_completed == 1
    assert snap.total_workflows_failed == 1
    assert snap.total_sagas_executed == 1
    assert snap.total_compensations_executed == 1
    assert snap.total_human_approvals_requested == 1
    assert snap.total_human_approvals_completed == 1
    assert snap.average_workflow_duration_ms == 150.0

    gcp_export = metrics.export_gcp_metrics()
    assert len(gcp_export) > 0


def test_serialization_and_cache():
    """Tests Pydantic v2 JSON serialization and WorkflowCache LRU/TTL."""
    version = WorkflowVersion(major=1, minor=2, patch=3)
    json_str = WorkflowSerializer.serialize_to_json(version)
    deserialized = WorkflowSerializer.deserialize_from_json(json_str, WorkflowVersion)
    assert deserialized.major == 1
    assert deserialized.minor == 2
    assert deserialized.patch == 3

    pubsub_msg = WorkflowSerializer.to_pubsub_message(version)
    assert "attributes" in pubsub_msg
    assert "data" in pubsub_msg

    # LRU Cache
    cache = WorkflowCache(capacity=2, default_ttl_seconds=60.0)
    cache.set("k1", "v1")
    cache.set("k2", "v2")
    assert cache.get("k1") == "v1"
    cache.set("k3", "v3")  # Evicts k2 (MRU was k1)
    assert cache.get("k2") is None
    assert cache.get("k3") == "v3"
    assert cache.get("k1") == "v1"


# ============================================================================
# 11. End-to-End Workflow Execution & Factory Tests
# ============================================================================

@pytest.mark.asyncio
async def test_end_to_end_workflow_execution():
    """Tests complete end-to-end execution of a 3-node workflow via WorkflowEngine."""
    runtime = WorkflowFactory.create_runtime()
    await runtime.initialize()

    # Create definition
    node1 = WorkflowNode(node_id="extract", name="Extract", handler="extract_handler")
    node2 = WorkflowNode(node_id="classify", name="Classify", handler="classify_handler")
    node3 = WorkflowNode(node_id="persist", name="Persist", handler="persist_handler")

    wf_def = (
        WorkflowDefinitionBuilder("DocumentProcessing")
        .add_node(node1)
        .add_node(node2)
        .add_node(node3)
        .add_edge("extract", "classify")
        .add_edge("classify", "persist")
        .build()
    )
    runtime.registry.register_definition(wf_def)

    req = (
        WorkflowRequestBuilder(wf_def.definition_id)
        .with_input("document_id", "DOC-999")
        .build()
    )

    result = await runtime.engine.start_workflow(req)
    assert result.lifecycle_state == WorkflowLifecycleState.COMPLETED
    assert result.statistics.total_nodes_executed == 3
    assert result.errors == []

    # Pause, Resume, and Cancel workflows
    instance = await runtime.engine.manager.create_instance(wf_def.definition_id)
    await runtime.engine.manager.start_instance(instance.instance_id)
    paused = await runtime.engine.pause_workflow(instance.instance_id)
    assert paused.state == WorkflowLifecycleState.PAUSED

    resumed = await runtime.engine.resume_workflow(instance.instance_id)
    assert resumed.state == WorkflowLifecycleState.RUNNING

    cancelled = await runtime.engine.cancel_workflow(instance.instance_id)
    assert cancelled.state == WorkflowLifecycleState.CANCELLED

    await runtime.shutdown()
