"""
Phase 13.18: Distributed Runtime REST API Endpoints
Autonomous Cloud Runtime & Distributed Agent Fabric (ACR-DAF).
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.runtime.distributed.runtime.distributed_runtime import distributed_runtime
from app.runtime.distributed.models.schemas import (
    WorkerNode,
    WorkerStatus,
    ScheduledJob,
    JobPriority,
    JobState,
    RegionName,
    DurableWorkflow,
    WorkflowCheckpoint,
    ClusterOverview,
    DisasterRecoverySnapshot,
)

router = APIRouter()


class RegisterWorkerRequest(BaseModel):
    hostname: str
    region: RegionName = RegionName.US_EAST
    capabilities: List[str] = Field(default_factory=lambda: ["reasoning", "ocr", "planning"])
    cpu_cores: int = 4
    memory_mb: int = 8192


class HeartbeatRequest(BaseModel):
    cpu_pct: Optional[float] = None
    memory_pct: Optional[float] = None


class EnqueueJobRequest(BaseModel):
    workflow_id: str = "wf_custom_01"
    agent_id: str = "agent_chief_architect"
    task_name: str = "Distributed System Execution"
    priority: JobPriority = JobPriority.NORMAL
    sla_deadline_ms: float = 5000.0
    payload: Dict[str, Any] = Field(default_factory=dict)


class ChaosFailureRequest(BaseModel):
    worker_id: str
    target_failover_worker_id: Optional[str] = None


class DrillRequest(BaseModel):
    failed_region: RegionName = RegionName.US_EAST
    target_failover_region: RegionName = RegionName.EU_CENTRAL


@router.get("/cluster/overview", summary="High-level cluster overview and node metrics", response_model=ClusterOverview)
async def get_cluster_overview() -> ClusterOverview:
    return distributed_runtime.get_cluster_overview()


@router.get("/workers", summary="List cloud worker fleet nodes", response_model=List[WorkerNode])
async def list_workers(
    region: Optional[RegionName] = Query(None),
    active_only: bool = Query(False),
) -> List[WorkerNode]:
    return distributed_runtime.fleet_manager.list_workers(region=region, active_only=active_only)


@router.post("/workers/register", summary="Register worker node to fabric", response_model=WorkerNode)
async def register_worker(request: RegisterWorkerRequest) -> WorkerNode:
    return distributed_runtime.fleet_manager.register_worker(
        hostname=request.hostname,
        region=request.region,
        capabilities=request.capabilities,
        cpu_cores=request.cpu_cores,
        memory_mb=request.memory_mb,
    )


@router.post("/workers/{worker_id}/heartbeat", summary="Record worker heartbeat")
async def record_heartbeat(worker_id: str, request: HeartbeatRequest) -> Dict[str, Any]:
    ok = distributed_runtime.fleet_manager.record_heartbeat(
        worker_id=worker_id,
        cpu_pct=request.cpu_pct,
        memory_pct=request.memory_pct,
    )
    if not ok:
        raise HTTPException(status_code=404, detail=f"Worker {worker_id} not found")
    return {"status": "HEARTBEAT_ACK", "worker_id": worker_id}


@router.post("/workers/{worker_id}/drain", summary="Gracefully drain worker node")
async def drain_worker(worker_id: str) -> Dict[str, Any]:
    ok = distributed_runtime.fleet_manager.drain_worker(worker_id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"Worker {worker_id} not found")
    return {"status": "DRAINING", "worker_id": worker_id}


@router.get("/queues", summary="Get distributed queue metrics and DLQs")
async def get_queue_metrics() -> List[Dict[str, Any]]:
    return distributed_runtime.queue_manager.get_all_metrics()


@router.post("/scheduler/jobs", summary="Enqueue scheduled job", response_model=ScheduledJob)
async def submit_job(request: EnqueueJobRequest) -> ScheduledJob:
    return distributed_runtime.scheduler.submit_job(
        workflow_id=request.workflow_id,
        agent_id=request.agent_id,
        task_name=request.task_name,
        priority=request.priority,
        payload=request.payload,
        sla_deadline_ms=request.sla_deadline_ms,
    )


@router.get("/scheduler/jobs", summary="List scheduled and completed jobs", response_model=List[ScheduledJob])
async def list_jobs(
    limit: int = Query(50, ge=1, le=500),
    state: Optional[JobState] = Query(None),
) -> List[ScheduledJob]:
    return distributed_runtime.scheduler.list_jobs(limit=limit, state=state)


@router.get("/workflows/durable", summary="List durable workflows", response_model=List[DurableWorkflow])
async def list_durable_workflows() -> List[DurableWorkflow]:
    return distributed_runtime.workflow_engine.list_workflows()


@router.post("/workflows/{workflow_id}/pause", summary="Pause durable workflow", response_model=DurableWorkflow)
async def pause_workflow(workflow_id: str) -> DurableWorkflow:
    wf = distributed_runtime.workflow_engine.pause_workflow(workflow_id)
    if not wf:
        raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")
    return wf


@router.post("/workflows/{workflow_id}/resume", summary="Resume durable workflow from checkpoint", response_model=DurableWorkflow)
async def resume_workflow(workflow_id: str) -> DurableWorkflow:
    wf = distributed_runtime.workflow_engine.resume_workflow(workflow_id)
    if not wf:
        raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")
    return wf


@router.get("/checkpoints/{workflow_id}", summary="Get checkpoint snapshots for workflow", response_model=List[WorkflowCheckpoint])
async def get_checkpoints(workflow_id: str) -> List[WorkflowCheckpoint]:
    wf = distributed_runtime.workflow_engine.get_workflow(workflow_id)
    if not wf:
        raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")
    return wf.checkpoints


@router.get("/autoscaling/status", summary="Get autoscaling policy and metrics")
async def get_autoscaling_status() -> Dict[str, Any]:
    return {
        "policy": distributed_runtime.autoscaler.policy.model_dump(),
        "recent_decisions": distributed_runtime.autoscaler.get_history(),
    }


@router.post("/autoscaling/evaluate", summary="Trigger autoscaler evaluation")
async def evaluate_autoscaling() -> Dict[str, Any]:
    return distributed_runtime.autoscaler.evaluate_scaling()


@router.get("/regions", summary="Get multi-region network topology and latency matrix")
async def get_regions() -> List[Dict[str, Any]]:
    return distributed_runtime.region_router.get_region_topology()


@router.post("/chaos/inject-failure", summary="Inject chaos worker crash and trigger failover")
async def inject_chaos_failure(request: ChaosFailureRequest) -> Dict[str, Any]:
    worker = distributed_runtime.fleet_manager.get_worker(request.worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail=f"Worker {request.worker_id} not found")

    worker.status = WorkerStatus.CRASHED
    target_worker = request.target_failover_worker_id
    if not target_worker:
        active = distributed_runtime.fleet_manager.list_workers(active_only=True)
        target_worker = active[0].worker_id if active else "node_failover_spare"

    migrated = distributed_runtime.workflow_engine.migrate_workflow_on_crash(
        crashed_worker_id=request.worker_id,
        target_worker_id=target_worker,
    )
    return {
        "status": "CHAOS_INJECTED",
        "crashed_worker_id": request.worker_id,
        "target_failover_worker_id": target_worker,
        "migrated_workflows": [m.workflow_id for m in migrated],
    }


@router.get("/disaster-recovery/status", summary="Get disaster recovery snapshots", response_model=List[DisasterRecoverySnapshot])
async def get_dr_status() -> List[DisasterRecoverySnapshot]:
    return distributed_runtime.dr_engine.list_snapshots()


@router.post("/disaster-recovery/drill", summary="Execute cross-region DR failover drill")
async def run_dr_drill(request: DrillRequest) -> Dict[str, Any]:
    return distributed_runtime.dr_engine.execute_failover_drill(
        failed_region=request.failed_region,
        target_failover_region=request.target_failover_region,
    )


@router.post("/runtime/cycle", summary="Execute distributed orchestrator cycle")
async def run_distributed_cycle() -> Dict[str, Any]:
    return await distributed_runtime.execute_distributed_cycle()
