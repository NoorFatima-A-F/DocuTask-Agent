"""Enterprise Cloud Networking, Service Mesh & Zero-Trust Infrastructure Security Platform."""

# Control plane
from .control_plane.registry import (
    NetworkProtocol,
    MeshType,
    RoutingStrategy,
    ZeroTrustAction,
    CertificateStatus,
    NetworkPolicyType,
    NetworkEndpoint,
    RouteRule,
    NetworkControlPlaneRegistry,
)
from .control_plane.manager import NetworkControlPlaneManager
from .control_plane.routing import GlobalNetworkRouter

# Discovery
from .discovery.registry import (
    ServiceHealthState,
    ServiceEndpoint,
    ServiceInstance,
    ServiceRegistration,
    ServiceDiscoveryRegistry,
)
from .discovery.resolver import ResolvedServiceTarget, ServiceResolver
from .discovery.heartbeat import ServiceHeartbeatManager

# Mesh
from .mesh.adapters import IServiceMeshAdapter, MeshConfigurationManifest
from .mesh.istio import IstioMeshAdapter
from .mesh.linkerd import LinkerdMeshAdapter
from .mesh.consul import ConsulMeshAdapter

# Traffic
from .traffic.load_balancing import LoadBalancerEngine
from .traffic.routing import RoutingDecision, TrafficRouter
from .traffic.retries import RetryPolicy, RetryEngine
from .traffic.failover import CircuitState, CircuitBreakerConfig, TrafficFailoverManager

# Security
from .security.workload_identity import SPIFFEIdentity, WorkloadSVID, WorkloadIdentityManager
from .security.certificates import X509Certificate, CertificateAuthorityManager
from .security.mtls import MTLSValidationResult, MTLSEngine
from .security.authorization import ZeroTrustRule, ZeroTrustEvaluationResult, ZeroTrustPolicyEngine

# Policies
from .policies.network_policy import NetworkPolicyRule, NetworkPolicy, NetworkPolicyEngine
from .policies.ingress import IngressPolicyManager
from .policies.egress import EgressPolicyManager

# Gateway
from .gateway.filters import (
    GatewayFilterResult,
    TokenBucketRateLimiter,
    IPFilter,
    WAFInspector,
    HMACSignatureValidator,
)
from .gateway.api_gateway import APIGatewaySecurityManager

# Telemetry
from .telemetry.traffic_metrics import NetworkMetricSummary, NetworkTelemetryCollector
from .telemetry.flow_logs import (
    NetworkSecurityEventType,
    NetworkFlowRecord,
    NetworkSecurityEvent,
    NetworkFlowLogger,
)

# SDK & API
from .sdk.network_sdk import NetworkCallResult, NetworkSDK
from .api.network_routes import router as network_router, get_network_sdk

__all__ = [
    # Control Plane
    "NetworkProtocol",
    "MeshType",
    "RoutingStrategy",
    "ZeroTrustAction",
    "CertificateStatus",
    "NetworkPolicyType",
    "NetworkEndpoint",
    "RouteRule",
    "NetworkControlPlaneRegistry",
    "NetworkControlPlaneManager",
    "GlobalNetworkRouter",
    # Discovery
    "ServiceHealthState",
    "ServiceEndpoint",
    "ServiceInstance",
    "ServiceRegistration",
    "ServiceDiscoveryRegistry",
    "ResolvedServiceTarget",
    "ServiceResolver",
    "ServiceHeartbeatManager",
    # Mesh
    "IServiceMeshAdapter",
    "MeshConfigurationManifest",
    "IstioMeshAdapter",
    "LinkerdMeshAdapter",
    "ConsulMeshAdapter",
    # Traffic
    "LoadBalancerEngine",
    "RoutingDecision",
    "TrafficRouter",
    "RetryPolicy",
    "RetryEngine",
    "CircuitState",
    "CircuitBreakerConfig",
    "TrafficFailoverManager",
    # Security
    "SPIFFEIdentity",
    "WorkloadSVID",
    "WorkloadIdentityManager",
    "X509Certificate",
    "CertificateAuthorityManager",
    "MTLSValidationResult",
    "MTLSEngine",
    "ZeroTrustRule",
    "ZeroTrustEvaluationResult",
    "ZeroTrustPolicyEngine",
    # Policies
    "NetworkPolicyRule",
    "NetworkPolicy",
    "NetworkPolicyEngine",
    "IngressPolicyManager",
    "EgressPolicyManager",
    # Gateway
    "GatewayFilterResult",
    "TokenBucketRateLimiter",
    "IPFilter",
    "WAFInspector",
    "HMACSignatureValidator",
    "APIGatewaySecurityManager",
    # Telemetry
    "NetworkMetricSummary",
    "NetworkTelemetryCollector",
    "NetworkSecurityEventType",
    "NetworkFlowRecord",
    "NetworkSecurityEvent",
    "NetworkFlowLogger",
    # SDK & API
    "NetworkCallResult",
    "NetworkSDK",
    "network_router",
    "get_network_sdk",
]
