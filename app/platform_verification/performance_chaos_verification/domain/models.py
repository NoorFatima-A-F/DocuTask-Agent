"""
Domain models for Enterprise Performance, Scaling & Chaos Verification (Part 3F).
"""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class BottleneckCategory(str, Enum):
    COMPUTE = "COMPUTE"
    MEMORY = "MEMORY"
    DATABASE = "DATABASE"
    NETWORK = "NETWORK"
    AI_PROVIDER = "AI_PROVIDER"
    STORAGE = "STORAGE"
    QUEUE = "QUEUE"
    NONE = "NONE"


class ChaosExperimentType(str, Enum):
    CONTAINER_KILL = "CONTAINER_KILL"
    DATABASE_OUTAGE = "DATABASE_OUTAGE"
    QUEUE_PARTITION = "QUEUE_PARTITION"
    NETWORK_LATENCY_LOSS = "NETWORK_LATENCY_LOSS"
    RESOURCE_EXHAUSTION = "RESOURCE_EXHAUSTION"


class PerformanceCertificationTier(str, Enum):
    ENTERPRISE_PERFORMANCE_READY = "ENTERPRISE_PERFORMANCE_READY"
    PRODUCTION_READY = "PRODUCTION_READY"
    OPTIMIZATION_REQUIRED = "OPTIMIZATION_REQUIRED"
    FAILED = "FAILED"


@dataclass
class WorkloadProfile:
    concurrent_users: int
    documents_per_hour: int
    target_rps: float
    workload_type: str  # "NORMAL", "DEPARTMENT", "ENTERPRISE"


@dataclass
class PipelineStageTiming:
    upload_ms: float
    ocr_ms: float
    extraction_ms: float
    validation_ms: float
    storage_ms: float
    total_pipeline_ms: float


@dataclass
class PerformanceBaselineReport:
    requests_per_second: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    error_rate: float
    pipeline_stage_timing: PipelineStageTiming
    db_query_latency_ms: float
    queue_enqueue_latency_ms: float
    status: str = "BASELINE"


@dataclass
class LoadTestReport:
    __test__ = False
    scenario_name: str
    concurrent_users: int
    throughput_rps: float
    p95_latency_ms: float
    error_rate: float
    total_documents_processed: int
    passed: bool


@dataclass
class StressTestReport:
    __test__ = False
    step_levels: List[int]
    max_sustainable_throughput_rps: float
    breaking_point_users: int
    saturation_resource: str
    passed: bool


@dataclass
class SpikeTestReport:
    __test__ = False
    baseline_rps: float
    spike_rps: float
    queue_depth_max: int
    recovery_time_seconds: float
    data_loss_count: int
    passed: bool


@dataclass
class EnduranceTestReport:
    __test__ = False
    duration_hours: float
    initial_memory_mb: float
    final_memory_mb: float
    memory_leak_detected: bool
    connection_leaks_detected: int
    performance_drift_percent: float
    passed: bool


@dataclass
class ResourceAnalysisReport:
    cpu_utilization_avg_percent: float
    cpu_throttling_detected: bool
    memory_allocation_mb: float
    db_connection_pool_utilization_percent: float
    queue_backlog_count: int
    ai_token_consumption_rate_tps: float


@dataclass
class BottleneckAnalysisReport:
    primary_bottleneck: BottleneckCategory
    limiting_component: str
    diagnostic_rationale: str
    recommended_action: str


@dataclass
class HorizontalScalingReport:
    api_instance_scaling: Dict[int, float]  # instances -> throughput_rps
    worker_instance_scaling: Dict[int, float]  # workers -> docs_per_hour
    api_linearity_efficiency: float
    worker_linearity_efficiency: float
    near_linear_scaling: bool


@dataclass
class DatabasePerformanceReport:
    read_query_latency_p95_ms: float
    write_transaction_latency_p95_ms: float
    deadlocks_encountered: int
    slow_queries_count: int
    index_efficiency_score: float


@dataclass
class AiPerformanceReport:
    ocr_pages_per_sec: float
    ocr_accuracy_under_load_percent: float
    llm_tokens_per_sec: float
    llm_ttft_ms: float
    agent_planning_latency_ms: float
    agent_tool_execution_ms: float


@dataclass
class ChaosExperimentResult:
    experiment_type: ChaosExperimentType
    target_service: str
    detection_time_sec: float
    recovery_time_sec: float
    data_loss_detected: bool
    transaction_corruption_detected: bool
    passed: bool


@dataclass
class PerformanceSloTarget:
    metric_name: str
    target_value: float
    actual_value: float
    unit: str
    compliant: bool


@dataclass
class PerformanceSloReport:
    targets: List[PerformanceSloTarget]
    overall_compliance_percent: float
    status: str


@dataclass
class PerformanceCertificationScorecard:
    latency_score: float
    throughput_score: float
    scalability_score: float
    resource_efficiency_score: float
    chaos_resilience_score: float
    recovery_performance_score: float
    composite_score: float
    certification_tier: PerformanceCertificationTier
    passed: bool


@dataclass
class PerformanceMetadata:
    repository: str
    commit: str
    environment: str
    hardware_profile: str
    timestamp: str
    verification_engine_version: str = "1.0.0"
