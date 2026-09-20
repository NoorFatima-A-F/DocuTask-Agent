"""
Enterprise Integration Fabric - Registry package.
"""

from app.connectors.registry.capability_registry import CapabilityRegistry
from app.connectors.registry.connector_registry import ConnectorRegistry

__all__ = [
    "ConnectorRegistry",
    "CapabilityRegistry",
]
