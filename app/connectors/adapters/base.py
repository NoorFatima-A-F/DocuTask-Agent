"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Protocol Adapters.
Provides standard adapters for REST, GraphQL, SOAP, gRPC, and File-based external APIs.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import json
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class BaseProtocolAdapter(ABC):
    """Abstract protocol adapter bridging generic connector contracts to low-level wire formats."""

    @abstractmethod
    def call(self, endpoint: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        pass


class RESTAdapter(BaseProtocolAdapter):
    """Standard REST/HTTP adapter with JSON encoding and status code interpretation."""

    def call(
        self,
        endpoint: str,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        method: str = "POST",
    ) -> Dict[str, Any]:
        # Simulated standard REST call
        return {
            "protocol": "REST",
            "method": method,
            "endpoint": endpoint,
            "headers": headers or {},
            "data": payload,
            "status_code": 200,
        }


class GraphQLAdapter(BaseProtocolAdapter):
    """Adapter for executing GraphQL queries and mutations."""

    def call(
        self,
        endpoint: str,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        query = payload.get("query", "")
        variables = payload.get("variables", {})
        return {
            "protocol": "GraphQL",
            "endpoint": endpoint,
            "data": {"query_executed": query, "variables": variables},
        }


class SOAPAdapter(BaseProtocolAdapter):
    """Adapter for legacy XML SOAP envelope envelopes and Web Services Description Language (WSDL)."""

    def call(
        self,
        endpoint: str,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        action = payload.get("soap_action", "Invoke")
        return {
            "protocol": "SOAP",
            "endpoint": endpoint,
            "soap_action": action,
            "body": payload.get("body", {}),
        }


class gRPCAdapter(BaseProtocolAdapter):
    """Adapter for Protobuf and gRPC RPC invocations."""

    def call(
        self,
        endpoint: str,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        service_method = payload.get("method", "Service/Method")
        return {
            "protocol": "gRPC",
            "endpoint": endpoint,
            "method": service_method,
            "message": payload.get("message", {}),
        }
