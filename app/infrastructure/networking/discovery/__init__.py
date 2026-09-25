"""Service Discovery Platform package."""

from .registry import (
    ServiceHealthState,
    ServiceEndpoint,
    ServiceInstance,
    ServiceRegistration,
    ServiceDiscoveryRegistry,
)
from .resolver import ResolvedServiceTarget, ServiceResolver
from .heartbeat import ServiceHeartbeatManager

__all__ = [
    "ServiceHealthState",
    "ServiceEndpoint",
    "ServiceInstance",
    "ServiceRegistration",
    "ServiceDiscoveryRegistry",
    "ResolvedServiceTarget",
    "ServiceResolver",
    "ServiceHeartbeatManager",
]
