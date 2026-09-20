"""
Domain Models for Enterprise Dependency-Aware Readiness Decision Engine (Part 3H.3.2).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional


class ReadinessState(str, Enum):
    STARTING = "STARTING"
    READY = "READY"
    DEGRADED = "DEGRADED"
    NOT_READY = "NOT_READY"
    RECOVERING = "RECOVERING"
    UNKNOWN = "UNKNOWN"


class DependencyCriticality(str, Enum):
    CRITICAL = "critical"
    IMPORTANT = "important"
    OPTIONAL = "optional"


class TrafficAction(str, Enum):
    ALLOW_TRAFFIC = "ALLOW_TRAFFIC"
    THROTTLE_TRAFFIC = "THROTTLE_TRAFFIC"
    REJECT_TRAFFIC = "REJECT_TRAFFIC"


class WorkerState(str, Enum):
    AVAILABLE = "AVAILABLE"
    BUSY = "BUSY"
    OVERLOADED = "OVERLOADED"
    FAILED = "FAILED"


class ReadinessTier(str, Enum):
    FAILED = "Failed"                                         # < 80
    NEEDS_IMPROVEMENT = "Improvement Required"               # 80 - 89
    PRODUCTION_READY = "Production Ready"                     # 90 - 94
    ENTERPRISE_READY = "Enterprise Readiness Certified"       # 95 - 100


@dataclass
class DatabaseReadinessReport:
    database: str
    status: str
    connected: bool
    authenticated: bool
    transaction_supported: bool
    schema_compatible: bool
    current_schema_version: str
    required_schema_version: str
    latency_ms: float
    connections_active: int
    connections_idle: int
    connections_waiting: int
    connections_available: int
    pool_exhausted: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QueueReadinessReport:
    broker: str
    status: str
    ping_pong_ok: bool
    enqueue_accessible: bool
    queue_state_readable: bool
    queue_depth: int
    oldest_message_age_seconds: float
    processing_delay_ms: float
    latency_ms: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StorageReadinessReport:
    storage_type: str
    status: str
    reachable: bool
    write_permission: bool
    read_permission: bool
    integrity_verified: bool
    cleanup_verified: bool
    latency_ms: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIProviderReadinessReport:
    provider: str
    status: str
    authenticated: bool
    latency_ms: float
    quota_remaining_pct: float
    response_valid: bool
    fallback_mode_active: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkerReadinessReport:
    worker_id: str
    status: str
    registered: bool
    heartbeat_age_seconds: float
    active_jobs: int
    capacity: int
    can_process_tasks: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DependencyMatrixItem:
    name: str
    criticality: DependencyCriticality
    failure_action: str
    traffic_action: TrafficAction
    current_health: str
    latency_ms: float
    healthy: bool


@dataclass
class DependencyMatrixReport:
    total_dependencies: int
    dependencies: List[DependencyMatrixItem]
    critical_dependencies_count: int
    important_dependencies_count: int
    optional_dependencies_count: int
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReadinessEvaluationResult:
    service: str
    state: ReadinessState
    traffic_action: TrafficAction
    traffic_allowed: bool
    reason: str
    failed_dependencies: List[str]
    degraded_dependencies: List[str]
    healthy_dependencies: List[str]
    checks: Dict[str, Any]
    evaluation_duration_ms: float
    timestamp: str


@dataclass
class FailureScenarioResult:
    scenario_id: str
    scenario_name: str
    injected_failure: str
    expected_state: ReadinessState
    actual_state: ReadinessState
    expected_traffic_action: TrafficAction
    actual_traffic_action: TrafficAction
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FailureSimulationReport:
    total_scenarios: int
    passed_scenarios: int
    all_scenarios_passed: bool
    scenarios: List[FailureScenarioResult]
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KubernetesCompatibilityReport:
    readiness_probe_path: str
    initial_delay_seconds: int
    period_seconds: int
    timeout_seconds: int
    success_threshold: int
    failure_threshold: int
    deterministic_response: bool
    fast_response: bool
    latency_ms: float
    no_side_effects: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReadinessSecurityReport:
    no_database_host_leak: bool
    no_password_or_token_leak: bool
    no_connection_string_leak: bool
    no_stack_trace_leak: bool
    no_internal_ip_leak: bool
    total_leaks_detected: int
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReadinessScorecard:
    dependency_detection_score: float   # Weight 25%
    failure_accuracy_score: float       # Weight 20%
    policy_correctness_score: float     # Weight 20%
    kubernetes_compatibility_score: float # Weight 15%
    security_score: float               # Weight 10%
    observability_score: float          # Weight 10%
    overall_readiness_score: float      # Composite 0 - 100
    certification_tier: ReadinessTier
    certification_verdict: str          # CERTIFIED / REJECTED
    traffic_admission_safe: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)
