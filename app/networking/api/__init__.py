"""Service Mesh API Package."""

from .schemas import (
    ServiceRegistrationRequest,
    ServiceResponseSchema,
    EndpointRegistrationRequest,
    EndpointResponseSchema,
    PolicyCreateRequest,
    RouteRuleCreateRequest,
    TrafficSplitRequest,
    CertificateIssueRequest,
    MeshCallRequest,
    MeshCallResponse,
)
from .routes import (
    router as network_mesh_router,
    get_mesh_client,
)

__all__ = [
    "ServiceRegistrationRequest",
    "ServiceResponseSchema",
    "EndpointRegistrationRequest",
    "EndpointResponseSchema",
    "PolicyCreateRequest",
    "RouteRuleCreateRequest",
    "TrafficSplitRequest",
    "CertificateIssueRequest",
    "MeshCallRequest",
    "MeshCallResponse",
    "network_mesh_router",
    "get_mesh_client",
]
