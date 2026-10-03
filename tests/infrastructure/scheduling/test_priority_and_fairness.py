"""Tests for Priority Scheduling, Anti-Starvation Aging, and Multi-Tenant Fairness."""

from datetime import datetime, timezone, timedelta
from app.infrastructure.executions.workload import (
    WorkloadPriority,
    WorkloadRequest,
)
from app.infrastructure.scheduling.priorities import PriorityScheduler
from app.infrastructure.scheduling.fairness import FairnessScheduler


def test_priority_scheduler_and_aging():
    scheduler = PriorityScheduler(aging_rate_per_sec=2.0)

    # High priority recently submitted
    w_high = WorkloadRequest(
        workload_id="w-high",
        tenant_id="tenant-1",
        priority=WorkloadPriority.HIGH,
        submitted_at=datetime.now(timezone.utc),
    )

    # Low priority submitted 500 seconds ago -> base=50 + 500*2 = 1050 > high base (500)
    w_low_aged = WorkloadRequest(
        workload_id="w-low-aged",
        tenant_id="tenant-1",
        priority=WorkloadPriority.LOW,
        submitted_at=datetime.now(timezone.utc) - timedelta(seconds=500),
    )

    ordered = scheduler.order_workloads_by_priority([w_high, w_low_aged])
    # Low priority aged task should jump ahead of fresh high priority task
    assert ordered[0].workload_id == "w-low-aged"


def test_fairness_scheduler_interleaving():
    fairness = FairnessScheduler(default_quantum=5)

    # Tenant A has 3 jobs, Tenant B has 2 jobs
    w_a1 = WorkloadRequest(workload_id="a1", tenant_id="tenant-A")
    w_a2 = WorkloadRequest(workload_id="a2", tenant_id="tenant-A")
    w_a3 = WorkloadRequest(workload_id="a3", tenant_id="tenant-A")
    w_b1 = WorkloadRequest(workload_id="b1", tenant_id="tenant-B")
    w_b2 = WorkloadRequest(workload_id="b2", tenant_id="tenant-B")

    ordered = fairness.sort_workloads_fairly([w_a1, w_a2, w_a3, w_b1, w_b2])
    # Should interleave: A, B, A, B, A
    tenant_order = [w.tenant_id for w in ordered]
    assert tenant_order == ["tenant-A", "tenant-B", "tenant-A", "tenant-B", "tenant-A"]
