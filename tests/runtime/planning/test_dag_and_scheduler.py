"""Tests for Mutable Execution DAG, Scheduler Leasing, Preemption, and Adaptive Replanning."""

import pytest
from app.runtime.planning.mutable_dag import MutableExecutionDAG, DAGNode, DAGNodeStatus, DAGMutationType
from app.runtime.planning.capability_discovery import CapabilityDiscoveryEngine
from app.runtime.planning.scheduler import EnterpriseResourceScheduler, QueuePriority, WorkerStatus
from app.runtime.planning.adaptive_replanner import AdaptiveReplanningEngine, ReplanningTrigger, ReplanningTriggerType


def test_mutable_dag_split_and_acyclic():
    dag = MutableExecutionDAG(mission_id="m_dag", strategy_id="s1")
    n1 = DAGNode(name="Ingest", capability_id="ocr_tesseract_v5", provider="tesseract_local")
    n2 = DAGNode(name="Extract", capability_id="llm_flash_lite", provider="gemini_flash_lite")
    n3 = DAGNode(name="Validate", capability_id="fast_rule_engine", provider="ast_validator")

    dag.add_node(n1)
    dag.add_node(n2)
    dag.add_node(n3)
    dag.add_edge(n1.node_id, n2.node_id)
    dag.add_edge(n2.node_id, n3.node_id)

    assert dag.validate_acyclic() is True
    assert len(dag.get_topological_order()) == 3

    # Split n2 into 2 shards
    shards = dag.split_node(n2.node_id, 2, "Parallelize extraction")
    assert len(shards) == 2
    assert dag.validate_acyclic() is True
    assert len(dag.mutation_history) == 1
    assert dag.mutation_history[0].mutation_type == DAGMutationType.NODE_SPLIT


def test_scheduler_leasing_and_release():
    caps = CapabilityDiscoveryEngine()
    scheduler = EnterpriseResourceScheduler(caps, initial_workers=4)

    status = scheduler.get_cluster_status()
    assert status["total_workers"] == 4
    assert status["idle_workers"] == 4

    # Acquire lease
    lease = scheduler.acquire_lease("m1", "step_1", "ocr_tesseract_v5", priority=QueuePriority.HIGH)
    assert lease is not None
    assert lease.is_active is True

    status_after = scheduler.get_cluster_status()
    assert status_after["idle_workers"] == 3
    assert status_after["busy_workers"] == 1

    # Release lease
    assert scheduler.release_lease(lease.lease_id) is True
    status_released = scheduler.get_cluster_status()
    assert status_released["idle_workers"] == 4


def test_scheduler_preemption():
    caps = CapabilityDiscoveryEngine()
    scheduler = EnterpriseResourceScheduler(caps, initial_workers=1)

    # Fill single worker with LOW priority task
    lease_low = scheduler.acquire_lease("m_low", "step_l", "ocr_tesseract_v5", priority=QueuePriority.LOW)
    assert lease_low is not None

    # Try acquiring with HIGH priority -> should fail without preemption
    lease_high = scheduler.acquire_lease("m_high", "step_h", "ocr_tesseract_v5", priority=QueuePriority.HIGH)
    assert lease_high is None

    # Try acquiring with CRITICAL priority -> should preempt LOW priority lease
    lease_crit = scheduler.acquire_lease("m_crit", "step_c", "ocr_tesseract_v5", priority=QueuePriority.CRITICAL)
    assert lease_crit is not None
    assert lease_low.preempted is True


def test_adaptive_replanner_on_low_confidence():
    caps = CapabilityDiscoveryEngine()
    dag = MutableExecutionDAG(mission_id="m_replan", strategy_id="s1")
    n1 = DAGNode(name="OCR Step", capability_id="ocr_tesseract_v5", provider="tesseract_local")
    dag.add_node(n1)

    replanner = AdaptiveReplanningEngine(caps)
    trigger = ReplanningTrigger(
        trigger_type=ReplanningTriggerType.LOW_CONFIDENCE,
        node_id=n1.node_id,
        metric_value=0.62,
        threshold=0.85,
        rationale="Tesseract OCR produced noisy results.",
    )

    result = replanner.handle_trigger(dag, trigger)
    assert n1.capability_id == "ocr_cloud_vision"
    assert "Google Cloud Neural Vision" in result.strategy_adaptation or "Cloud" in result.strategy_adaptation
