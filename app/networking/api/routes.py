"""FastAPI REST API Routes for Enterprise Service Mesh & Network Platform."""

from typing import List, Optional
from fastapi import APIRouter, Depends

from .schemas import (
    CertificateIssueRequest,
    EndpointRegistrationRequest,
    EndpointResponseSchema,
    MeshCallRequest,
    MeshCallResponse,
    PolicyCreateRequest,
    RouteRuleCreateRequest,
    ServiceRegistrationRequest,
    ServiceResponseSchema,
    TrafficSplitRequest,
)
from ..discovery.registry import EndpointHealth, ServiceEndpoint
from ..mesh.control_plane import MeshServiceSpec
from ..routing.router import MatchCondition, RouteDestination, RouteRule
from ..routing.traffic_split import SplitType, TrafficSplitConfig, VersionSplit
from ..security.policies import NetworkPolicy, NetworkPolicyRule, PolicyAction
from ..sdk.client import MeshClient

router = APIRouter(prefix="/network", tags=["Network Control Plane & Service Mesh"])
network_mesh_router = router

_global_mesh_client: Optional[MeshClient] = None


def get_mesh_client() -> MeshClient:
    global _global_mesh_client
    if _global_mesh_client is None:
        _global_mesh_client = MeshClient(service_name="api-gateway", namespace="default")
    return _global_mesh_client


@router.post("/services", response_model=ServiceResponseSchema)
def register_service(
    req: ServiceRegistrationRequest,
    client: MeshClient = Depends(get_mesh_client),
):
    spec = MeshServiceSpec(
        service_name=req.service_name,
        namespace=req.namespace,
        display_name=req.display_name,
        description=req.description,
        mtls_required=req.mtls_required,
        timeout_ms=req.timeout_ms,
        tags=req.tags,
    )
    res = client.controller.register_service(spec)
    return ServiceResponseSchema(
        service_name=res.service_name,
        namespace=res.namespace,
        display_name=res.display_name,
        mtls_required=res.mtls_required,
        timeout_ms=res.timeout_ms,
        tags=res.tags,
    )


@router.get("/services", response_model=List[ServiceResponseSchema])
def list_services(
    namespace: Optional[str] = None,
    client: MeshClient = Depends(get_mesh_client),
):
    services = client.controller.list_services(namespace=namespace)
    return [
        ServiceResponseSchema(
            service_name=s.service_name,
            namespace=s.namespace,
            display_name=s.display_name,
            mtls_required=s.mtls_required,
            timeout_ms=s.timeout_ms,
            tags=s.tags,
        )
        for s in services
    ]


@router.post("/endpoints", response_model=EndpointResponseSchema)
def register_endpoint(
    req: EndpointRegistrationRequest,
    client: MeshClient = Depends(get_mesh_client),
):
    ep = ServiceEndpoint(
        endpoint_id=req.endpoint_id,
        service_name=req.service_name,
        namespace=req.namespace,
        host=req.host,
        port=req.port,
        region=req.region,
        zone=req.zone,
        weight=req.weight,
        health=EndpointHealth.HEALTHY,
    )
    client.registry.register_endpoint(ep)
    return EndpointResponseSchema(
        endpoint_id=ep.endpoint_id,
        service_name=ep.service_name,
        host=ep.host,
        port=ep.port,
        namespace=ep.namespace,
        region=ep.region,
        zone=ep.zone,
        weight=ep.weight,
        health=ep.health.value,
    )


@router.get("/endpoints", response_model=List[EndpointResponseSchema])
def list_endpoints(
    service_name: Optional[str] = None,
    namespace: Optional[str] = None,
    client: MeshClient = Depends(get_mesh_client),
):
    endpoints = client.registry.list_endpoints(
        service_name=service_name,
        namespace=namespace,
        healthy_only=False,
    )
    return [
        EndpointResponseSchema(
            endpoint_id=ep.endpoint_id,
            service_name=ep.service_name,
            host=ep.host,
            port=ep.port,
            namespace=ep.namespace,
            region=ep.region,
            zone=ep.zone,
            weight=ep.weight,
            health=ep.health.value,
        )
        for ep in endpoints
    ]


@router.post("/policies")
def create_policy(
    req: PolicyCreateRequest,
    client: MeshClient = Depends(get_mesh_client),
):
    rule = NetworkPolicyRule(
        rule_id=f"rule-{req.policy_id}",
        source_service=req.source_service,
        source_namespace=req.source_namespace,
        target_service=req.target_service,
        target_namespace=req.target_namespace,
        allowed_methods=req.allowed_methods,
        allowed_paths=req.allowed_paths,
        action=PolicyAction(req.action.upper()),
        priority=req.priority,
    )
    policy = NetworkPolicy(
        policy_id=req.policy_id,
        name=req.name,
        namespace=req.namespace,
        default_action=PolicyAction(req.default_action.upper()),
        rules=[rule],
    )
    client.policy_engine.add_policy(policy)
    return {"policy_id": policy.policy_id, "status": "created"}


@router.post("/routes")
def create_route(
    req: RouteRuleCreateRequest,
    client: MeshClient = Depends(get_mesh_client),
):
    rule = RouteRule(
        rule_id=req.rule_id,
        name=req.name,
        matches=[MatchCondition(path=req.path_prefix, path_type="prefix")],
        destinations=[
            RouteDestination(
                service_name=req.target_service,
                namespace=req.namespace,
                version=req.version,
                weight=req.weight,
            )
        ],
        priority=req.priority,
    )
    client.router.add_rule(rule)
    return {"rule_id": rule.rule_id, "status": "created"}


@router.post("/traffic/split")
def configure_traffic_split(
    req: TrafficSplitRequest,
    client: MeshClient = Depends(get_mesh_client),
):
    splits = [
        VersionSplit(version=s.get("version", "v1"), weight=int(s.get("weight", 100)))
        for s in req.splits
    ]
    cfg = TrafficSplitConfig(
        split_id=req.split_id,
        service_name=req.service_name,
        namespace=req.namespace,
        split_type=SplitType(req.split_type.upper()),
        splits=splits,
        shadow_version=req.shadow_version,
        shadow_percentage=req.shadow_percentage,
    )
    client.traffic_splitter.set_split_config(cfg)
    return {"split_id": cfg.split_id, "status": "configured"}


@router.post("/certificates/issue")
def issue_certificate(
    req: CertificateIssueRequest,
    client: MeshClient = Depends(get_mesh_client),
):
    cert = client.cert_manager.issue_certificate(
        subject=req.subject,
        san_uris=req.san_uris,
        validity_seconds=req.validity_days * 86400.0,
    )
    return {
        "serial_number": cert.serial_number,
        "subject": cert.subject,
        "valid_from": cert.valid_from,
        "valid_to": cert.valid_to,
        "san_uris": cert.san_uris,
    }


@router.get("/telemetry")
def get_mesh_telemetry(client: MeshClient = Depends(get_mesh_client)):
    summary = client.metrics.get_summary()
    return {
        "total_requests": summary.total_requests,
        "successful_requests": summary.successful_requests,
        "failed_requests": summary.failed_requests,
        "error_rate_pct": summary.error_rate_pct,
        "req_per_sec": summary.req_per_sec,
        "p50_latency_ms": summary.p50_latency_ms,
        "p90_latency_ms": summary.p90_latency_ms,
        "p95_latency_ms": summary.p95_latency_ms,
        "p99_latency_ms": summary.p99_latency_ms,
    }


@router.post("/call", response_model=MeshCallResponse)
def execute_mesh_call(
    req: MeshCallRequest,
    client: MeshClient = Depends(get_mesh_client),
):
    res = client.call(
        target_service=req.target_service,
        action=req.action,
        payload=req.payload,
        target_namespace=req.target_namespace,
        timeout_ms=req.timeout_ms,
    )
    return MeshCallResponse(
        status_code=res.status_code,
        request_id=res.request_id,
        duration_ms=res.duration_ms,
        payload=res.payload,
        error_message=res.error_message,
    )
