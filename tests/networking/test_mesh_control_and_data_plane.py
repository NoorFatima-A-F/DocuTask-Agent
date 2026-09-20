"""Tests for Mesh Control Plane, Data Plane Interceptor, and Service Proxies."""

import pytest
from app.networking.mesh.control_plane import (
    MeshNode,
    MeshServiceSpec,
    MeshState,
    ProtocolType,
    ServiceMeshController,
)
from app.networking.mesh.data_plane import (
    DataPlaneInterceptor,
    MeshRequest,
    MeshResponse,
    TrafficDirection,
)
from app.networking.mesh.proxy import ServiceProxy


def test_control_plane_service_registration():
    controller = ServiceMeshController(name="test-cluster-mesh")
    spec = MeshServiceSpec(
        service_name="ocr-service",
        namespace="ai-workers",
        display_name="OCR Processing Engine",
        protocols=[ProtocolType.HTTP_2, ProtocolType.GRPC],
    )
    registered = controller.register_service(spec)
    assert registered.service_name == "ocr-service"
    assert controller.topology.active_version > 1

    fetched = controller.get_service("ocr-service", namespace="ai-workers")
    assert fetched is not None
    assert fetched.display_name == "OCR Processing Engine"

    # List services
    services = controller.list_services(namespace="ai-workers")
    assert len(services) == 1


def test_control_plane_node_lifecycle():
    controller = ServiceMeshController()
    node = MeshNode(
        node_id="node-ocr-01",
        service_name="ocr-service",
        namespace="default",
        cluster_id="cluster-primary",
        region="us-central1",
        ip_address="10.0.1.5",
        port=8080,
    )
    controller.register_node(node)
    assert controller.get_node("node-ocr-01") is not None

    # Heartbeat
    hb_ok = controller.heartbeat_node("node-ocr-01", healthy=True)
    assert hb_ok is True

    # Snapshot config
    cfg = controller.get_active_config()
    assert cfg["nodes_count"] == 1
    assert cfg["healthy_nodes"] == 1

    # Deregister
    assert controller.deregister_node("node-ocr-01") is True
    assert controller.get_node("node-ocr-01") is None


def test_data_plane_inbound_outbound_pipeline():
    interceptor = DataPlaneInterceptor(
        node_id="node-worker-01",
        service_name="worker-service",
        namespace="default",
    )

    # Add outbound header inspection
    def outbound_header_filter(req: MeshRequest):
        req.headers["X-Mesh-Custom"] = "OutboundInjected"
        return None

    interceptor.add_outbound_filter(outbound_header_filter)

    outbound_req = MeshRequest(
        source_service="worker-service",
        target_service="db-service",
        action="query",
        payload={"table": "users"},
    )

    outbound_res = interceptor.process_outbound(
        outbound_req,
        forward_fn=lambda r: MeshResponse(
            status_code=200,
            payload={"status": "ok", "hdr": r.headers.get("X-Mesh-Custom")},
        ),
    )

    assert outbound_res.status_code == 200
    assert outbound_res.payload["hdr"] == "OutboundInjected"
    assert outbound_res.duration_ms >= 0


def test_service_proxy_stats():
    proxy = ServiceProxy(service_name="payment-service")
    
    # Send request
    res = proxy.send(
        target_service="fraud-check",
        action="validate",
        payload={"amount": 100},
    )
    assert res.status_code == 200
    assert proxy.stats.total_requests == 1
    assert proxy.stats.outbound_requests == 1
    assert proxy.stats.successful_requests == 1

    # Receive request
    inbound_req = MeshRequest(
        source_service="client-app",
        target_service="payment-service",
        action="charge",
        payload={"order_id": "ord-123"},
    )
    in_res = proxy.receive(
        inbound_req,
        handler_fn=lambda r: MeshResponse(status_code=200, payload={"charged": True}),
    )
    assert in_res.status_code == 200
    assert proxy.stats.total_requests == 2
    assert proxy.stats.inbound_requests == 1
