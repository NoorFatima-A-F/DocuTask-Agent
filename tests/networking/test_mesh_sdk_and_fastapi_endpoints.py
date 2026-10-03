"""Tests for Mesh SDK, Decorators, and FastAPI REST Endpoints."""


from app.networking.api.routes import (
    register_service,
    list_services,
    register_endpoint,
    list_endpoints,
    create_policy,
    create_route,
    configure_traffic_split,
    issue_certificate,
    get_mesh_telemetry,
    execute_mesh_call,
    get_mesh_client,
)
from app.networking.api.schemas import (
    CertificateIssueRequest,
    EndpointRegistrationRequest,
    MeshCallRequest,
    PolicyCreateRequest,
    RouteRuleCreateRequest,
    ServiceRegistrationRequest,
    TrafficSplitRequest,
)
from app.networking.mesh.data_plane import MeshResponse
from app.networking.sdk.client import MeshClient
from app.networking.sdk.decorators import mesh_endpoint, mesh_service, with_retry


def test_mesh_client_end_to_end_call():
    client = MeshClient(service_name="frontend-service", namespace="default")

    # Register local target handler
    client.register_handler(
        service_name="backend-service",
        action="calculate",
        handler_fn=lambda r: MeshResponse(
            status_code=200,
            payload={"sum": sum(r.payload.get("numbers", []))},
        ),
    )

    res = client.call(
        target_service="backend-service",
        action="calculate",
        payload={"numbers": [1, 2, 3, 4, 5]},
    )

    assert res.status_code == 200
    assert res.payload["sum"] == 15
    assert res.duration_ms >= 0


def test_sdk_decorators():
    @mesh_service(name="document-indexer", namespace="search")
    class Indexer:
        @mesh_endpoint(action="index_document")
        def index(self, doc_id: str):
            return {"indexed": doc_id}

    idx = Indexer()
    assert getattr(Indexer, "__mesh_service_name__") == "document-indexer"
    assert getattr(idx.index, "__mesh_action__") == "index_document"
    assert idx.index("doc-123") == {"indexed": "doc-123"}

    # Retry decorator
    attempts = 0

    @with_retry(max_attempts=3, initial_backoff_ms=5.0)
    def flaky_func():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("fail")
        return "success"

    assert flaky_func() == "success"
    assert attempts == 3


def test_fastapi_network_routes():
    client = get_mesh_client()

    # 1. Register service
    svc_req = ServiceRegistrationRequest(
        service_name="ai-worker",
        namespace="default",
        display_name="AI Worker",
    )
    res_svc = register_service(svc_req, client=client)
    assert res_svc.service_name == "ai-worker"

    # 2. List services
    res_list = list_services(namespace=None, client=client)
    assert len(res_list) >= 1

    # 3. Register endpoint
    ep_req = EndpointRegistrationRequest(
        endpoint_id="ep-test-1",
        service_name="ai-worker",
        host="10.0.0.1",
        port=8080,
    )
    res_ep = register_endpoint(ep_req, client=client)
    assert res_ep.endpoint_id == "ep-test-1"

    # 4. List endpoints
    res_eps = list_endpoints(service_name="ai-worker", client=client)
    assert len(res_eps) >= 1

    # 5. Create policy
    pol_req = PolicyCreateRequest(
        policy_id="pol-allow-ai",
        name="Allow AI Worker",
        target_service="ai-worker",
        action="ALLOW",
    )
    res_pol = create_policy(pol_req, client=client)
    assert res_pol["status"] == "created"

    # 6. Create route
    route_req = RouteRuleCreateRequest(
        rule_id="route-ai-v1",
        name="Route to AI v1",
        target_service="ai-worker",
    )
    res_route = create_route(route_req, client=client)
    assert res_route["status"] == "created"

    # 7. Configure traffic split
    split_req = TrafficSplitRequest(
        split_id="split-ai",
        service_name="ai-worker",
        splits=[{"version": "v1", "weight": 100}],
    )
    res_split = configure_traffic_split(split_req, client=client)
    assert res_split["status"] == "configured"

    # 8. Issue certificate
    cert_req = CertificateIssueRequest(
        subject="CN=ai-worker.default",
        san_uris=["spiffe://docutask.internal/ns/default/sa/ai-worker"],
    )
    res_cert = issue_certificate(cert_req, client=client)
    assert "serial_number" in res_cert

    # 9. Execute mesh call
    client.register_handler(
        service_name="ai-worker",
        action="ping",
        handler_fn=lambda r: MeshResponse(status_code=200, payload={"pong": True}),
    )
    call_req = MeshCallRequest(
        target_service="ai-worker",
        action="ping",
    )
    res_call = execute_mesh_call(call_req, client=client)
    assert res_call.status_code == 200

    # 10. Get telemetry
    res_telemetry = get_mesh_telemetry(client=client)
    assert res_telemetry["total_requests"] >= 1
