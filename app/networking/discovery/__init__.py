"""Service Discovery & Target Resolution Package."""

from .registry import (
    EndpointHealth,
    ServiceEndpoint,
    ServiceRegistry,
)
from .resolver import (
    ResolvedTarget,
    ServiceResolver,
)

__all__ = [
    "EndpointHealth",
    "ServiceEndpoint",
    "ServiceRegistry",
    "ResolvedTarget",
    "ServiceResolver",
]
