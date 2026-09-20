"""Service Proxy Sidecar for Mesh Interception."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional

from .data_plane import DataPlaneInterceptor, MeshRequest, MeshResponse


@dataclass
class ProxyStats:
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    inbound_requests: int = 0
    outbound_requests: int = 0
    avg_latency_ms: float = 0.0
    _total_latency_ms: float = 0.0


class ServiceProxy:
    """Sidecar Proxy instance attached to a service workload instance."""

    def __init__(
        self,
        service_name: str,
        node_id: Optional[str] = None,
        namespace: str = "default",
        interceptor: Optional[DataPlaneInterceptor] = None,
    ):
        self.service_name = service_name
        self.node_id = node_id or f"node-{service_name}-{uuid.uuid4().hex[:6]}"
        self.namespace = namespace
        self.interceptor = interceptor or DataPlaneInterceptor(
            node_id=self.node_id,
            service_name=self.service_name,
            namespace=self.namespace,
        )
        self.stats = ProxyStats()

    def send(
        self,
        target_service: str,
        action: str,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        target_namespace: str = "default",
        forward_fn: Optional[Callable[[MeshRequest], MeshResponse]] = None,
    ) -> MeshResponse:
        """Send an outbound request from this service through the proxy."""
        req = MeshRequest(
            source_service=self.service_name,
            source_namespace=self.namespace,
            target_service=target_service,
            target_namespace=target_namespace,
            action=action,
            payload=payload,
            headers=headers or {},
        )

        default_forward: Callable[[MeshRequest], MeshResponse] = forward_fn or (
            lambda r: MeshResponse(
                status_code=200,
                payload={"acknowledged": True, "target": r.target_service, "action": r.action},
                routed_node_id=self.node_id,
            )
        )

        res = self.interceptor.process_outbound(req, default_forward)
        self._record_stats(res, inbound=False)
        return res

    def receive(
        self,
        request: MeshRequest,
        handler_fn: Callable[[MeshRequest], MeshResponse],
    ) -> MeshResponse:
        """Receive an inbound request directed to this service through the proxy."""
        res = self.interceptor.process_inbound(request, handler_fn)
        self._record_stats(res, inbound=True)
        return res

    def _record_stats(self, response: MeshResponse, inbound: bool) -> None:
        self.stats.total_requests += 1
        if inbound:
            self.stats.inbound_requests += 1
        else:
            self.stats.outbound_requests += 1

        if 200 <= response.status_code < 400:
            self.stats.successful_requests += 1
        else:
            self.stats.failed_requests += 1

        self.stats._total_latency_ms += response.duration_ms
        self.stats.avg_latency_ms = self.stats._total_latency_ms / max(1, self.stats.total_requests)
