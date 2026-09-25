"""FastAPI Routes for Infrastructure Lifecycle, Services, and Resources."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status

from ..core.resources import ResourceCategory
from ..sdk.client import InfrastructureSDK
from .schemas import (
    ResourceProvisionRequest,
    ResourceResponse,
    RuntimeActionRequest,
    RuntimeDeployRequest,
    ServiceHealthResponse,
    ServiceInstanceResponse,
)

router = APIRouter(prefix="/api/v1/infrastructure", tags=["Infrastructure Platform"])

# Shared singleton SDK instance for routes
infrastructure_sdk = InfrastructureSDK()


# -----------------------------------------------------------------------------
# Runtime Routes
# -----------------------------------------------------------------------------

@router.post("/runtime/deploy", response_model=ServiceInstanceResponse)
def deploy_service(req: RuntimeDeployRequest) -> ServiceInstanceResponse:
    try:
        inst = infrastructure_sdk.deploy_service(
            name=req.service,
            environment=req.environment,
            replicas=req.replicas,
            version=req.version,
            config=req.config,
        )
        return ServiceInstanceResponse(
            instance_id=inst.instance_id,
            service_name=inst.service_name,
            environment=inst.environment,
            replicas=inst.replicas,
            state=inst.state.value,
            version=inst.version,
            created_at=inst.created_at,
            error_message=inst.error_message,
        )
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.post("/runtime/start", response_model=ServiceInstanceResponse)
def start_runtime(req: RuntimeActionRequest) -> ServiceInstanceResponse:
    try:
        inst = infrastructure_sdk.runtime.start_service(req.instance_id)
        return ServiceInstanceResponse(
            instance_id=inst.instance_id,
            service_name=inst.service_name,
            environment=inst.environment,
            replicas=inst.replicas,
            state=inst.state.value,
            version=inst.version,
            created_at=inst.created_at,
        )
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.post("/runtime/stop", response_model=ServiceInstanceResponse)
def stop_runtime(req: RuntimeActionRequest) -> ServiceInstanceResponse:
    try:
        inst = infrastructure_sdk.runtime.stop_service(req.instance_id)
        return ServiceInstanceResponse(
            instance_id=inst.instance_id,
            service_name=inst.service_name,
            environment=inst.environment,
            replicas=inst.replicas,
            state=inst.state.value,
            version=inst.version,
            created_at=inst.created_at,
        )
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.post("/runtime/restart", response_model=ServiceInstanceResponse)
def restart_runtime(req: RuntimeActionRequest) -> ServiceInstanceResponse:
    try:
        inst = infrastructure_sdk.restart_service(req.instance_id)
        return ServiceInstanceResponse(
            instance_id=inst.instance_id,
            service_name=inst.service_name,
            environment=inst.environment,
            replicas=inst.replicas,
            state=inst.state.value,
            version=inst.version,
            created_at=inst.created_at,
        )
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.get("/runtime/status", response_model=List[ServiceInstanceResponse])
def get_runtime_status(environment: Optional[str] = None) -> List[ServiceInstanceResponse]:
    instances = infrastructure_sdk.runtime.list_instances(environment=environment)
    return [
        ServiceInstanceResponse(
            instance_id=i.instance_id,
            service_name=i.service_name,
            environment=i.environment,
            replicas=i.replicas,
            state=i.state.value,
            version=i.version,
            created_at=i.created_at,
            error_message=i.error_message,
        )
        for i in instances
    ]


# -----------------------------------------------------------------------------
# Services & Health Routes
# -----------------------------------------------------------------------------

@router.get("/services")
def list_services(environment: Optional[str] = None) -> List[Dict[str, Any]]:
    services = infrastructure_sdk.service_registry.list_services(environment=environment)
    return [s.model_dump() for s in services]


@router.get("/services/{id}")
def get_service(id: str) -> Dict[str, Any]:
    svc = infrastructure_sdk.service_registry.get_service(id)
    if not svc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Service {id} not found")
    return svc.model_dump()


@router.get("/services/{id}/health", response_model=ServiceHealthResponse)
def get_service_health(id: str) -> ServiceHealthResponse:
    health = infrastructure_sdk.check_health(id)
    return ServiceHealthResponse(
        service_id=health.service_id,
        status=health.status.value,
        version=health.version,
        cpu_percent=health.cpu_percent,
        memory_mb=health.memory_mb,
        latency_p95_ms=health.latency_p95_ms,
        errors_per_minute=health.errors_per_minute,
        region=health.region,
        cluster=health.cluster,
        last_check=health.last_check,
    )


# -----------------------------------------------------------------------------
# Resources Routes
# -----------------------------------------------------------------------------

@router.get("/resources", response_model=List[ResourceResponse])
def list_resources(environment: Optional[str] = None) -> List[ResourceResponse]:
    resources = infrastructure_sdk.resource_mgr.list_resources(environment=environment)
    return [
        ResourceResponse(
            resource_id=r.resource_id,
            name=r.name,
            category=r.category.value,
            resource_type=r.resource_type,
            state=r.state.value,
            endpoint_url=r.endpoint_url,
            allocated_at=r.allocated_at,
        )
        for r in resources
    ]


@router.post("/resources/provision", response_model=ResourceResponse)
def provision_resource(req: ResourceProvisionRequest) -> ResourceResponse:
    try:
        category_enum = ResourceCategory(req.category.upper())
        res = infrastructure_sdk.provision_resource(
            name=req.name,
            category=category_enum,
            resource_type=req.resource_type,
            cpu_cores=req.cpu_cores,
            memory_mb=req.memory_mb,
            storage_gb=req.storage_gb,
            environment=req.environment,
        )
        return ResourceResponse(
            resource_id=res.resource_id,
            name=res.name,
            category=res.category.value,
            resource_type=res.resource_type,
            state=res.state.value,
            endpoint_url=res.endpoint_url,
            allocated_at=res.allocated_at,
        )
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.delete("/resources/{id}", response_model=ResourceResponse)
def delete_resource(id: str) -> ResourceResponse:
    try:
        res = infrastructure_sdk.resource_mgr.release_resource(id)
        return ResourceResponse(
            resource_id=res.resource_id,
            name=res.name,
            category=res.category.value,
            resource_type=res.resource_type,
            state=res.state.value,
            endpoint_url=res.endpoint_url,
            allocated_at=res.allocated_at,
        )
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))
