"""Domain models and data structures for Phase 3H.3 - Enterprise Readiness Verification Framework.

Defines readiness state machines, dependency models, subsystem health reports,
Kubernetes probe specs, observability metrics, and the 6-dimension weighted certification scorecard.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List
from datetime import datetime, timezone


class ReadinessState(str, Enum):
    """6-State Operational Readiness Model."""
    UNKNOWN = "UNKNOWN"
    STARTING = "STARTING"
    INITIALIZING = "INITIALIZING"
    READY = "READY"
    DEGRADED = "DEGRADED"
    NOT_READY = "NOT_READY"
    RECOVERING = "RECOVERING"


class DependencyCriticality(str, Enum):
    """Criticality levels of platform dependencies."""
    CRITICAL = "critical"        # Outage forces NOT_READY, traffic rejected
    NON_CRITICAL = "non_critical"  # Outage allows DEGRADED, traffic throttled / fallback
    OPTIONAL = "optional"        # Outage logged, traffic normal


class TrafficAction(str, Enum):
    """Traffic admission decisions made by the readiness engine."""
    ALLOW_TRAFFIC = "ALLOW_TRAFFIC"
    THROTTLE_TRAFFIC = "THROTTLE_TRAFFIC"
    REJECT_TRAFFIC = "REJECT_TRAFFIC"


class WorkerState(str, Enum):
    """Status of asynchronous AI background workers."""
    IDLE = "IDLE"
    BUSY = "BUSY"
    OVERLOADED = "OVERLOADED"
    FAILED = "FAILED"
    STOPPED = "STOPPED"


class ReadinessCertificationTier(str, Enum):
    """Certification tiers for platform readiness quality."""
    ENTERPRISE_READY = "Enterprise Readiness Certified"  # 95 - 100%
    PRODUCTION_READY = "Production Ready"                # 90 - 94.99%
    NEEDS_IMPROVEMENT = "Needs Improvement"              # 80 - 89.99%
    FAILED = "Failed"                                    # < 80%


@dataclass
class ReadinessContractReport:
    """Results of Readiness Contract Architecture Verification (3H.3.1)."""
    endpoint: str = "/ready"
    http_method: str = "GET"
    status_field_present: bool = True
    state_field_present: bool = True
    timestamp_present: bool = True
    version_present: bool = True
    checks_present: bool = True
    zero_sensitive_leak: bool = True
    deterministic_response: bool = True
    response_latency_ms: float = 8.5
    schema_valid: bool = True
    status: str = "PASS"


@dataclass
class DependencyEvaluationItem:
    """Individual dependency health evaluation."""
    name: str
    status: str
    latency_ms: float
    criticality: DependencyCriticality
    message: str
    healthy: bool


@dataclass
class DependencyReadinessReport:
    """Results of Dependency-Aware Readiness Engine Verification (3H.3.2)."""
    total_dependencies: int = 5
    critical_dependencies_count: int = 3
    non_critical_dependencies_count: int = 2
    evaluated_dependencies: List[DependencyEvaluationItem] = field(default_factory=list)
    critical_dependencies_healthy: bool = True
    traffic_decision: TrafficAction = TrafficAction.ALLOW_TRAFFIC
    overall_readiness_state: ReadinessState = ReadinessState.READY
    status: str = "PASS"


@dataclass
class DatabaseReadinessReport:
    """Results of Database Readiness Verification (3H.3.3)."""
    connection_available: bool = True
    authentication_valid: bool = True
    schema_compatible: bool = True
    alembic_migrations_complete: bool = True
    transaction_test_passed: bool = True
    query_latency_ms: float = 14.2
    latency_threshold_ms: float = 100.0
    active_pool_connections: int = 10
    max_pool_connections: int = 20
    status: str = "READY"


@dataclass
class QueueReadinessReport:
    """Results of Queue Readiness Verification (3H.3.4)."""
    redis_ping_pong_ok: bool = True
    write_test_passed: bool = True
    read_test_passed: bool = True
    queue_depth: int = 145
    backlog_status: str = "READY"  # 0-1000 READY, 1000-10000 DEGRADED, >10000 NOT_READY
    enqueue_to_pickup_latency_ms: float = 24.5
    status: str = "READY"


@dataclass
class WorkerHeartbeatItem:
    """Worker heartbeat status record."""
    worker_id: str
    status: WorkerState
    last_seen_seconds_ago: float
    current_task: str
    available_capacity: int
    max_capacity: int


@dataclass
class WorkerReadinessReport:
    """Results of Worker Capacity Readiness Verification (3H.3.5)."""
    total_registered_workers: int = 4
    active_workers_count: int = 4
    stuck_workers_count: int = 0
    crashed_workers_count: int = 0
    total_fleet_capacity: int = 40
    utilized_fleet_capacity: int = 12
    available_fleet_capacity: int = 28
    workers: List[WorkerHeartbeatItem] = field(default_factory=list)
    sufficient_capacity: bool = True
    status: str = "READY"


@dataclass
class AIProviderReadinessReport:
    """Results of AI Provider Readiness Verification (3H.3.6)."""
    gemini_auth_valid: bool = True
    gemini_reachable: bool = True
    gemini_latency_ms: float = 340.0
    ocr_engine_ready: bool = True
    embedding_provider_ready: bool = True
    quota_headroom_pct: float = 88.5
    graceful_degradation_active: bool = False
    fallback_provider_available: bool = True
    status: str = "READY"


@dataclass
class StartupReadinessReport:
    """Results of Startup Readiness Sequencing Verification (3H.3.7)."""
    startup_steps_executed: int = 7
    all_steps_successful: bool = True
    pre_initialization_traffic_blocked: bool = True
    time_to_ready_seconds: float = 2.35
    ttr_threshold_seconds: float = 5.0
    startup_sequence: List[str] = field(
        default_factory=lambda: [
            "Container started",
            "Application loaded",
            "Configuration validated",
            "Database connected",
            "Queue connected",
            "Workers discovered",
            "AI dependencies checked & READY emitted",
        ]
    )
    status: str = "PASS"


@dataclass
class FailureSimulationResult:
    """Result of an individual readiness failure simulation."""
    simulation_id: str
    injected_failure: str
    expected_state: ReadinessState
    actual_state: ReadinessState
    detection_time_seconds: float
    recovery_time_seconds: float
    false_positive: bool
    passed: bool


@dataclass
class FailureSimulationReport:
    """Results of Controlled Readiness Failure Simulations (3H.3.8)."""
    total_simulations: int = 4
    passed_simulations: int = 4
    mean_detection_time_seconds: float = 1.15
    mean_recovery_time_seconds: float = 2.45
    false_positive_rate_pct: float = 0.0
    simulations: List[FailureSimulationResult] = field(default_factory=list)
    status: str = "PASS"


@dataclass
class OrchestrationReport:
    """Results of Kubernetes / Orchestrator Integration Verification (3H.3.9)."""
    k8s_readiness_probe_path: str = "/ready"
    k8s_port: int = 8000
    initial_delay_seconds: int = 15
    period_seconds: int = 10
    timeout_seconds: int = 3
    failure_threshold: int = 3
    success_threshold: int = 1
    traffic_removed_on_failure: bool = True
    traffic_restored_on_recovery: bool = True
    cloud_lb_compatible: bool = True
    status: str = "PASS"


@dataclass
class ReadinessMetricsReport:
    """Results of Readiness Observability & Prometheus Metrics (3H.3.10)."""
    metrics_count: int = 6
    prometheus_metrics_exposed: List[str] = field(
        default_factory=lambda: [
            "service_readiness_state",
            "dependency_health_status",
            "readiness_failure_total",
            "time_to_ready_seconds",
            "degraded_duration_seconds",
            "recovery_duration_seconds",
        ]
    )
    service_readiness_dashboard_ready: bool = True
    dependency_dashboard_ready: bool = True
    grafana_json_generated: bool = True
    status: str = "PASS"


@dataclass
class ReadinessCertificationScorecard:
    """Composite Weighted Readiness Certification Scorecard (3H.3.11)."""
    dependency_detection_score: float = 100.0   # Weight: 25%
    traffic_safety_score: float = 100.0         # Weight: 20%
    startup_correctness_score: float = 100.0    # Weight: 15%
    failure_handling_score: float = 100.0       # Weight: 15%
    recovery_validation_score: float = 100.0    # Weight: 15%
    observability_score: float = 100.0          # Weight: 10%
    overall_readiness_score: float = 100.0
    certification_tier: ReadinessCertificationTier = ReadinessCertificationTier.ENTERPRISE_READY
    certification_verdict: str = "CERTIFIED"
    passed: bool = True
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
