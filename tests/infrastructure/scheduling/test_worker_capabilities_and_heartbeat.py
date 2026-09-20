"""Tests for Worker Capabilities, Leases, Heartbeat, and Registry."""

from datetime import datetime, timezone, timedelta
import tempfile

from app.infrastructure.workers.models import (
    ResourceCapacity,
    Worker,
    WorkerLease,
    WorkerStatus,
    WorkerType,
)
from app.infrastructure.workers.capabilities import WorkerCapabilityRegistry
from app.infrastructure.workers.leases import WorkerLeaseManager
from app.infrastructure.workers.heartbeat import (
    WorkerHeartbeatManager,
    WorkerHeartbeatPayload,
)
from app.infrastructure.workers.drain import WorkerDrainManager
from app.infrastructure.workers.registry import WorkerRegistry


def test_worker_capability_registry():
    cap_reg = WorkerCapabilityRegistry()
    cap_reg.register_capabilities(
        "wrk-1", {"workflow.execute", "gpu.cuda", "gpu.a100", "compliance.hipaa"}
    )
    cap_reg.register_capabilities(
        "wrk-2", {"document.ocr", "gpu.cuda", "gpu.t4"}
    )

    assert cap_reg.satisfies_capabilities("wrk-1", {"workflow.execute", "gpu.cuda"}) is True
    assert cap_reg.satisfies_capabilities("wrk-2", {"gpu.a100"}) is False

    # Matching score with optional capabilities
    score = cap_reg.calculate_capability_match_score(
        "wrk-1",
        mandatory={"workflow.execute"},
        optional={"gpu.a100", "memory.high"},
    )
    assert score > 1.0

    # Query workers
    cuda_workers = cap_reg.query_workers({"gpu.cuda"})
    assert "wrk-1" in cuda_workers and "wrk-2" in cuda_workers


def test_worker_leases_and_heartbeat():
    lease_mgr = WorkerLeaseManager()
    hb_mgr = WorkerHeartbeatManager(lease_mgr)

    # 1. Issue lease
    lease = lease_mgr.issue_lease("wrk-hb-1", cluster_id="cls-1", ttl_seconds=10)
    assert lease.is_valid is True
    assert lease_mgr.is_lease_valid("wrk-hb-1") is True

    # 2. Process heartbeat
    payload = WorkerHeartbeatPayload(
        worker_id="wrk-hb-1",
        status=WorkerStatus.AVAILABLE,
        cpu_usage_pct=45.0,
        memory_usage_pct=50.0,
    )
    assert hb_mgr.process_heartbeat(payload) is True

    # 3. Simulate expired lease
    expired_lease = WorkerLease(
        worker_id="wrk-hb-1",
        cluster_id="cls-1",
        ttl_seconds=5,
        last_renewed=datetime.now(timezone.utc) - timedelta(seconds=15),
    )
    lease_mgr._leases["wrk-hb-1"] = expired_lease
    assert lease_mgr.is_lease_valid("wrk-hb-1") is False
    assert "wrk-hb-1" in lease_mgr.find_expired_leases()


def test_worker_drain_manager():
    drain_mgr = WorkerDrainManager()
    worker = Worker(
        worker_id="wrk-drain-1",
        status=WorkerStatus.AVAILABLE,
        active_assignments=["asg-1"],
    )

    drain_mgr.start_drain(worker, reason="Node upgrade")
    assert worker.status == WorkerStatus.DRAINING
    assert drain_mgr.is_draining("wrk-drain-1") is True
    assert drain_mgr.check_drain_complete(worker) is False

    # Complete in-flight work
    worker.active_assignments.clear()
    assert drain_mgr.check_drain_complete(worker) is True
    drain_mgr.complete_drain(worker)
    assert worker.status == WorkerStatus.UNAVAILABLE


def test_worker_registry_and_persistence():
    with tempfile.TemporaryDirectory() as tmpdir:
        persistence_path = f"{tmpdir}/workers.json"
        registry = WorkerRegistry(persistence_path=persistence_path)

        w1 = Worker(
            worker_id="wrk-reg-1",
            region_id="us-east-1",
            cluster_id="cls-1",
            worker_type=WorkerType.OCR,
            capabilities={"document.ocr"},
            resource_capacity=ResourceCapacity(cpu_cores=8.0, memory_gb=32.0),
        )
        registry.register_worker(w1)

        # Worker should advance to AVAILABLE on registration
        saved_w1 = registry.get_worker("wrk-reg-1")
        assert saved_w1 is not None
        assert saved_w1.status == WorkerStatus.AVAILABLE
        assert saved_w1.active_lease is not None

        # Filter eligible workers
        eligible = registry.find_eligible_workers(
            region_id="us-east-1",
            mandatory_capabilities={"document.ocr"},
            min_cpu=4.0,
        )
        assert len(eligible) == 1
        assert eligible[0].worker_id == "wrk-reg-1"

        # Persistence reload
        reloaded = WorkerRegistry(persistence_path=persistence_path)
        assert reloaded.get_worker("wrk-reg-1") is not None
