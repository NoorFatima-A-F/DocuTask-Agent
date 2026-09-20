"""Tests for Unified NetworkSDK and FastAPI REST API routes."""

import pytest
from app.infrastructure.networking import NetworkSDK, get_network_sdk
from app.infrastructure.networking.api.network_routes import (
    list_registered_services,
    register_service,
    list_routes,
    list_policies,
    create_policy,
    rotate_certificate,
    get_traffic_telemetry,
    resolve_service_endpoint,
    make_secure_call,
    ServiceRegisterRequest,
    NetworkPolicyCreateRequest,
    CertificateRotateRequest,
    SecureCallRequest,
)


def test_network_sdk_end_to_end_secure_call() -> None:
    sdk = NetworkSDK()

    # Register destination service
    sdk.register_service(
        service_name="ocr-processor",
        host="10.0.1.10",
        port=8443,
        capabilities=["ocr"],
    )

    # Make secure call
    res = sdk.secure_call(
        caller_service="workflow-coordinator",
        target_service="ocr-processor",
        method="POST",
        path="/v1/ocr",
        payload={"doc_id": "doc_999"},
    )
    assert res.success is True
    assert res.status_code == 200
    assert res.target_endpoint == "https://10.0.1.10:8443"
    assert "ocr-processor" in res.target_spiffe


def test_network_fastapi_routes() -> None:
    sdk = get_network_sdk()

    # 1. Register service route
    reg_req = ServiceRegisterRequest(
        service_name="ai-summarizer",
        host="10.0.3.50",
        port=9000,
        capabilities=["summary"],
    )
    reg_resp = register_service(reg_req)
    assert reg_resp["status"] == "registered"

    # 2. List services route
    services_resp = list_registered_services()
    assert services_resp["services_count"] >= 1

    # 3. Discovery route
    disc_resp = resolve_service_endpoint("ai-summarizer")
    assert disc_resp["service_name"] == "ai-summarizer"
    assert disc_resp["port"] == 9000

    # 4. List routes
    routes_resp = list_routes()
    assert routes_resp["routes_count"] >= 1

    # 5. Create policy route
    pol_req = NetworkPolicyCreateRequest(
        policy_id="pol_api_test",
        name="API Test Policy",
        target_service="ai-summarizer",
        action="allow",
    )
    pol_resp = create_policy(pol_req)
    assert pol_resp["status"] == "applied"

    # 6. Secure call route
    call_req = SecureCallRequest(
        caller_service="workflow-engine",
        target_service="ai-summarizer",
        method="POST",
        path="/summarize",
        payload={"text": "document text"},
    )
    call_resp = make_secure_call(call_req)
    assert call_resp["success"] is True
    assert call_resp["status_code"] == 200

    # 7. Traffic telemetry route
    traffic_resp = get_traffic_telemetry()
    assert traffic_resp["metrics"]["total_requests"] >= 1
