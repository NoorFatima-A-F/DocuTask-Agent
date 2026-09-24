"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Connector SDK Base.
Defines the canonical base class and lifecycle contracts that every connector plugin must implement.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional

from app.connectors.core.models import (
    ActionDescriptor,
    CapabilityDescriptor,
    Connector,
    ConnectorCategory,
    ConnectorHealth,
    TriggerDescriptor,
)


class BaseConnector(ABC):
    """
    Abstract Base Class for all first-party and third-party connector plugins.
    Enforces contract uniformity across metadata, authentication, capabilities,
    actions, triggers, and execution.
    """

    def __init__(self, connector_model: Optional[Connector] = None):
        self._connector = connector_model or self._default_model()
        self._authenticated = False
        self._action_handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}
        self._trigger_handlers: Dict[str, Callable[..., Any]] = {}

    def _default_model(self) -> Connector:
        return Connector(
            id=self.__class__.__name__.lower(),
            name=self.__class__.__name__,
            vendor="Custom",
            category=ConnectorCategory.CUSTOM,
        )

    def metadata(self) -> Connector:
        """Returns the connector's descriptor model and configuration schema."""
        return self._connector

    @abstractmethod
    def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """
        Validates and configures runtime authentication using isolated tenant credentials.
        """
        pass

    @abstractmethod
    def validate_connection(self) -> bool:
        """Tests live connectivity with the external upstream service."""
        pass

    @abstractmethod
    def capabilities(self) -> List[CapabilityDescriptor]:
        """Lists technology-independent capabilities provided by this connector."""
        pass

    @abstractmethod
    def actions(self) -> List[ActionDescriptor]:
        """Lists all executable action contracts."""
        pass

    def triggers(self) -> List[TriggerDescriptor]:
        """Lists all supported triggers and webhooks."""
        return []

    def health_check(self) -> ConnectorHealth:
        """Performs a live diagnostic health check."""
        try:
            if self.validate_connection():
                return ConnectorHealth.HEALTHY
            return ConnectorHealth.DEGRADED
        except Exception:
            return ConnectorHealth.UNHEALTHY

    @abstractmethod
    def execute(
        self,
        action_name: str,
        inputs: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes a named action with input payload and execution context.
        """
        pass

    def shutdown(self) -> None:
        """Cleans up sockets, thread pools, and active sessions on connector removal."""
        self._authenticated = False
