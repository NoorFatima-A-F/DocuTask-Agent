"""Tests for Global & Regional Schedulers and Placement Engine."""

from app.infrastructure.clusters.models import Cluster, ClusterStatus
from app.infrastructure.clusters.registry import ClusterRegistry
from app.infrastructure.regions.models import Geography, Region, RegionStatus
from app.infrastructure.regions.registry import RegionRegistry
from app.infrastructure.workers.models import (
    ResourceCapacity,
    Worker,
    WorkerStatus,
    WorkerType,
)
from app.infrastructure.workers.registry import WorkerRegistry
from app.infrastructure.executions.workload import (
    ResourceRequirements,
    WorkloadPriority,
    WorkloadRequest,
    WorkloadState,
    WorkloadType,
)
from app.infrastructure.executions.assignment import AssignmentManager
from app.infrastructure.executions.leases import ExecutionLeaseManager
from app.infrastructure.scheduling.concurrency import ConcurrencyController
from app.infrastructure.scheduling.reservations import ResourceReservationManager
from app.infrastructure.scheduling.diagnostics import SchedulerDiagnosticsService
from app.infrastructure.scheduling.placement import PlacementEngine


def test_global_and_regional_placement_pipeline():
    reg_reg = RegionRegistry()
    cls_reg = ClusterRegistry()
    wrk_reg = WorkerRegistry()

    # 1. Setup Regions (US and EU)
    r_us = Region(
        region_id="us-east-1",
        name="us-east-1",
        display_name="US East",
        data_residency_jurisdiction="US",
        is_primary=True,
    )
    r_eu = Region(
        region_id="eu-west-1",
        name="eu-west-1",
        display_name="EU West",
        data_residency_jurisdiction="EU",
        geography=Geography(jurisdiction="EU"),
    )
    reg_reg.register_region(r_us)
    reg_reg.register_region(r_eu)

    # 2. Setup Clusters
    c_us = Cluster(
        cluster_id="cls-us-1",
        name="US Cluster",
        region_id="us-east-1",
        status=ClusterStatus.ACTIVE,
    )
    c_eu = Cluster(
        cluster_id="cls-eu-1",
        name="EU Cluster",
        region_id="eu-west-1",
        status=ClusterStatus.ACTIVE,
    )
    cls_reg.register_cluster(c_us)
    cls_reg.register_cluster(c_eu)

    # 3. Setup Workers
    w_us = Worker(
        worker_id="wrk-us-ocr",
        region_id="us-east-1",
        cluster_id="cls-us-1",
        capabilities={"document.ocr", "gpu.cuda"},
        resource_capacity=ResourceCapacity(cpu_cores=16.0, memory_gb=64.0, gpu_count=1),
    )
    w_eu = Worker(
        worker_id="wrk-eu-ocr",
        region_id="eu-west-1",
        cluster_id="cls-eu-1",
        capabilities={"document.ocr", "gpu.cuda"},
        resource_capacity=ResourceCapacity(cpu_cores=8.0, memory_gb=32.0, gpu_count=1),
    )
    wrk_reg.register_worker(w_us)
    wrk_reg.register_worker(w_eu)

    # 4. Initialize PlacementEngine
    lease_mgr = ExecutionLeaseManager()
    asg_mgr = AssignmentManager(wrk_reg)
    res_mgr = ResourceReservationManager(wrk_reg)
    conc_ctrl = ConcurrencyController()
    diag_svc = SchedulerDiagnosticsService()

    engine = PlacementEngine(
        region_registry=reg_reg,
        cluster_registry=cls_reg,
        worker_registry=wrk_reg,
        assignment_manager=asg_mgr,
        lease_manager=lease_mgr,
        reservation_manager=res_mgr,
        concurrency_controller=conc_ctrl,
        diagnostics_service=diag_svc,
    )

    # 5. Place EU Workload
    req_eu = WorkloadRequest(
        workload_id="wkl-eu-1",
        workload_type=WorkloadType.OCR_JOB,
        tenant_id="tenant-eu-bank",
        required_jurisdiction="EU",
        required_capabilities={"document.ocr"},
    )
    success_eu, asg_eu, dec_eu = engine.place_workload(req_eu)

    assert success_eu is True
    assert asg_eu is not None
    assert dec_eu.selected_region == "eu-west-1"
    assert dec_eu.selected_worker == "wrk-eu-ocr"
    assert dec_eu.is_scheduled is True

    # 6. Place US Workload
    req_us = WorkloadRequest(
        workload_id="wkl-us-1",
        workload_type=WorkloadType.OCR_JOB,
        tenant_id="tenant-us-firm",
        required_jurisdiction="US",
        required_capabilities={"document.ocr"},
    )
    success_us, asg_us, dec_us = engine.place_workload(req_us)

    assert success_us is True
    assert asg_us is not None
    assert dec_us.selected_region == "us-east-1"
    assert dec_us.selected_worker == "wrk-us-ocr"
