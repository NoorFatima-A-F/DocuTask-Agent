"""
Domain models for Part 3B: Enterprise Service Communication & Distributed System Verification Framework.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone


class DistributedCertificationTier(str, Enum):
    ENTERPRISE_DISTRIBUTED_SYSTEM_READY = "ENTERPRISE_DISTRIBUTED_SYSTEM_READY"
    PRODUCTION_READY = "PRODUCTION_READY"
    IMPROVEMENT_REQUIRED = "IMPROVEMENT_REQUIRED"
    FAILED = "FAILED"


DistributedCertificationTier.__test__ = False


class CircuitBreakerState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


CircuitBreakerState.__test__ = False


class CommunicationProtocol(str, Enum):
    HTTP_REST = "HTTP_REST"
    GRPC = "GRPC"
    REDIS_QUEUE = "REDIS_QUEUE"
    SQL_CONNECTION = "SQL_CONNECTION"
    S3_STORAGE = "S3_STORAGE"


class FailureMode(str, Enum):
    TIMEOUT = "TIMEOUT"
    LATENCY_SPIKE = "LATENCY_SPIKE"
    PACKET_LOSS = "PACKET_LOSS"
    CONNECTION_DROP = "CONNECTION_DROP"
    RATE_LIMITED = "RATE_LIMITED"
    INTERNAL_ERROR = "INTERNAL_ERROR"


@dataclass
class ServiceDependencyNode:
    name: str
    protocol: CommunicationProtocol
    depends_on: List[str] = field(default_factory=list)
    is_critical_path: bool = True
    timeout_seconds: float = 10.0


@dataclass
class ServiceDependencyGraph:
    nodes: Dict[str, ServiceDependencyNode] = field(default_factory=dict)
    has_cycles: bool = False
    cycle_paths: List[List[str]] = field(default_factory=list)


@dataclass
class DependencyAnalysisReport:
    total_services: int
    dependency_complexity_score: float
    critical_path_services: List[str] = field(default_factory=list)
    circular_dependencies: List[List[str]] = field(default_factory=list)
    single_points_of_failure: List[str] = field(default_factory=list)
    status: str = "PASS"


@dataclass
class CommunicationContractReport:
    total_contracts_scanned: int
    undocumented_fields: List[str] = field(default_factory=list)
    breaking_changes: List[str] = field(default_factory=list)
    schema_validation_passed: bool = True
    status: str = "PASS"


@dataclass
class ApiCommunicationReport:
    success_rate_pct: float
    average_latency_ms: float
    error_400_handled: bool = True
    error_401_handled: bool = True
    error_500_controlled_without_leak: bool = True
    status: str = "PASS"


@dataclass
class TimeoutValidationReport:
    configured_timeouts_count: int
    infinite_wait_hazards: List[str] = field(default_factory=list)
    graceful_timeout_handling_verified: bool = True
    status: str = "PASS"


@dataclass
class RetryBehaviorReport:
    exponential_backoff_verified: bool
    jitter_verified: bool
    retry_storm_prevention_verified: bool
    max_retries_configured: int = 3
    status: str = "PASS"


@dataclass
class CircuitBreakerReport:
    __test__ = False
    service_name: str
    threshold_failures: int = 5
    recovery_timeout_seconds: float = 30.0
    state_transitions_verified: bool = True
    fast_failure_on_open_verified: bool = True
    half_open_probe_verified: bool = True
    status: str = "PASS"


@dataclass
class NetworkFailureReport:
    latency_spike_resilience_verified: bool = True
    packet_loss_resilience_verified: bool = True
    connection_drop_recovery_verified: bool = True
    status: str = "PASS"
    issues: List[str] = field(default_factory=list)


@dataclass
class DatabaseCommunicationReport:
    pool_exhaustion_handled: bool = True
    automatic_reconnect_verified: bool = True
    transaction_rollback_on_disconnect: bool = True
    status: str = "PASS"


@dataclass
class StorageCommunicationReport:
    integrity_checksum_verified: bool = True
    unavailability_graceful_rejection: bool = True
    status: str = "PASS"


@dataclass
class AiProviderCommunicationReport:
    provider_name: str
    timeout_fallback_verified: bool = True
    rate_limit_backoff_verified: bool = True
    malformed_response_handled: bool = True
    status: str = "PASS"


@dataclass
class DistributedConsistencyReport:
    idempotency_keys_enforced: bool = True
    orphan_documents_prevented: bool = True
    duplicate_queue_tasks_prevented: bool = True
    compensation_actions_verified: bool = True
    status: str = "PASS"


@dataclass
class TraceabilityReport:
    request_id_propagated: bool = True
    trace_id_propagated: bool = True
    correlation_id_propagated: bool = True
    untraceable_spans: List[str] = field(default_factory=list)
    reconstructability_score: float = 100.0
    status: str = "PASS"


@dataclass
class CommunicationPerformanceReport:
    load_req_per_sec: int
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    error_rate_pct: float
    meets_sla: bool = True


@dataclass
class DistributedSystemCertificationReport:
    communication_reliability_score: float
    failure_handling_score: float
    consistency_score: float
    scalability_score: float
    observability_score: float
    security_score: float
    composite_score: float
    tier: DistributedCertificationTier
    evaluation_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ServiceCommunicationEvidencePackage:
    package_id: str
    commit_sha: str
    scorecard: DistributedSystemCertificationReport
    dependency_graph: DependencyAnalysisReport
    contract_report: CommunicationContractReport
    api_report: ApiCommunicationReport
    timeout_report: TimeoutValidationReport
    retry_report: RetryBehaviorReport
    circuit_breaker_report: CircuitBreakerReport
    network_failure_report: NetworkFailureReport
    database_report: DatabaseCommunicationReport
    storage_report: StorageCommunicationReport
    ai_provider_report: AiProviderCommunicationReport
    consistency_report: DistributedConsistencyReport
    traceability_report: TraceabilityReport
    performance_report: CommunicationPerformanceReport
    package_sha256: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
