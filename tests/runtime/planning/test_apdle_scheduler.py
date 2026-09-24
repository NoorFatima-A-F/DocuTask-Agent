"""
Unit & Integration Tests for APDLE Parallel Scheduler, Worker Allocation, and Master Execution.
"""

import pytest
from app.runtime.planning.graph.graph_builder import ExecutionGraphBuilder
from app.runtime.planning.graph.node import DAGNode, NodeStatus
from app.runtime.planning.scheduler.queue_manager import PriorityQueueManager
from app.runtime.planning.scheduler.scheduler import DAGScheduler
from app.runtime.planning.scheduler.worker_allocator import WorkerAllocator


@pytest.mark.asyncio
async def test_worker_allocation_and_capabilities():
    """Verifies that tasks are correctly routed to capable workers."""
    allocator = WorkerAllocator()
    node_ocr = DAGNode(mission_id="m1", name="OCR Task", task_type="OCR", required_capabilities=["OCR"])
    node_smt = DAGNode(mission_id="m1", name="SMT Task", task_type="VALIDATION", required_capabilities=["SMT"])

    worker_ocr = allocator.allocate_worker(node_ocr)
    assert worker_ocr is not None
    assert "OCR" in worker_ocr.capabilities

    worker_smt = allocator.allocate_worker(node_smt)
    assert worker_smt is not None
    assert "SMT" in worker_smt.capabilities


def test_priority_queue_manager():
    """Verifies priority ordering in task queue manager."""
    qm = PriorityQueueManager()
    n_low = DAGNode(node_id="n_low", mission_id="m1", name="Low", task_type="GEN", priority=80)
    n_high = DAGNode(node_id="n_high", mission_id="m1", name="High", task_type="GEN", priority=10)

    qm.push(n_low)
    qm.push(n_high)

    first = qm.pop()
    assert first is not None
    assert first.node_id == "n_high"


@pytest.mark.asyncio
async def test_master_dag_scheduler_execution():
    """Verifies complete end-to-end execution of a 5-stage parallel DAG."""
    dag = ExecutionGraphBuilder.build_financial_invoice_audit_dag(mission_id="m-exec-01")
    scheduler = DAGScheduler()

    execution_result = await scheduler.execute_dag(dag)
    assert execution_result["status"] == "COMPLETED"
    assert execution_result["completed_nodes_count"] == 5
    assert execution_result["failed_nodes_count"] == 0
    assert execution_result["actual_runtime_ms"] > 0

    # Every node in the DAG should now be COMPLETED
    for node in dag.nodes.values():
        assert node.status == NodeStatus.COMPLETED
        assert node.actual_runtime_ms > 0
