"""FastAPI Routes for Worker Registration, Heartbeat, and Draining."""

from typing import Any, Dict, List, Optional, Set
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.infrastructure.workers.models import (
    ResourceCapacity,
    WorkerStatus,
    WorkerType,
)
from app.infrastructure.workers.heartbeat import WorkerHeartbeatPayload
from app.infrastructure.sdk.scheduling import WorkerSDK

router = APIRouter(prefix="/api/v1/infrastructure/workers", tags=["Worker Orchestration"])

worker_sdk = WorkerSDK()


class RegisterWorkerRequest(BaseModel):
    worker_id: str
    region_id: str
    cluster_id: str
    worker_type: WorkerType = WorkerType.CUSTOM
    service_name: str = "docutask-worker"
    version: str = "3.1.0"
    capabilities: Set[str] = Field(default_factory=set)
    labels: Dict[str, str] = Field(default_factory=dict)
    resource_capacity: Optional[ResourceCapacity] = None
    concurrency_limit: int = 10
    supported_workloads: List[str] = Field(default_factory=lambda: ["workflow", "agent", "ocr"])


class DrainWorkerRequest(BaseModel):
    reason: str = "Administrative drain"


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def register_worker(req: RegisterWorkerRequest) -> Dict[str, Any]:
    try:
        worker = worker_sdk.register_worker(
            worker_id=req.worker_id,
            region_id=req.region_id,
            cluster_id=req.cluster_id,
            worker_type=req.worker_type,
            service_name=req.service_name,
            version=req.version,
            capabilities=req.capabilities,
            labels=req.labels,
            resource_capacity=req.resource_capacity,
            concurrency_limit=req.concurrency_limit,
            supported_workloads=req.supported_workloads,
        )
        return worker.model_dump(mode="json")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.get("/{worker_id}", response_model=Dict[str, Any])
def get_worker(worker_id: str) -> Dict[str, Any]:
    worker = worker_sdk.get_worker(worker_id)
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Worker '{worker_id}' not found.",
        )
    return worker.model_dump(mode="json")


@router.get("", response_model=List[Dict[str, Any]])
def list_workers(
    region_id: Optional[str] = None,
    cluster_id: Optional[str] = None,
    status: Optional[WorkerStatus] = None,
) -> List[Dict[str, Any]]:
    workers = worker_sdk.list_workers(region_id=region_id, cluster_id=cluster_id, status=status)
    return [w.model_dump(mode="json") for w in workers]


@router.post("/{worker_id}/heartbeat", response_model=Dict[str, Any])
def worker_heartbeat(worker_id: str, payload: WorkerHeartbeatPayload) -> Dict[str, Any]:
    payload.worker_id = worker_id
    lease = worker_sdk.heartbeat(payload)
    if not lease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Worker '{worker_id}' not found.",
        )
    return lease.model_dump(mode="json")


@router.post("/{worker_id}/drain", response_model=Dict[str, Any])
def drain_worker(worker_id: str, req: DrainWorkerRequest) -> Dict[str, Any]:
    worker = worker_sdk.drain(worker_id, reason=req.reason)
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Worker '{worker_id}' not found.",
        )
    return worker.model_dump(mode="json")
