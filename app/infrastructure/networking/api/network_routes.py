"""FastAPI REST routes for Enterprise Cloud Networking & Security Control Plane."""

from dataclasses import asdict
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from ..sdk.network_sdk import NetworkSDK
from ..policies.network_policy import NetworkPolicy, NetworkPolicyRule, NetworkPolicyType
from ..control_plane.registry import ZeroTrustAction

router = APIRouter(prefix="/network", tags=["Cloud Networking & Zero Trust Security"])

# Global shared SDK instance
_sdk_instance: Optional[NetworkSDK] = None


def get_network_sdk() -> NetworkSDK:
    """Obtain or initialize singleton NetworkSDK instance."""
    global _sdk_instance
    if _sdk_instance is None:
        _sdk_instance = NetworkSDK()
    return _sdk_instance


# --- Pydantic Request Models ---
class ServiceRegisterRequest(BaseModel):
    service_name: str
    host: str
    port: int
    namespace: str = "default"
    region: str = "us-east-1"
    cluster_id: str = "cluster-alpha"
    labels: Dict[str, str] = Field(default_factory=dict)
    capabilities: List[str] = Field(default_factory=list)
    tenant_scope: List[str] = Field(default_factory=lambda: ["*"])


class NetworkPolicyCreateRequest(BaseModel):
    policy_id: str
    name: str
    target_service: str
    namespace: str = "default"
    policy_types: List[str] = Field(default_factory=lambda: ["ingress", "egress"])
    allowed_namespaces: List[str] = Field(default_factory=lambda: ["*"])
    allowed_ports: List[int] = Field(default_factory=list)
    allowed_protocols: List[str] = Field(default_factory=lambda: ["https", "grpc"])
    action: str = "allow"


class CertificateRotateRequest(BaseModel):
    serial_number: str


class SecureCallRequest(BaseModel):
    caller_service: str
    target_service: str
    method: str = "GET"
    path: str = "/"
    payload: Optional[Dict[str, Any]] = None
    headers: Dict[str, str] = Field(default_factory=dict)
    tenant_id: Optional[str] = None


class FailoverTriggerRequest(BaseModel):
    service_name: str
    target_region: str
    drain_time_seconds: int = 30


# --- Endpoints ---
@router.get("/services")
def list_registered_services() -> Dict[str, Any]:
    """List all dynamically registered services."""
    sdk = get_network_sdk()
    instances = sdk.discovery_registry.list_all_instances()
    return {
        "services_count": len(sdk.discovery_registry.list_all_services()),
        "instances_count": len(instances),
        "instances": [
            {
                "instance_id": i.instance_id,
                "service_name": i.service_name,
                "host": i.host,
                "port": i.port,
                "namespace": i.namespace,
                "region": i.region,
                "cluster_id": i.cluster_id,
                "health_state": i.health_state.value,
                "url": i.url,
            }
            for i in instances
        ],
    }


@router.post("/services")
def register_service(req: ServiceRegisterRequest) -> Dict[str, Any]:
    """Register a new service instance."""
    sdk = get_network_sdk()
    inst = sdk.register_service(
        service_name=req.service_name,
        host=req.host,
        port=req.port,
        namespace=req.namespace,
        region=req.region,
        cluster_id=req.cluster_id,
        labels=req.labels,
        capabilities=req.capabilities,
        tenant_scope=req.tenant_scope,
    )
    return {
        "instance_id": inst.instance_id,
        "service_name": inst.service_name,
        "status": "registered",
        "url": inst.url,
    }


@router.get("/routes")
def list_routes() -> Dict[str, Any]:
    """List active routing rules."""
    sdk = get_network_sdk()
    routes = sdk.control_plane_registry.list_routes()
    return {
        "routes_count": len(routes),
        "routes": [
            {
                "rule_id": r.rule_id,
                "service_name": r.service_name,
                "strategy": r.strategy.value,
                "endpoints_count": len(r.endpoints),
                "canary_weight": r.canary_weight,
            }
            for r in routes
        ],
    }


@router.get("/policies")
def list_policies() -> Dict[str, Any]:
    """List declarative network policies."""
    sdk = get_network_sdk()
    policies = sdk.network_policy_engine.list_policies()
    return {
        "policies_count": len(policies),
        "policies": [
            {
                "policy_id": p.policy_id,
                "name": p.name,
                "target_service": p.target_service,
                "namespace": p.namespace,
                "is_active": p.is_active,
            }
            for p in policies
        ],
    }


@router.post("/policies")
def create_policy(req: NetworkPolicyCreateRequest) -> Dict[str, Any]:
    """Create a new declarative network policy."""
    sdk = get_network_sdk()
    act = ZeroTrustAction.ALLOW if req.action.lower() == "allow" else ZeroTrustAction.DENY
    rule = NetworkPolicyRule(
        rule_id=f"rule-{req.policy_id}",
        direction=NetworkPolicyType.INGRESS,
        allowed_namespaces=req.allowed_namespaces,
        allowed_ports=req.allowed_ports,
        allowed_protocols=req.allowed_protocols,
        action=act,
    )
    policy = NetworkPolicy(
        policy_id=req.policy_id,
        name=req.name,
        target_service=req.target_service,
        namespace=req.namespace,
        policy_types=[NetworkPolicyType(t) for t in req.policy_types if t in ("ingress", "egress")],
        ingress_rules=[rule],
    )
    sdk.apply_network_policy(policy)
    return {"policy_id": policy.policy_id, "status": "applied"}


@router.post("/certificates/rotate")
def rotate_certificate(req: CertificateRotateRequest) -> Dict[str, Any]:
    """Rotate an X.509 workload certificate."""
    sdk = get_network_sdk()
    new_cert = sdk.rotate_certificate(req.serial_number)
    if not new_cert:
        raise HTTPException(status_code=404, detail="Certificate serial number not found")
    return {
        "status": "rotated",
        "new_serial": new_cert.serial_number,
        "subject_cn": new_cert.subject_cn,
        "expires_at": new_cert.expires_at.isoformat(),
    }


@router.get("/traffic")
def get_traffic_telemetry() -> Dict[str, Any]:
    """Retrieve network traffic and flow summary."""
    sdk = get_network_sdk()
    summary = sdk.get_telemetry_summary()
    recent_flows = sdk.flow_logger.get_recent_flows(limit=20)
    return {
        "metrics": asdict(summary),
        "recent_flows_count": len(recent_flows),
    }


@router.get("/discovery")
def resolve_service_endpoint(service: str = Query(..., description="Service name or alias")) -> Dict[str, Any]:
    """Resolve a service endpoint via dynamic discovery."""
    sdk = get_network_sdk()
    resolved = sdk.resolve_service(service)
    if not resolved:
        raise HTTPException(status_code=404, detail=f"Service '{service}' not found")
    return {
        "service_name": resolved.service_name,
        "url": resolved.url,
        "host": resolved.host,
        "port": resolved.port,
        "region": resolved.region,
        "spiffe_id": resolved.spiffe_id,
        "resolved_via": resolved.resolved_via,
    }


@router.post("/failover")
def trigger_failover(req: FailoverTriggerRequest) -> Dict[str, Any]:
    """Trigger regional traffic failover."""
    sdk = get_network_sdk()
    sdk.flow_logger.emit_security_event(
        event_type=sdk.flow_logger.get_recent_events()[0].event_type.TRAFFIC_SHIFTED if sdk.flow_logger.get_recent_events() else "TrafficShifted",
        source="TrafficFailoverManager",
        details={"service": req.service_name, "target_region": req.target_region},
        severity="WARN",
    )
    return {
        "status": "failover_initiated",
        "service": req.service_name,
        "target_region": req.target_region,
    }


@router.post("/call")
def make_secure_call(req: SecureCallRequest) -> Dict[str, Any]:
    """Execute a secure zero-trust call between services."""
    sdk = get_network_sdk()
    res = sdk.secure_call(
        caller_service=req.caller_service,
        target_service=req.target_service,
        method=req.method,
        path=req.path,
        payload=req.payload,
        headers=req.headers,
        tenant_id=req.tenant_id,
    )
    return {
        "success": res.success,
        "status_code": res.status_code,
        "target_endpoint": res.target_endpoint,
        "target_spiffe": res.target_spiffe,
        "latency_ms": res.latency_ms,
        "error": res.error,
        "data": res.data,
    }
