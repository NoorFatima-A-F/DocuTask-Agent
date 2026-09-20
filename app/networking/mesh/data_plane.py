"""Data Plane Interceptor for Mesh Communication."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class TrafficDirection(str, Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"


@dataclass
class MeshRequest:
    source_service: str
    target_service: str
    action: str
    path: str = "/"
    method: str = "POST"
    headers: Dict[str, str] = field(default_factory=dict)
    payload: Dict[str, Any] = field(default_factory=dict)
    request_id: str = field(default_factory=lambda: f"req-{uuid.uuid4().hex[:10]}")
    trace_id: str = field(default_factory=lambda: f"trace-{uuid.uuid4().hex[:12]}")
    span_id: str = field(default_factory=lambda: f"span-{uuid.uuid4().hex[:8]}")
    source_namespace: str = "default"
    target_namespace: str = "default"
    timeout_ms: float = 5000.0
    created_at: float = field(default_factory=time.time)


@dataclass
class MeshResponse:
    status_code: int
    headers: Dict[str, str] = field(default_factory=dict)
    payload: Any = None
    request_id: str = ""
    duration_ms: float = 0.0
    error_message: Optional[str] = None
    routed_node_id: Optional[str] = None
    applied_policy: Optional[str] = None


class DataPlaneInterceptor:
    """Core data plane interceptor for inbound and outbound mesh traffic."""

    def __init__(self, node_id: str, service_name: str, namespace: str = "default"):
        self.node_id = node_id
        self.service_name = service_name
        self.namespace = namespace
        self._inbound_filters: List[Callable[[MeshRequest], Optional[MeshResponse]]] = []
        self._outbound_filters: List[Callable[[MeshRequest], Optional[MeshResponse]]] = []
        self._active_connections = 0

    @property
    def active_connections(self) -> int:
        return self._active_connections

    def add_inbound_filter(self, filter_fn: Callable[[MeshRequest], Optional[MeshResponse]]) -> None:
        self._inbound_filters.append(filter_fn)

    def add_outbound_filter(self, filter_fn: Callable[[MeshRequest], Optional[MeshResponse]]) -> None:
        self._outbound_filters.append(filter_fn)

    def process_outbound(
        self,
        request: MeshRequest,
        forward_fn: Callable[[MeshRequest], MeshResponse],
    ) -> MeshResponse:
        """Process an outbound request from this service through outbound interceptors."""
        start_time = time.time()
        self._active_connections += 1
        try:
            # Inject source metadata if missing
            if not request.source_service:
                request.source_service = self.service_name
            if not request.source_namespace:
                request.source_namespace = self.namespace

            # Apply outbound filters (e.g., auth, fault injection, rate limits)
            for f in self._outbound_filters:
                intercepted_response = f(request)
                if intercepted_response is not None:
                    intercepted_response.duration_ms = (time.time() - start_time) * 1000
                    return intercepted_response

            # Forward to next hop (e.g., router / transport)
            response = forward_fn(request)
            response.duration_ms = (time.time() - start_time) * 1000
            response.request_id = request.request_id
            return response
        finally:
            self._active_connections = max(0, self._active_connections - 1)

    def process_inbound(
        self,
        request: MeshRequest,
        handler_fn: Callable[[MeshRequest], MeshResponse],
    ) -> MeshResponse:
        """Process an inbound request received by this service through inbound interceptors."""
        start_time = time.time()
        self._active_connections += 1
        try:
            # Apply inbound filters (e.g., mTLS verify, zero-trust auth, rate limit)
            for f in self._inbound_filters:
                intercepted_response = f(request)
                if intercepted_response is not None:
                    intercepted_response.duration_ms = (time.time() - start_time) * 1000
                    return intercepted_response

            # Dispatch to local application handler
            response = handler_fn(request)
            response.duration_ms = (time.time() - start_time) * 1000
            response.request_id = request.request_id
            return response
        finally:
            self._active_connections = max(0, self._active_connections - 1)
