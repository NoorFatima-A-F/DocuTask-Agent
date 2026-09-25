"""FastAPI Routes for Regional Topology, Tenant Affinity, and Multi-Region Routing."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.infrastructure.regions.models import Geography, RegionStatus
from app.infrastructure.regions.affinity import TenantAffinityRule
from app.infrastructure.routing.metadata import WorkloadRoutingRequest
from app.infrastructure.sdk.clusters import ClusterSDK

router = APIRouter(prefix="/api/v1/infrastructure", tags=["Regional Management & Routing"])

cluster_sdk = ClusterSDK()


class RegisterRegionRequest(BaseModel):
    region_id: str
    name: str
    display_name: str
    provider: str = "aws"
    data_residency_jurisdiction: str = "US"
    is_primary: bool = False
    routing_priority: int = 100
    geography: Optional[Geography] = None
    failover_region_id: Optional[str] = None


class UpdateRegionStatusRequest(BaseModel):
    status: RegionStatus


@router.post("/regions", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def register_region(req: RegisterRegionRequest) -> Dict[str, Any]:
    try:
        region = cluster_sdk.register_region(
            region_id=req.region_id,
            name=req.name,
            display_name=req.display_name,
            provider=req.provider,
            data_residency_jurisdiction=req.data_residency_jurisdiction,
            is_primary=req.is_primary,
            routing_priority=req.routing_priority,
            geography=req.geography,
            failover_region_id=req.failover_region_id,
        )
        return region.model_dump(mode="json")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.get("/regions/{region_id}", response_model=Dict[str, Any])
def get_region(region_id: str) -> Dict[str, Any]:
    region = cluster_sdk.get_region(region_id)
    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Region '{region_id}' not found.",
        )
    return region.model_dump(mode="json")


@router.get("/regions", response_model=List[Dict[str, Any]])
def list_regions(
    status: Optional[RegionStatus] = None,
    jurisdiction: Optional[str] = None,
    provider: Optional[str] = None,
) -> List[Dict[str, Any]]:
    regions = cluster_sdk.list_regions(status=status, jurisdiction=jurisdiction, provider=provider)
    return [r.model_dump(mode="json") for r in regions]


@router.post("/regions/{region_id}/status", response_model=Dict[str, Any])
def update_region_status(region_id: str, req: UpdateRegionStatusRequest) -> Dict[str, Any]:
    region = cluster_sdk.region_registry.update_region_status(region_id, req.status)
    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Region '{region_id}' not found.",
        )
    return region.model_dump(mode="json")


@router.post("/affinity", response_model=Dict[str, Any])
def set_tenant_affinity(rule: TenantAffinityRule) -> Dict[str, Any]:
    saved = cluster_sdk.set_tenant_affinity(rule)
    return saved.model_dump(mode="json")


@router.post("/routing/evaluate", response_model=Dict[str, Any])
def evaluate_routing(req: WorkloadRoutingRequest) -> Dict[str, Any]:
    decision = cluster_sdk.evaluate_routing(req)
    return decision.model_dump(mode="json")


@router.get("/topology", response_model=Dict[str, Any])
def get_topology() -> Dict[str, Any]:
    return cluster_sdk.get_global_topology()
