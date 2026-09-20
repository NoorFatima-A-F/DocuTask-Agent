"""Unified Network SDK providing high-level programmatic network capabilities."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import time
from typing import Any, Callable, Dict, List, Optional
import uuid

from ..control_plane.registry import (
    NetworkControlPlaneRegistry,
    RouteRule,
    RoutingStrategy,
    NetworkEndpoint,
    ZeroTrustAction,
    NetworkProtocol,
)
from ..control_plane.manager import NetworkControlPlaneManager
from ..control_plane.routing import GlobalNetworkRouter
from ..discovery.registry import (
    ServiceDiscoveryRegistry,
    ServiceRegistration,
    ServiceInstance,
    ServiceHealthState,
)
from ..discovery.resolver import ServiceResolver, ResolvedServiceTarget
from ..discovery.heartbeat import ServiceHeartbeatManager
from ..mesh.adapters import IServiceMeshAdapter
from ..mesh.istio import IstioMeshAdapter
from ..mesh.linkerd import LinkerdMeshAdapter
from ..mesh.consul import ConsulMeshAdapter
from ..traffic.load_balancing import LoadBalancerEngine
from ..traffic.routing import TrafficRouter, RoutingDecision
from ..traffic.retries import RetryEngine, RetryPolicy
from ..traffic.failover import TrafficFailoverManager
from ..security.workload_identity import SPIFFEIdentity, WorkloadSVID, WorkloadIdentityManager
from ..security.certificates import CertificateAuthorityManager, X509Certificate
from ..security.mtls import MTLSEngine, MTLSValidationResult
from ..security.authorization import ZeroTrustPolicyEngine, ZeroTrustRule, ZeroTrustEvaluationResult
from ..policies.network_policy import NetworkPolicyEngine, NetworkPolicy, NetworkPolicyRule, NetworkPolicyType
from ..policies.ingress import IngressPolicyManager
from ..policies.egress import EgressPolicyManager
from ..gateway.api_gateway import APIGatewaySecurityManager
from ..telemetry.traffic_metrics import NetworkTelemetryCollector, NetworkMetricSummary
from ..telemetry.flow_logs import NetworkFlowLogger, NetworkSecurityEventType, NetworkSecurityEvent, NetworkFlowRecord


@dataclass
class NetworkCallResult:
    """Outcome of a secure network call through the Network SDK."""
    success: bool
    status_code: int
    data: Optional[Any] = None
    target_endpoint: Optional[str] = None
    target_spiffe: Optional[str] = None
    latency_ms: float = 0.0
    attempts: int = 1
    routed_via: str = "direct"
    error: Optional[str] = None
    flow_id: Optional[str] = None


class NetworkSDK:
    """Central programmatic façade for enterprise cloud networking and zero-trust security."""

    def __init__(
        self,
        trust_domain: str = "docutask.internal",
        default_namespace: str = "default",
        default_region: str = "us-east-1",
        default_cluster: str = "cluster-alpha",
    ) -> None:
        self.trust_domain = trust_domain
        self.default_namespace = default_namespace
        self.default_region = default_region
        self.default_cluster = default_cluster

        # 1. Control Plane & Discovery
        self.control_plane_registry = NetworkControlPlaneRegistry()
        self.control_plane_manager = NetworkControlPlaneManager(self.control_plane_registry)
        self.discovery_registry = ServiceDiscoveryRegistry()
        self.resolver = ServiceResolver(self.discovery_registry)
        self.heartbeat_manager = ServiceHeartbeatManager(self.discovery_registry)
        self.global_router = GlobalNetworkRouter(self.control_plane_registry)

        # 2. Service Mesh Adapters
        self.mesh_adapters: Dict[str, IServiceMeshAdapter] = {
            "istio": IstioMeshAdapter(),
            "linkerd": LinkerdMeshAdapter(),
            "consul": ConsulMeshAdapter(),
        }

        # 3. Traffic Management & Resilience
        self.load_balancer = LoadBalancerEngine()
        self.traffic_router = TrafficRouter()
        self.retry_engine = RetryEngine()
        self.failover_manager = TrafficFailoverManager()

        # 4. Security & Identity
        self.identity_manager = WorkloadIdentityManager(trust_domain=trust_domain)
        self.ca_manager = CertificateAuthorityManager(trust_domain=trust_domain)
        self.mtls_engine = MTLSEngine(self.ca_manager)
        self.zero_trust_engine = ZeroTrustPolicyEngine()

        # 5. Network Policies
        self.network_policy_engine = NetworkPolicyEngine()
        self.ingress_policy_manager = IngressPolicyManager(self.network_policy_engine)
        self.egress_policy_manager = EgressPolicyManager(self.network_policy_engine)

        # 6. Gateway & Telemetry
        self.gateway_security = APIGatewaySecurityManager()
        self.telemetry_collector = NetworkTelemetryCollector()
        self.flow_logger = NetworkFlowLogger()

        # Bootstrap internal default service identities and certs
        self._init_defaults()

    def _init_defaults(self) -> None:
        """Initialize default allow policies for system namespace."""
        self.zero_trust_engine.add_rule(ZeroTrustRule(
            rule_id="default-allow-internal",
            name="Allow Internal DocuTask Services",
            action=ZeroTrustAction.ALLOW,
            source_spiffe_pattern=f"spiffe://{self.trust_domain}/*",
            target_spiffe_pattern=f"spiffe://{self.trust_domain}/*",
            allowed_methods=["*"],
            allowed_paths=["/*"],
            priority=1000,
        ))

    # --- Service Discovery API ---
    def register_service(
        self,
        service_name: str,
        host: str,
        port: int,
        namespace: Optional[str] = None,
        region: Optional[str] = None,
        cluster_id: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        capabilities: Optional[List[str]] = None,
        tenant_scope: Optional[List[str]] = None,
    ) -> ServiceInstance:
        """Register a service workload into the dynamic discovery catalog."""
        ns = namespace or self.default_namespace
        reg = ServiceRegistration(
            service_name=service_name,
            host=host,
            port=port,
            namespace=ns,
            region=region or self.default_region,
            cluster_id=cluster_id or self.default_cluster,
            labels=labels or {},
            capabilities=capabilities or [],
            tenant_scope=tenant_scope or ["*"],
        )
        instance = self.discovery_registry.register_instance(reg)

        # Issue workload certificate automatically
        self.ca_manager.issue_workload_certificate(service_name=service_name, namespace=ns)

        # Update control plane route
        ep = NetworkEndpoint(
            host=host,
            port=port,
            region=reg.region,
            cluster_id=reg.cluster_id,
            protocol=NetworkProtocol.HTTPS,
        )
        existing_route = self.control_plane_registry.get_route(service_name)
        if existing_route:
            if ep not in existing_route.endpoints:
                existing_route.endpoints.append(ep)
        else:
            self.control_plane_registry.register_route(RouteRule(
                rule_id=f"rule-{service_name}",
                service_name=service_name,
                endpoints=[ep],
            ))

        self.flow_logger.emit_security_event(
            event_type=NetworkSecurityEventType.SERVICE_REGISTERED,
            source=service_name,
            details={"instance_id": instance.instance_id, "host": host, "port": port, "namespace": ns},
        )
        return instance

    def deregister_service(self, instance_id: str) -> bool:
        """Deregister service instance."""
        inst = self.discovery_registry.get_instance(instance_id)
        if inst:
            self.discovery_registry.deregister_instance(instance_id)
            self.flow_logger.emit_security_event(
                event_type=NetworkSecurityEventType.SERVICE_REMOVED,
                source=inst.service_name,
                details={"instance_id": instance_id},
            )
            return True
        return False

    def resolve_service(
        self,
        service_or_alias: str,
        caller_region: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ) -> Optional[ResolvedServiceTarget]:
        """Resolve a service target address."""
        return self.resolver.resolve(
            service_or_alias=service_or_alias,
            caller_region=caller_region or self.default_region,
            tenant_id=tenant_id,
        )

    # --- Secure Service-to-Service Execution ---
    def secure_call(
        self,
        caller_service: str,
        target_service: str,
        method: str = "GET",
        path: str = "/",
        payload: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        tenant_id: Optional[str] = None,
        caller_namespace: Optional[str] = None,
        mock_handler: Optional[Callable[[Dict[str, Any]], Any]] = None,
    ) -> NetworkCallResult:
        """Execute an end-to-end zero-trust secure service call."""
        start_time = time.time()
        headers = headers or {}
        ns = caller_namespace or self.default_namespace

        caller_spiffe = f"spiffe://{self.trust_domain}/ns/{ns}/sa/{caller_service}"
        target_spiffe = f"spiffe://{self.trust_domain}/ns/{self.default_namespace}/sa/{target_service}"

        # 1. Zero-Trust Policy Authorization Check
        zt_result = self.zero_trust_engine.evaluate(
            caller_spiffe=caller_spiffe,
            target_spiffe=target_spiffe,
            method=method,
            path=path,
            tenant_id=tenant_id,
        )
        if not zt_result.is_allowed:
            self.telemetry_collector.record_policy_denial()
            self.flow_logger.emit_security_event(
                event_type=NetworkSecurityEventType.POLICY_DENIED,
                source=caller_service,
                details={"target": target_service, "reason": zt_result.reason},
                severity="WARN",
            )
            flow = self.flow_logger.record_flow(
                source_address=caller_service,
                destination_address=target_service,
                source_spiffe=caller_spiffe,
                destination_spiffe=target_spiffe,
                action="DENY",
                tenant_id=tenant_id,
            )
            return NetworkCallResult(
                success=False,
                status_code=403,
                target_spiffe=target_spiffe,
                latency_ms=(time.time() - start_time) * 1000.0,
                error=f"Zero-Trust Policy Denied: {zt_result.reason}",
                flow_id=flow.flow_id,
            )

        # 2. Dynamic Service Resolution
        resolved = self.resolve_service(target_service, caller_region=self.default_region, tenant_id=tenant_id)
        if not resolved:
            return NetworkCallResult(
                success=False,
                status_code=503,
                target_spiffe=target_spiffe,
                latency_ms=(time.time() - start_time) * 1000.0,
                error=f"Service Unavailable: Could not resolve healthy instance for '{target_service}'",
            )

        # 3. Simulated mTLS Handshake Validation
        caller_cert = self.ca_manager.issue_workload_certificate(caller_service, namespace=ns)
        server_cert = self.ca_manager.issue_workload_certificate(target_service, namespace=self.default_namespace)
        mtls_res = self.mtls_engine.validate_connection(caller_cert, server_cert, expected_destination_spiffe=target_spiffe)
        if not mtls_res.is_valid:
            self.telemetry_collector.record_tls_failure()
            self.flow_logger.emit_security_event(
                event_type=NetworkSecurityEventType.MTLS_FAILURE,
                source=caller_service,
                details={"target": target_service, "error": mtls_res.error_message},
                severity="ERROR",
            )
            return NetworkCallResult(
                success=False,
                status_code=495,
                target_endpoint=resolved.url,
                target_spiffe=target_spiffe,
                latency_ms=(time.time() - start_time) * 1000.0,
                error=f"mTLS Handshake Failed: {mtls_res.error_message}",
            )

        # 4. Route & Circuit Breaker Check
        target_ep = NetworkEndpoint(
            host=resolved.host,
            port=resolved.port,
            protocol=NetworkProtocol.HTTPS,
            region=resolved.region,
            cluster_id=resolved.cluster_id,
        )
        if not self.failover_manager.can_execute(target_ep):
            return NetworkCallResult(
                success=False,
                status_code=503,
                target_endpoint=resolved.url,
                target_spiffe=target_spiffe,
                latency_ms=(time.time() - start_time) * 1000.0,
                error="Circuit Breaker OPEN: Target endpoint is failing",
            )

        # 5. Execute Handler
        duration_ms = (time.time() - start_time) * 1000.0 + 2.5
        resp_data = {"status": "ok", "caller": caller_service, "target": target_service, "data": payload}
        if mock_handler:
            try:
                resp_data = mock_handler(payload or {})
                self.failover_manager.record_success(target_ep)
            except Exception as e:
                self.failover_manager.record_failure(target_ep)
                return NetworkCallResult(
                    success=False,
                    status_code=500,
                    target_endpoint=resolved.url,
                    target_spiffe=target_spiffe,
                    latency_ms=duration_ms,
                    error=str(e),
                )
        else:
            self.failover_manager.record_success(target_ep)

        # 6. Record Flow and Telemetry
        flow = self.flow_logger.record_flow(
            source_address=caller_service,
            destination_address=resolved.url,
            source_spiffe=caller_spiffe,
            destination_spiffe=target_spiffe,
            action="ALLOW",
            bytes_transferred=len(str(payload or "")) + len(str(resp_data)),
            duration_ms=duration_ms,
            tenant_id=tenant_id,
        )
        self.telemetry_collector.record_request(
            duration_ms=duration_ms,
            success=True,
            bytes_sent=len(str(payload or "")),
            bytes_recv=len(str(resp_data)),
        )

        return NetworkCallResult(
            success=True,
            status_code=200,
            data=resp_data,
            target_endpoint=resolved.url,
            target_spiffe=target_spiffe,
            latency_ms=duration_ms,
            routed_via=resolved.resolved_via,
            flow_id=flow.flow_id,
        )

    # --- Certificate & Policy Controls ---
    def rotate_certificate(self, serial_number: str) -> Optional[X509Certificate]:
        """Rotate a certificate by serial number."""
        new_cert = self.ca_manager.rotate_certificate(serial_number)
        if new_cert:
            self.flow_logger.emit_security_event(
                event_type=NetworkSecurityEventType.CERTIFICATE_ROTATED,
                source="CertificateAuthorityManager",
                details={"old_serial": serial_number, "new_serial": new_cert.serial_number},
            )
        return new_cert

    def apply_network_policy(self, policy: NetworkPolicy) -> None:
        """Apply declarative network policy."""
        self.network_policy_engine.add_policy(policy)
        self.flow_logger.emit_security_event(
            event_type=NetworkSecurityEventType.NETWORK_POLICY_UPDATED,
            source="NetworkPolicyEngine",
            details={"policy_id": policy.policy_id, "name": policy.name, "namespace": policy.namespace},
        )

    def get_telemetry_summary(self) -> NetworkMetricSummary:
        """Return network metrics summary."""
        return self.telemetry_collector.get_summary()
