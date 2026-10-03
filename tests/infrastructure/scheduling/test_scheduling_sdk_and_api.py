"""Tests for WorkerSDK, SchedulingSDK, and REST API Endpoints."""

from app.infrastructure.workers.models import (
    ResourceCapacity,
    WorkerStatus,
    WorkerType,
)
from app.infrastructure.workers.heartbeat import WorkerHeartbeatPayload
from app.infrastructure.executions.workload import (
    WorkloadRequest,
    WorkloadState,
    WorkloadType,
)
from app.infrastructure.regions.models import Region, RegionStatus
from app.infrastructure.clusters.models import Cluster, ClusterStatus
from app.infrastructure.sdk.scheduling import SchedulingSDK, WorkerSDK
from app.infrastructure.api.worker_routes import (
    register_worker,
    get_worker,
    worker_heartbeat,
    drain_worker,
    RegisterWorkerRequest,
    DrainWorkerRequest,
)
from app.infrastructure.api.scheduler_routes import (
    submit_workload,
    get_workload_status,
    cancel_workload,
    get_workload_diagnostics,
)


def test_worker_and_scheduling_sdk():
    scheduling_sdk = SchedulingSDK()
    worker_sdk = WorkerSDK(scheduling_sdk.worker_registry)

    # 1. Setup Region and Cluster
    scheduling_sdk.region_registry.register_region(
        Region(
            region_id="us-east-1",
            name="us-east-1",
            display_name="US East",
            data_residency_jurisdiction="US",
            status=RegionStatus.ACTIVE,
        )
    )
    scheduling_sdk.cluster_registry.register_cluster(
        Cluster(
            cluster_id="cls-us-1",
            name="US Main",
            region_id="us-east-1",
            status=ClusterStatus.ACTIVE,
        )
    )

    # 2. Register Worker
    worker = worker_sdk.register_worker(
        worker_id="wrk-sdk-1",
        region_id="us-east-1",
        cluster_id="cls-us-1",
        worker_type=WorkerType.WORKFLOW,
        capabilities={"workflow.execute"},
        resource_capacity=ResourceCapacity(cpu_cores=16.0, memory_gb=64.0),
    )
    assert worker.worker_id == "wrk-sdk-1"
    assert worker.status == WorkerStatus.AVAILABLE

    # 3. Submit Workload
    req = WorkloadRequest(
        workload_id="wkl-sdk-1",
        workload_type=WorkloadType.WORKFLOW_TASK,
        tenant_id="tenant-acme",
        required_jurisdiction="US",
        required_capabilities={"workflow.execute"},
    )
    success, asg, decision = scheduling_sdk.submit(req)
    assert success is True
    assert asg is not None
    assert decision.selected_worker == "wrk-sdk-1"
    assert scheduling_sdk.status("wkl-sdk-1") == WorkloadState.ASSIGNED

    # 4. Diagnostics
    diag = scheduling_sdk.diagnostics("wkl-sdk-1")
    assert diag is not None
    assert diag.is_scheduled is True
    assert diag.selected_placement["worker"] == "wrk-sdk-1"

    # 5. Cancel Workload
    assert scheduling_sdk.cancel("wkl-sdk-1") is True
    assert scheduling_sdk.status("wkl-sdk-1") == WorkloadState.CANCELLED


def test_api_endpoints_direct():
    # 1. Register Worker via API
    reg_res = register_worker(
        RegisterWorkerRequest(
            worker_id="wrk-api-1",
            region_id="us-east-1",
            cluster_id="cls-us-1",
            worker_type=WorkerType.OCR,
            capabilities={"document.ocr"},
        )
    )
    assert reg_res["worker_id"] == "wrk-api-1"
    assert reg_res["status"] == WorkerStatus.AVAILABLE.value

    # 2. Get Worker via API
    get_res = get_worker("wrk-api-1")
    assert get_res["worker_id"] == "wrk-api-1"

    # 3. Heartbeat via API
    hb_res = worker_heartbeat(
        "wrk-api-1",
        WorkerHeartbeatPayload(worker_id="wrk-api-1", cpu_usage_pct=25.0),
    )
    assert hb_res["is_valid"] is True

    # 4. Drain Worker via API
    drain_res = drain_worker(
        "wrk-api-1", DrainWorkerRequest(reason="Maintenance")
    )
    assert drain_res["status"] == WorkerStatus.DRAINING.value

    # 5. Submit Workload via API
    req = WorkloadRequest(
        workload_id="wkl-api-1",
        tenant_id="tenant-api",
        workload_type=WorkloadType.CUSTOM,
    )
    submit_res = submit_workload(req)
    assert "decision" in submit_res
    assert submit_res["workload_id"] == "wkl-api-1"

    # 6. Status and Diagnostics via API
    status_res = get_workload_status("wkl-api-1")
    assert "state" in status_res

    diag_res = get_workload_diagnostics("wkl-api-1")
    assert diag_res["workload_id"] == "wkl-api-1"

    # 7. Cancel Workload via API
    cancel_res = cancel_workload("wkl-api-1")
    assert cancel_res["status"] == "CANCELLED"
