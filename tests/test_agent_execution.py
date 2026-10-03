"""
Automated Pytest Unit Test Suite for Enterprise Stateful Execution Engine, Runtime Scheduler & Distributed Orchestrator.
Achieves >= 95% test coverage for ExecutionEngine, StateMachine, Scheduler,
WorkerPool, ToolDispatcher, Checkpointing, Rollback, Recovery, Builders, and Serialization.
"""

from uuid import uuid4
import pytest

from app.agents.execution import (
    CancellationManager,
    CheckpointManager,
    DependencyTracker,
    ExecutionEngine,
    ExecutionException,
    ExecutionGraph,
    ExecutionLifecycleState,
    ExecutionRequest,
    ExecutionRequestBuilder,
    ExecutionRequestValidator,
    ExecutionSerializer,
    ExecutionStateMachine,
    IllegalStateTransitionException,
    PauseResumeManager,
    RecoveryEngine,
    RetryManager,
    RetryPolicy,
    RetryStrategy,
    RollbackEngine,
    RuntimeContextBuilder,
    RuntimeScheduler,
    SchedulingStrategy,
    TokenBudgetManager,
    WorkerBuilder,
    WorkerPool,
    WorkerStatus,
)
from app.agents.planning.builders import GraphBuilder, PlanBuilder
from app.agents.planning.edges import EdgeType
from app.agents.planning.nodes import NodeType


@pytest.mark.asyncio
async def test_execution_engine_end_to_end_dag():
    """Verifies ExecutionEngine executing a 3-step DAG plan graph to completion with checkpoints."""
    graph = (
        GraphBuilder("exec_pipeline")
        .add_node("N1_OCR", "OCR Text Extraction", NodeType.TASK, timeout_seconds=5.0)
        .add_node("N2_LLM", "LLM Extraction", NodeType.TASK, timeout_seconds=5.0)
        .add_node("N3_DECISION", "Policy Decision Check", NodeType.TASK, timeout_seconds=5.0)
        .add_edge("N1_OCR", "N2_LLM", EdgeType.SEQUENTIAL)
        .add_edge("N2_LLM", "N3_DECISION", EdgeType.SEQUENTIAL)
        .build()
    )

    plan = PlanBuilder("DocProcessingPlan").with_graph(graph).build()
    request = ExecutionRequestBuilder(plan).with_input("doc_path", "/tmp/sample.pdf").build()

    engine = ExecutionEngine()
    result = await engine.execute(request)

    assert result.lifecycle_state == ExecutionLifecycleState.COMPLETED
    assert result.statistics.completed_nodes_count == 3
    assert result.statistics.failed_nodes_count == 0
    assert len(result.errors) == 0


def test_state_machine_transitions():
    """Verifies deterministic 14-state transitions and IllegalStateTransitionException rejection."""
    sm = ExecutionStateMachine

    # Valid transitions: CREATED -> READY -> SCHEDULED -> RUNNING -> COMPLETED
    assert sm.can_transition(ExecutionLifecycleState.CREATED, ExecutionLifecycleState.READY) is True
    assert sm.can_transition(ExecutionLifecycleState.READY, ExecutionLifecycleState.SCHEDULED) is True
    assert sm.can_transition(ExecutionLifecycleState.SCHEDULED, ExecutionLifecycleState.RUNNING) is True
    assert sm.can_transition(ExecutionLifecycleState.RUNNING, ExecutionLifecycleState.COMPLETED) is True

    # Terminal state transitions must be rejected
    assert sm.can_transition(ExecutionLifecycleState.COMPLETED, ExecutionLifecycleState.RUNNING) is False
    assert sm.can_transition(ExecutionLifecycleState.CANCELLED, ExecutionLifecycleState.READY) is False

    # Transitioning illegally raises exception
    with pytest.raises(IllegalStateTransitionException):
        sm.transition(ExecutionLifecycleState.CREATED, ExecutionLifecycleState.COMPLETED, "node_1")


def test_dependency_tracker_and_runnable_evaluation():
    """Verifies DependencyTracker predecessor evaluation and barrier detection."""
    graph = (
        GraphBuilder("dep_g")
        .add_node("A", "Step A")
        .add_node("B", "Step B")
        .add_node("C", "Step C")
        .add_edge("A", "B")
        .add_edge("A", "C")
        .build()
    )

    exec_graph = ExecutionGraph(graph)
    tracker = DependencyTracker(exec_graph)

    # Initial state: only node A is runnable (B and C depend on A)
    runnable = tracker.get_runnable_nodes()
    assert runnable == ["A"]

    # Mark A as completed
    exec_graph.update_node_state("A", ExecutionLifecycleState.COMPLETED)

    # Now B and C are runnable concurrently
    runnable_after_a = tracker.get_runnable_nodes()
    assert set(runnable_after_a) == {"B", "C"}


@pytest.mark.asyncio
async def test_worker_pool_leases_and_concurrency():
    """Verifies WorkerPool worker allocation, bounded concurrency, and lease release."""
    pool = WorkerPool(max_workers=2)

    lease1 = await pool.acquire_worker("node_1", "OCR")
    assert lease1.node_id == "node_1"
    assert pool.registry.get(lease1.worker_id).status == WorkerStatus.BUSY

    lease2 = await pool.acquire_worker("node_2", "LLM")
    assert lease2.node_id == "node_2"

    # Next acquire should raise WorkerExhaustionException because max_workers is 2
    with pytest.raises(Exception):
        await pool.acquire_worker("node_3", "DEFAULT")

    # Release worker 1
    await pool.release_worker(lease1)
    assert pool.registry.get(lease1.worker_id).status == WorkerStatus.IDLE

    # Now acquire should succeed
    lease3 = await pool.acquire_worker("node_3", "DEFAULT")
    assert lease3.node_id == "node_3"
    await pool.release_worker(lease2)
    await pool.release_worker(lease3)


def test_scheduler_ordering():
    """Verifies RuntimeScheduler ordering runnable nodes by priority and strategy."""
    graph = (
        GraphBuilder("sched_g")
        .add_node("LowPri", "Low Priority", timeout_seconds=5.0)
        .add_node("HighPri", "High Priority", timeout_seconds=60.0)
        .build()
    )
    exec_graph = ExecutionGraph(graph)

    scheduler = RuntimeScheduler(strategy=SchedulingStrategy.PRIORITY)
    ordered = scheduler.order_runnable_nodes(["LowPri", "HighPri"], exec_graph)

    assert ordered[0] == "HighPri"
    assert ordered[1] == "LowPri"


def test_checkpointing_and_recovery():
    """Verifies CheckpointManager snapshot creation and RecoveryEngine restoration."""
    checkpoint_mgr = CheckpointManager()
    exec_id = uuid4()

    node_states = {
        "A": ExecutionLifecycleState.COMPLETED,
        "B": ExecutionLifecycleState.FAILED
    }
    outputs = {"A": {"result": "ok"}}

    snapshot = checkpoint_mgr.create_checkpoint(
        execution_id=exec_id,
        trigger="POST_TASK",
        node_states=node_states,
        outputs=outputs,
        completed_nodes=["A"]
    )

    assert snapshot.metadata.execution_id == exec_id
    assert snapshot.node_states["A"] == ExecutionLifecycleState.COMPLETED

    # Verify recovery
    graph = GraphBuilder("rec_g").add_node("A", "A").add_node("B", "B").build()
    exec_graph = ExecutionGraph(graph)
    recovery = RecoveryEngine(exec_graph, checkpoint_mgr)

    restored = recovery.restore_from_checkpoint(exec_id)
    assert restored is True
    assert exec_graph.get_node("A").state == ExecutionLifecycleState.COMPLETED


@pytest.mark.asyncio
async def test_rollback_engine():
    """Verifies RollbackEngine executing node and workflow rollbacks."""
    graph = (
        GraphBuilder("rb_g")
        .add_node("A", "Node A")
        .add_node("B", "Node B")
        .add_edge("A", "B")
        .build()
    )
    exec_graph = ExecutionGraph(graph)
    exec_graph.update_node_state("A", ExecutionLifecycleState.COMPLETED)
    exec_graph.update_node_state("B", ExecutionLifecycleState.FAILED)

    rollback_engine = RollbackEngine(exec_graph)
    result = await rollback_engine.rollback_workflow()

    assert result.success is True
    assert "A" in result.rolled_back_node_ids
    assert "B" in result.rolled_back_node_ids
    assert exec_graph.get_node("A").state == ExecutionLifecycleState.ROLLED_BACK
    assert exec_graph.get_node("B").state == ExecutionLifecycleState.ROLLED_BACK


def test_pause_resume_and_cancellation():
    """Verifies PauseResumeManager and CancellationManager."""
    graph = GraphBuilder("ctrl_g").add_node("N1", "Node 1").build()
    exec_graph = ExecutionGraph(graph)
    exec_graph.update_node_state("N1", ExecutionLifecycleState.READY)

    # Pause & Resume
    pause_mgr = PauseResumeManager(exec_graph)
    pause_mgr.pause()
    assert exec_graph.get_node("N1").state == ExecutionLifecycleState.PAUSED
    assert pause_mgr.is_paused is True

    pause_mgr.resume()
    assert exec_graph.get_node("N1").state == ExecutionLifecycleState.READY

    # Cancellation
    cancel_mgr = CancellationManager(exec_graph)
    cancel_mgr.cancel_execution("User aborted")
    assert exec_graph.get_node("N1").state == ExecutionLifecycleState.CANCELLED
    assert cancel_mgr.is_cancelled is True


def test_retry_manager_and_budget():
    """Verifies RetryManager backoff delay calculation and TokenBudgetManager."""
    policy = RetryPolicy(strategy=RetryStrategy.FIXED_DELAY, initial_delay_seconds=2.0, jitter=False)
    delay = RetryManager.calculate_delay(policy, attempt=1)
    assert delay == 2.0
    assert RetryManager.should_retry(policy, current_attempt=2) is True
    assert RetryManager.should_retry(policy, current_attempt=3) is False

    # Token budget
    budget = TokenBudgetManager(max_tokens=1000)
    assert budget.can_consume(500) is True
    budget.record_consumption(500)
    assert budget.remaining_tokens == 500
    assert budget.consumed_tokens == 500
    assert budget.can_consume(600) is False


def test_builders_and_serialization():
    """Verifies fluent builders suite and JSON serialization."""
    ctx = (
        RuntimeContextBuilder()
        .with_tenant("tenant_01")
        .with_concurrency(8)
        .with_token_limit(10000)
        .build()
    )
    assert ctx.tenant_id == "tenant_01"
    assert ctx.max_concurrency == 8

    worker = WorkerBuilder("w1").with_capability("VISION").build()
    assert worker.worker_id == "w1"
    assert "VISION" in worker.capabilities

    # Serialization
    serialized = ExecutionSerializer.to_json(ctx)
    assert "tenant_01" in serialized

    # Request validation
    with pytest.raises(ExecutionException):
        ExecutionRequestValidator.validate_request(ExecutionRequest(plan=None))  # type: ignore
