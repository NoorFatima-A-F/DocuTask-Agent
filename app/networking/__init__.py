"""Enterprise Service Mesh, Networking & Zero-Trust Communication Platform."""

# Mesh Control & Data Plane
from .mesh.control_plane import (
    MeshState,
    ProtocolType,
    MeshNode,
    MeshServiceSpec,
    MeshConfigVersion,
    MeshTopology,
    ServiceMeshController,
)
from .mesh.data_plane import (
    TrafficDirection,
    MeshRequest,
    MeshResponse,
    DataPlaneInterceptor,
)
from .mesh.proxy import (
    ProxyStats,
    ServiceProxy,
)

# Identity & Certificates
from .identity.service_identity import (
    SPIFFEIdentity,
    WorkloadIdentity,
    ServiceIdentityManager,
)
from .identity.certificates import (
    CertificateBackend,
    X509Certificate,
    CertificateManager,
)
from .identity.workload import (
    SVIDType,
    WorkloadSVID,
    AttestationEvidence,
    WorkloadAttestationManager,
)

# Security & Policies
from .security.mtls import (
    MTLSMode,
    TLSVersion,
    MTLSSession,
    MTLSHandshakeResult,
    MTLSManager,
    CIPHER_SUITES_TLS_1_3,
)
from .security.policies import (
    PolicyAction,
    NetworkPolicyRule,
    NetworkPolicy,
    NetworkPolicyEngine,
)
from .security.authorization import (
    ZeroTrustSubject,
    ZeroTrustResource,
    ZeroTrustDecision,
    ZeroTrustEvaluator,
)

# Discovery & Resolution
from .discovery.registry import (
    EndpointHealth,
    ServiceEndpoint,
    ServiceRegistry,
)
from .discovery.resolver import (
    ResolvedTarget,
    ServiceResolver,
)

# Routing & Traffic Management
from .routing.router import (
    MatchCondition,
    RouteDestination,
    RouteRule,
    TrafficRouter,
)
from .routing.policies import (
    LoadBalancingAlgorithm,
    ConnectionPoolSettings,
    OutlierDetectionSettings,
    TrafficPolicy,
    RoutingPolicyEngine,
)
from .routing.traffic_split import (
    SplitType,
    VersionSplit,
    TrafficSplitConfig,
    TrafficSplitter,
)

# Resilience & Fault Injection
from .resilience.retry import (
    BackoffStrategy,
    RetryPolicy,
    RetryPolicyEngine,
)
from .resilience.circuit_breaker import (
    CircuitState,
    CircuitBreakerConfig,
    CircuitBreaker,
)
from .resilience.timeout import (
    DeadlineContext,
    TimeoutManager,
)
from .resilience.fault_injection import (
    FaultType,
    FaultInjectionRule,
    FaultInjectionEngine,
)

# Load Balancing & Health
from .load_balancing.algorithms import (
    LoadBalancerEngine,
)
from .load_balancing.health import (
    HealthCheckConfig,
    OutlierDetectionTracker,
    HealthCheckEngine,
)

# Telemetry & Observability
from .telemetry.metrics import (
    MeshMetricsSummary,
    MeshMetricsCollector,
)
from .telemetry.traces import (
    SpanKind,
    MeshSpan,
    TraceContextPropagator,
)
from .telemetry.logs import (
    MeshAccessLogRecord,
    MeshAccessLogger,
)

# SDK & Decorators
from .sdk.client import (
    MeshClient,
)
from .sdk.decorators import (
    mesh_service,
    mesh_endpoint,
    circuit_protected,
    with_retry,
)

# API
from .api.routes import (
    network_mesh_router,
    get_mesh_client,
)

__all__ = [
    # Mesh
    "MeshState",
    "ProtocolType",
    "MeshNode",
    "MeshServiceSpec",
    "MeshConfigVersion",
    "MeshTopology",
    "ServiceMeshController",
    "TrafficDirection",
    "MeshRequest",
    "MeshResponse",
    "DataPlaneInterceptor",
    "ProxyStats",
    "ServiceProxy",
    # Identity
    "SPIFFEIdentity",
    "WorkloadIdentity",
    "ServiceIdentityManager",
    "CertificateBackend",
    "X509Certificate",
    "CertificateManager",
    "SVIDType",
    "WorkloadSVID",
    "AttestationEvidence",
    "WorkloadAttestationManager",
    # Security
    "MTLSMode",
    "TLSVersion",
    "MTLSSession",
    "MTLSHandshakeResult",
    "MTLSManager",
    "CIPHER_SUITES_TLS_1_3",
    "PolicyAction",
    "NetworkPolicyRule",
    "NetworkPolicy",
    "NetworkPolicyEngine",
    "ZeroTrustSubject",
    "ZeroTrustResource",
    "ZeroTrustDecision",
    "ZeroTrustEvaluator",
    # Discovery
    "EndpointHealth",
    "ServiceEndpoint",
    "ServiceRegistry",
    "ResolvedTarget",
    "ServiceResolver",
    # Routing
    "MatchCondition",
    "RouteDestination",
    "RouteRule",
    "TrafficRouter",
    "LoadBalancingAlgorithm",
    "ConnectionPoolSettings",
    "OutlierDetectionSettings",
    "TrafficPolicy",
    "RoutingPolicyEngine",
    "SplitType",
    "VersionSplit",
    "TrafficSplitConfig",
    "TrafficSplitter",
    # Resilience
    "BackoffStrategy",
    "RetryPolicy",
    "RetryPolicyEngine",
    "CircuitState",
    "CircuitBreakerConfig",
    "CircuitBreaker",
    "DeadlineContext",
    "TimeoutManager",
    "FaultType",
    "FaultInjectionRule",
    "FaultInjectionEngine",
    # Load Balancing
    "LoadBalancerEngine",
    "HealthCheckConfig",
    "OutlierDetectionTracker",
    "HealthCheckEngine",
    # Telemetry
    "MeshMetricsSummary",
    "MeshMetricsCollector",
    "SpanKind",
    "MeshSpan",
    "TraceContextPropagator",
    "MeshAccessLogRecord",
    "MeshAccessLogger",
    # SDK
    "MeshClient",
    "mesh_service",
    "mesh_endpoint",
    "circuit_protected",
    "with_retry",
    # API
    "network_mesh_router",
    "get_mesh_client",
]
