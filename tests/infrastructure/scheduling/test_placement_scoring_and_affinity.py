"""Tests for Hard Constraints, Affinity, Policies, and Placement Scoring."""

from app.infrastructure.executions.workload import (
    ResourceRequirements,
    WorkloadRequest,
)
from app.infrastructure.workers.models import (
    ResourceCapacity,
    Worker,
    WorkerStatus,
)
from app.infrastructure.workers.capabilities import WorkerCapabilityRegistry
from app.infrastructure.workers.leases import WorkerLeaseManager
from app.infrastructure.scheduling.constraints import ConstraintEvaluator
from app.infrastructure.scheduling.affinity import AffinityEngine
from app.infrastructure.scheduling.scoring import PlacementScoringEngine


def test_constraint_evaluator():
    cap_reg = WorkerCapabilityRegistry()
    lease_mgr = WorkerLeaseManager()
    evaluator = ConstraintEvaluator(cap_reg, lease_mgr)

    worker = Worker(
        worker_id="wrk-c-1",
        region_id="us-east-1",
        cluster_id="cls-1",
        status=WorkerStatus.AVAILABLE,
        capabilities={"document.ocr", "gpu.cuda"},
        resource_capacity=ResourceCapacity(cpu_cores=4.0, memory_gb=16.0, gpu_count=1),
        tenant_restrictions=["tenant-allowed"],
    )
    cap_reg.register_capabilities(worker.worker_id, worker.capabilities)
    lease_mgr.issue_lease(worker.worker_id, cluster_id="cls-1")

    # 1. Matching workload
    valid_req = WorkloadRequest(
        workload_id="w-1",
        tenant_id="tenant-allowed",
        required_capabilities={"document.ocr"},
        resource_requirements=ResourceRequirements(cpu_cores=2.0, memory_gb=8.0),
    )
    ok, errs = evaluator.evaluate_worker(worker, valid_req)
    assert ok is True
    assert len(errs) == 0

    # 2. Ineligible tenant
    ineligible_tenant_req = WorkloadRequest(
        workload_id="w-2",
        tenant_id="tenant-blocked",
    )
    ok, errs = evaluator.evaluate_worker(worker, ineligible_tenant_req)
    assert ok is False
    assert any("restricted" in e for e in errs)

    # 3. Missing capability
    missing_cap_req = WorkloadRequest(
        workload_id="w-3",
        tenant_id="tenant-allowed",
        required_capabilities={"gpu.a100"},
    )
    ok, errs = evaluator.evaluate_worker(worker, missing_cap_req)
    assert ok is False
    assert any("gpu.a100" in e for e in errs)


def test_affinity_and_scoring_engine():
    aff_engine = AffinityEngine()
    cap_reg = WorkerCapabilityRegistry()
    scoring_engine = PlacementScoringEngine(
        capability_registry=cap_reg, affinity_engine=aff_engine
    )

    w1 = Worker(
        worker_id="wrk-score-1",
        region_id="us-east-1",
        cluster_id="cls-1",
        status=WorkerStatus.AVAILABLE,
        capabilities={"document.ocr", "gpu.a100"},
        labels={"tier": "high_throughput", "zone": "a"},
        resource_capacity=ResourceCapacity(cpu_cores=32.0, memory_gb=128.0, worker_slots=20),
    )
    w2 = Worker(
        worker_id="wrk-score-2",
        region_id="us-west-2",
        cluster_id="cls-2",
        status=WorkerStatus.AVAILABLE,
        capabilities={"document.ocr"},
        labels={"tier": "standard"},
        resource_capacity=ResourceCapacity(cpu_cores=8.0, memory_gb=32.0, worker_slots=5),
    )
    cap_reg.register_capabilities(w1.worker_id, w1.capabilities)
    cap_reg.register_capabilities(w2.worker_id, w2.capabilities)

    workload = WorkloadRequest(
        workload_id="w-scoring",
        tenant_id="tenant-1",
        required_capabilities={"document.ocr"},
        optional_capabilities={"gpu.a100"},
        affinity_tags={"tier": "high_throughput"},
        region_preferences=["us-east-1"],
        data_locality_uri="s3://docutask-us-east-1-store/file.pdf",
    )

    ranked = scoring_engine.rank_candidates([w1, w2], workload)
    assert len(ranked) == 2
    # w1 should rank significantly higher due to resource headroom, optional capability, affinity tag, and data locality
    assert ranked[0].worker_id == "wrk-score-1"
    assert ranked[0].total_score > ranked[1].total_score
