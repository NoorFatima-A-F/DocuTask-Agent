"""Infrastructure API package exports."""

from .routes import infrastructure_sdk, router
from .cluster_routes import router as cluster_router
from .region_routes import router as region_router
from .worker_routes import router as worker_router
from .scheduler_routes import router as scheduler_router
from .reliability_routes import reliability_sdk, router as reliability_router
from app.infrastructure.observability.api.observability_routes import observability_sdk, router as observability_router
from app.infrastructure.networking.api.network_routes import get_network_sdk, router as network_router
network_sdk = get_network_sdk()
from app.infrastructure.deployment.api.deployment_routes import get_deployment_sdk, router as deployment_router
deployment_sdk = get_deployment_sdk()
from .schemas import (
    ResourceProvisionRequest,
    ResourceResponse,
    RuntimeActionRequest,
    RuntimeDeployRequest,
    ServiceHealthResponse,
    ServiceInstanceResponse,
)

__all__ = [
    "ResourceProvisionRequest",
    "ResourceResponse",
    "RuntimeActionRequest",
    "RuntimeDeployRequest",
    "ServiceHealthResponse",
    "ServiceInstanceResponse",
    "cluster_router",
    "deployment_router",
    "deployment_sdk",
    "infrastructure_sdk",
    "network_router",
    "network_sdk",
    "observability_router",
    "observability_sdk",
    "region_router",
    "reliability_router",
    "reliability_sdk",
    "router",
    "scheduler_router",
    "worker_router",
]


