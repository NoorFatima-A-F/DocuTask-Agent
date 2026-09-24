"""
Domain Models for Enterprise Liveness Verification Framework (Part 3H.2).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List


class LivenessState(str, Enum):
    STARTING = "STARTING"
    ALIVE = "ALIVE"
    DEGRADED = "DEGRADED"
    STUCK = "STUCK"
    FAILED = "FAILED"


class LivenessTier(str, Enum):
    FAILED = "Failed"                                      # < 80
    NEEDS_IMPROVEMENT = "Needs Improvement"                # 80 - 89
    PRODUCTION_READY = "Production Ready"                  # 90 - 94
    ENTERPRISE_READY = "Enterprise Liveness Ready"         # 95 - 100


class ProcessStatus(str, Enum):
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    ZOMBIE = "ZOMBIE"
    TERMINATED = "TERMINATED"


class FailureType(str, Enum):
    PROCESS_CRASH = "PROCESS_CRASH"
    APPLICATION_FREEZE = "APPLICATION_FREEZE"
    MEMORY_EXHAUSTION = "MEMORY_EXHAUSTION"
    HEARTBEAT_LOSS = "HEARTBEAT_LOSS"
    DEADLOCK = "DEADLOCK"


@dataclass
class RuntimeIdentity:
    service_name: str
    version: str
    instance_id: str
    process_id: int
    startup_time: str
    uptime_seconds: float
    status: LivenessState = LivenessState.ALIVE


@dataclass
class LivenessContractReport:
    endpoint: str
    contract_sample: Dict[str, Any]
    isolated_from_dependencies: bool
    zero_db_checks_verified: bool
    zero_redis_checks_verified: bool
    zero_external_api_checks_verified: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResponsivenessReport:
    endpoint_tested: str
    average_latency_ms: float
    max_latency_ms: float
    latency_threshold_ms: float
    timeouts_count: int
    responsive: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProcessStateReport:
    total_processes_checked: int
    running_processes_count: int
    blocked_count: int
    zombies_count: int
    terminated_count: int
    all_processes_alive: bool
    passed: bool
    processes: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class EventLoopHealthReport:
    average_latency_ms: float
    maximum_latency_ms: float
    heartbeat_interval_seconds: float
    failure_threshold_ms: float
    pending_tasks_count: int
    loop_healthy: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DeadlockReport:
    deadlock_detected: bool
    watchdog_active: bool
    frozen_threads_count: int
    blocked_locks_count: int
    restart_signal_generated: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkerLivenessReport:
    total_workers_tracked: int
    active_workers_count: int
    zombie_workers_count: int
    stuck_workers_count: int
    all_workers_healthy: bool
    passed: bool
    workers: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SchedulerLivenessReport:
    scheduler_running: bool
    last_tick_timestamp: str
    seconds_since_last_tick: float
    missed_jobs_count: int
    next_execution_time: str
    scheduler_healthy: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResourceHealthReport:
    memory_rss_mb: float
    memory_heap_mb: float
    memory_growth_rate_pct: float
    memory_state: str  # NORMAL, WARNING, CRITICAL, UNHEALTHY
    cpu_usage_pct: float
    cpu_throttled: bool
    load_average: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FailureSimulationReport:
    total_simulations: int
    passed_simulations: int
    process_kill_handled: bool
    event_loop_freeze_handled: bool
    memory_exhaustion_handled: bool
    worker_deadlock_handled: bool
    passed: bool
    simulations: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class RecoveryReport:
    failure_detection_time_seconds: float
    restart_time_seconds: float
    initialization_time_seconds: float
    mttr_seconds: float
    orchestrator_restart_verified: bool
    cloud_runtimes_compatible: List[str]  # Docker Compose, Kubernetes, Cloud Run, ECS
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SecurityReport:
    public_endpoint_leak_free: bool
    sensitive_data_filtered: bool
    auth_policy_enforced: bool
    rate_limiting_active: bool
    credentials_leaked_count: int
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LivenessScorecard:
    runtime_detection_accuracy_score: float  # Weight 25%
    event_loop_monitoring_score: float       # Weight 20%
    deadlock_detection_score: float          # Weight 15%
    resource_monitoring_score: float         # Weight 15%
    recovery_integration_score: float        # Weight 15%
    security_score: float                    # Weight 10%
    overall_liveness_score: float            # Composite 0 - 100
    certification_tier: LivenessTier
    certification_verdict: str               # CERTIFIED / REJECTED
    auto_recovery_validated: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)
