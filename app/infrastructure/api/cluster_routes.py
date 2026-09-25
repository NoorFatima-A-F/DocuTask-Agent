"""FastAPI Routes for Cluster Lifecycle, Health, and Operations."""

from typing import Any, Dict, List, Optional, Set
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.infrastructure.clusters.models import (
    CapacityModel,
    ClusterStatus,
    ClusterType,
)
from app.infrastructure.clusters.health import SubComponentHealth
from app.infrastructure.sdk.clusters import ClusterSDK

router = APIRouter(prefix="/api/v1/infrastructure/clusters", tags=["Cluster Management"])

cluster_sdk = ClusterSDK()


class RegisterClusterRequest(BaseModel):
    cluster_id: str
    name: str
    region_id: str
    provider: str = "kubernetes"
    cluster_type: ClusterType = ClusterType.PRODUCTION
    labels: Dict[str, str] = Field(default_factory=dict)
    capabilities: Set[str] = Field(default_factory=set)
    capacity: Optional[CapacityModel] = None


class StateTransitionRequest(BaseModel):
    target_state: ClusterStatus
    reason: Optional[str] = None


class HeartbeatRequest(BaseModel):
    sub_components: List[SubComponentHealth] = Field(default_factory=list)
    ttl_seconds: int = 60


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def register_cluster(req: RegisterClusterRequest) -> Dict[str, Any]:
    try:
        cluster = cluster_sdk.register_cluster(
            cluster_id=req.cluster_id,
            name=req.name,
            region_id=req.region_id,
            provider=req.provider,
            cluster_type=req.cluster_type,
            labels=req.labels,
            capabilities=req.capabilities,
            capacity=req.capacity,
        )
        return cluster.model_dump(mode="json")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.get("/{cluster_id}", response_model=Dict[str, Any])
def get_cluster(cluster_id: str) -> Dict[str, Any]:
    cluster = cluster_sdk.get_cluster(cluster_id)
    if not cluster:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cluster '{cluster_id}' not found.",
        )
    return cluster.model_dump(mode="json")


@router.get("", response_model=List[Dict[str, Any]])
def list_clusters(
    region_id: Optional[str] = None,
    status: Optional[ClusterStatus] = None,
    environment: Optional[str] = None,
) -> List[Dict[str, Any]]:
    clusters = cluster_sdk.list_clusters(
        region_id=region_id, status=status, environment=environment
    )
    return [c.model_dump(mode="json") for c in clusters]


@router.post("/{cluster_id}/state", response_model=Dict[str, Any])
def transition_cluster_state(cluster_id: str, req: StateTransitionRequest) -> Dict[str, Any]:
    try:
        cluster = cluster_sdk.transition_cluster_state(
            cluster_id, req.target_state, reason=req.reason
        )
        if not cluster:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cluster '{cluster_id}' not found.",
            )
        return cluster.model_dump(mode="json")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.post("/{cluster_id}/heartbeat", response_model=Dict[str, Any])
def cluster_heartbeat(cluster_id: str, req: HeartbeatRequest) -> Dict[str, Any]:
    lease = cluster_sdk.heartbeat(
        cluster_id=cluster_id,
        sub_components=req.sub_components,
        ttl_seconds=req.ttl_seconds,
    )
    if not lease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cluster '{cluster_id}' not found.",
        )
    return lease.model_dump(mode="json")


@router.get("/{cluster_id}/diagnostics", response_model=Dict[str, Any])
def get_cluster_diagnostics(cluster_id: str) -> Dict[str, Any]:
    try:
        return cluster_sdk.get_cluster_diagnostics(cluster_id)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))


@router.delete("/{cluster_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cluster(cluster_id: str) -> None:
    deleted = cluster_sdk.global_control_plane.deregister_cluster_globally(cluster_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cluster '{cluster_id}' not found.",
        )
