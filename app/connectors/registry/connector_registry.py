"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Connector Registry.
Provides discovery, version resolution, health tracking, and catalog management for all connectors.
"""

from __future__ import annotations

from datetime import datetime, timezone
import logging
from typing import Dict, List, Optional
from app.connectors.core.exceptions import ConnectorNotFoundError
from app.connectors.core.models import (
    Connector,
    ConnectorCategory,
    ConnectorHealth,
    ConnectorStatus,
)
from app.connectors.sdk.base import BaseConnector

logger = logging.getLogger(__name__)


class ConnectorRegistry:
    """
    Central catalog storing connector manifests, active plugin instances,
    version metadata, permissions, and operational health.
    """

    def __init__(self):
        self._connectors: Dict[str, Connector] = {}
        self._instances: Dict[str, BaseConnector] = {}
        self._version_history: Dict[str, Dict[str, Connector]] = {}  # id -> {version -> Connector}

    def register(self, connector: Connector | BaseConnector) -> Connector:
        """
        Registers a connector model or active BaseConnector instance into the catalog.
        """
        if isinstance(connector, BaseConnector):
            instance = connector
            model = instance.metadata()
            self._instances[model.id] = instance
        else:
            model = connector
            instance = None

        self._connectors[model.id] = model

        # Version history
        if model.id not in self._version_history:
            self._version_history[model.id] = {}
        self._version_history[model.id][model.version] = model

        logger.info(f"Registered connector '{model.id}' v{model.version} ({model.name})")
        return model

    def register_instance(self, connector_id: str, instance: BaseConnector) -> None:
        """Associates a live BaseConnector execution instance with a connector ID."""
        self._instances[connector_id] = instance
        self._connectors[connector_id] = instance.metadata()

    def get(self, connector_id: str, version: Optional[str] = None) -> Connector:
        """Retrieves connector metadata by ID, optionally pinning a specific version."""
        if connector_id not in self._connectors:
            raise ConnectorNotFoundError(f"Connector '{connector_id}' not found in registry", connector_id=connector_id)

        if version and connector_id in self._version_history:
            if version in self._version_history[connector_id]:
                return self._version_history[connector_id][version]

        return self._connectors[connector_id]

    def get_instance(self, connector_id: str) -> Optional[BaseConnector]:
        """Retrieves the live runnable BaseConnector plugin instance if loaded."""
        return self._instances.get(connector_id)

    def list_all(
        self,
        category: Optional[ConnectorCategory | str] = None,
        status: Optional[ConnectorStatus | str] = None,
        healthy_only: bool = False,
    ) -> List[Connector]:
        """Lists connectors with optional filtering by category, status, and health."""
        results = list(self._connectors.values())

        if category:
            cat_val = category.value if isinstance(category, ConnectorCategory) else str(category)
            results = [c for c in results if (c.category.value if isinstance(c.category, ConnectorCategory) else str(c.category)) == cat_val]

        if status:
            stat_val = status.value if isinstance(status, ConnectorStatus) else str(status)
            results = [c for c in results if (c.status.value if isinstance(c.status, ConnectorStatus) else str(c.status)) == stat_val]

        if healthy_only:
            results = [c for c in results if c.health == ConnectorHealth.HEALTHY]

        return results

    def search(self, query: str) -> List[Connector]:
        """Performs a fuzzy search across connector ID, name, vendor, and capabilities."""
        q = query.lower()
        matches = []
        for c in self._connectors.values():
            if (
                q in c.id.lower()
                or q in c.name.lower()
                or q in c.vendor.lower()
                or any(q in cap.lower() for cap in c.capabilities)
            ):
                matches.append(c)
        return matches

    def update_health(self, connector_id: str, health: ConnectorHealth) -> None:
        """Updates the live health status of a registered connector."""
        connector = self.get(connector_id)
        connector.health = health
        connector.updated_at = datetime.now(timezone.utc)

    def unregister(self, connector_id: str) -> bool:
        """Removes a connector from the registry."""
        if connector_id in self._connectors:
            del self._connectors[connector_id]
            self._instances.pop(connector_id, None)
            return True
        return False
