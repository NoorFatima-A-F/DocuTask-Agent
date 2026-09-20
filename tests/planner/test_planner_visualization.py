"""
Pytest Suite for Phase 13.2 Autonomous Planner Execution Visualization (APEV-DAG).
Tests 14-state lifecycle, goal decomposition, DAG generation, live mutation, scheduling, critical path, and decision ledger.
"""

import pytest
from app.runtime.planner_visualization.planner_lifecycle.lifecycle_engine import PlannerLifecycleEngine
from app.runtime.planner_visualization.planner_lifecycle.goal_analyzer import GoalAnalysisEngine
from app.runtime.planner_visualization.planner_lifecycle.task_decomposer import TaskDecompositionEngine
from app.runtime.planner_visualization.dag.dag_engine import DAGBuilderEngine
from app.runtime.planner_visualization.dag.dag_mutator import DAGMutationEngine
from app.runtime.planner_visualization.dag.critical_path import CriticalPathEngine
from app.runtime.planner_visualization.scheduler.scheduler_engine import SchedulerEngine
from app.runtime.planner_visualization.scheduler.queue_manager import RuntimeQueueManager
from app.runtime.planner_visualization.worker_assignment.worker_assigner import WorkerAssignmentEngine
from app.runtime.planner_visualization.replanning.replanning_coordinator import ReplanningCoordinator
from app.runtime.planner_visualization.metrics.planner_metrics import PlannerMetricsCalculator
from app.runtime.planner_visualization.metrics.decision_ledger import PlannerDecisionLedger
from app.runtime.planner_visualization.api.planner_api_service import PlannerAPIService
from app.runtime.planner_visualization.ui_models.models import PlannerStateEnum, TaskNodeType, TaskExecutionState


def test_planner_lifecycle_state_machine():
    engine = PlannerLifecycleEngine(mission_id="test-m01")
    assert engine.current_state == PlannerStateEnum.CREATED

    # Advance state
    engine.transition_to(PlannerStateEnum.INITIALIZING, reason="Setting up planner runtime")
    assert engine.current_state == PlannerStateEnum.INITIALIZING

    engine.transition_to(PlannerStateEnum.CONTEXT_LOADING, reason="Loading context")
    engine.transition_to(PlannerStateEnum.GOAL_ANALYSIS, reason="Analyzing goal")
    assert engine.current_state == PlannerStateEnum.GOAL_ANALYSIS

    timeline = engine.get_timeline()
    assert len(timeline) >= 4
    assert timeline[-1]["to_state"] == "GOAL_ANALYSIS"


def test_goal_analysis_and_task_decomposition():
    goal_eng = GoalAnalysisEngine(mission_id="test-m01")
    goal = goal_eng.analyze_goal("Process audit invoices")
    assert goal.priority == "HIGH"
    assert len(goal.sub_objectives) >= 4
    assert len(goal.constraints) >= 4

    decomp = TaskDecompositionEngine(mission_id="test-m01")
    tasks = decomp.decompose(goal.title)
    assert len(tasks) == 9
    assert any(t.node_type == TaskNodeType.PARALLEL for t in tasks)
    assert any(t.node_type == TaskNodeType.JOIN for t in tasks)


def test_dag_generation_and_critical_path():
    dag_builder = DAGBuilderEngine(mission_id="test-m01")
    snapshot = dag_builder.get_snapshot()

    assert snapshot.total_nodes == 9
    assert len(snapshot.edges) == 9
    assert len(snapshot.critical_path) > 0
    assert snapshot.critical_path_duration_ms > 0

    cpm = CriticalPathEngine.compute_critical_path(snapshot.nodes, snapshot.edges)
    assert len(cpm["critical_path_nodes"]) > 0
    assert len(cpm["bottlenecks"]) > 0


def test_dag_live_mutation_and_replanning():
    dag_builder = DAGBuilderEngine(mission_id="test-m01")
    mutator = DAGMutationEngine(dag_builder)

    # Test split node
    split_res = mutator.split_node("node_extract_schema", num_splits=2)
    assert split_res["status"] == "SUCCESS"
    assert "node_extract_schema_split_1" in dag_builder.nodes
    assert "node_extract_schema_split_2" in dag_builder.nodes

    # Test recovery node injection
    replanner = ReplanningCoordinator(dag_builder, mutator)
    replan_res = replanner.trigger_replan_on_failure(
        failed_node_id="node_ocr_chunk_1",
        reason="Low contrast on raster scan",
        alternative_strategy="ENHANCED_CONTRAST_OCR",
    )
    assert replan_res["status"] == "SUCCESS"
    assert "node_ocr_chunk_1_recovery" in dag_builder.nodes


def test_scheduler_queues_and_worker_assignment():
    scheduler = SchedulerEngine(mission_id="test-m01")
    status = scheduler.get_scheduler_status()
    assert status["total_workers"] >= 6
    assert status["concurrency_limit"] == 8

    dispatch = scheduler.dispatch_task("task-new-01", "OCR_EXTRACTION", "OCR_EXTRACTION")
    assert dispatch["status"] == "DISPATCHED"

    queue_mgr = RuntimeQueueManager(mission_id="test-m01")
    queues = queue_mgr.get_queues()
    assert "WAITING" in queues["counts"]
    assert "RUNNING" in queues["counts"]
    assert "COMPLETED" in queues["counts"]

    assigner = WorkerAssignmentEngine(mission_id="test-m01")
    assignments = assigner.get_assignments()
    assert len(assignments) >= 6
    assert all(a.capability_match_score >= 0.8 for a in assignments)


def test_planner_metrics_and_decision_ledger():
    dag_builder = DAGBuilderEngine(mission_id="test-m01")
    calc = PlannerMetricsCalculator(dag_builder)
    metrics = calc.compute_metrics()

    assert metrics.tasks_generated == 9
    assert metrics.critical_path_ms > 0
    assert metrics.parallelism_factor >= 1.0

    ledger = PlannerDecisionLedger(mission_id="test-m01")
    decisions = ledger.get_decisions()
    assert len(decisions) >= 3
    assert all(d.truth_ledger_hash for d in decisions)
    assert all(d.confidence >= 0.9 for d in decisions)


def test_planner_api_service_aggregation():
    service = PlannerAPIService.get_instance("mission-test-agg")
    state = service.get_state()
    assert "current_state" in state

    dag = service.get_dag_snapshot()
    assert len(dag["nodes"]) == 9

    workers = service.get_workers()
    assert len(workers) >= 6

    metrics = service.get_metrics()
    assert metrics["tasks_generated"] == 9
