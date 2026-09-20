"""
Domain models and schemas for Phase V10 Enterprise Performance, Scalability & Reliability Verification Program (EPSRV).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any


class PerformanceStatus(str, Enum):
    OPTIMAL = "OPTIMAL"
    ACCEPTABLE = "ACCEPTABLE"
    DEGRADED = "DEGRADED"
    CRITICAL = "CRITICAL"
    FAILED = "FAILED"


class WorkloadType(str, Enum):
    INVOICE_PROCESSING = "INVOICE_PROCESSING"
    CONTRACT_ANALYSIS = "CONTRACT_ANALYSIS"
    MULTI_AGENT_WORKFLOW = "MULTI_AGENT_WORKFLOW"
    SPIKE_BURST = "SPIKE_BURST"
    SOAK_ENDURANCE = "SOAK_ENDURANCE"


class ChaosFailureType(str, Enum):
    DATABASE_UNAVAILABLE = "DATABASE_UNAVAILABLE"
    REDIS_UNAVAILABLE = "REDIS_UNAVAILABLE"
    LLM_API_TIMEOUT = "LLM_API_TIMEOUT"
    WORKER_CRASH = "WORKER_CRASH"
    NETWORK_INTERRUPTION = "NETWORK_INTERRUPTION"


@dataclass
class LatencyDistribution:
    """Percentile latency distribution in milliseconds."""
    p50_ms: float
    p90_ms: float
    p95_ms: float
    p99_ms: float
    max_ms: float
    mean_ms: float
    std_dev_ms: float
    sample_count: int
    sla_target_p95_ms: float
    sla_met: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "p50_ms": round(self.p50_ms, 2),
            "p90_ms": round(self.p90_ms, 2),
            "p95_ms": round(self.p95_ms, 2),
            "p99_ms": round(self.p99_ms, 2),
            "max_ms": round(self.max_ms, 2),
            "mean_ms": round(self.mean_ms, 2),
            "std_dev_ms": round(self.std_dev_ms, 2),
            "sample_count": self.sample_count,
            "sla_target_p95_ms": round(self.sla_target_p95_ms, 2),
            "sla_met": self.sla_met,
        }


@dataclass
class StageLatency:
    """Latency contribution of a single pipeline stage."""
    stage_name: str
    latency_ms: float
    percentage_of_total: float
    sla_target_ms: float
    sla_met: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stage_name": self.stage_name,
            "latency_ms": round(self.latency_ms, 2),
            "percentage_of_total": round(self.percentage_of_total, 1),
            "sla_target_ms": round(self.sla_target_ms, 2),
            "sla_met": self.sla_met,
        }


@dataclass
class PipelineLatencyBreakdown:
    """Granular breakdown of document intelligence pipeline latency."""
    pipeline_name: str
    total_latency_ms: float
    stages: List[StageLatency]
    sla_target_total_ms: float
    sla_met: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pipeline_name": self.pipeline_name,
            "total_latency_ms": round(self.total_latency_ms, 2),
            "stages": [s.to_dict() for s in self.stages],
            "sla_target_total_ms": round(self.sla_target_total_ms, 2),
            "sla_met": self.sla_met,
        }


@dataclass
class ThroughputResult:
    """Throughput capacity benchmark result."""
    workload_name: str
    target_volume_per_hr: int
    achieved_volume_per_hr: float
    concurrency_level: int
    completed_jobs: int
    failed_jobs: int
    average_latency_ms: float
    queue_depth_peak: int
    completion_rate_pct: float
    status: PerformanceStatus

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workload_name": self.workload_name,
            "target_volume_per_hr": self.target_volume_per_hr,
            "achieved_volume_per_hr": round(self.achieved_volume_per_hr, 1),
            "concurrency_level": self.concurrency_level,
            "completed_jobs": self.completed_jobs,
            "failed_jobs": self.failed_jobs,
            "average_latency_ms": round(self.average_latency_ms, 2),
            "queue_depth_peak": self.queue_depth_peak,
            "completion_rate_pct": round(self.completion_rate_pct, 2),
            "status": self.status.value,
        }


@dataclass
class LoadTestResult:
    """Load test scenario outcome."""
    scenario_name: str
    concurrent_users: int
    duration_simulated_hrs: float
    total_requests: int
    successful_requests: int
    failed_requests: int
    error_rate_pct: float
    latency_dist: LatencyDistribution
    status: PerformanceStatus

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_name": self.scenario_name,
            "concurrent_users": self.concurrent_users,
            "duration_simulated_hrs": self.duration_simulated_hrs,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "error_rate_pct": round(self.error_rate_pct, 4),
            "latency": self.latency_dist.to_dict(),
            "status": self.status.value,
        }


@dataclass
class CapacityBoundary:
    """Stress test capacity threshold."""
    user_level: int
    document_volume: int
    p95_latency_ms: float
    error_rate_pct: float
    cpu_utilization_pct: float
    memory_mb: float
    classification: str  # STABLE, WARNING, CRITICAL

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_level": self.user_level,
            "document_volume": self.document_volume,
            "p95_latency_ms": round(self.p95_latency_ms, 2),
            "error_rate_pct": round(self.error_rate_pct, 2),
            "cpu_utilization_pct": round(self.cpu_utilization_pct, 1),
            "memory_mb": round(self.memory_mb, 1),
            "classification": self.classification,
        }


@dataclass
class SpikeTestResult:
    """Spike test burst resilience result."""
    baseline_rate_per_min: int
    spike_rate_per_min: int
    surge_multiplier: float
    burst_duration_sec: int
    dropped_jobs: int
    queue_backpressure_engaged: bool
    graceful_degradation: bool
    recovery_time_sec: float
    status: PerformanceStatus

    def to_dict(self) -> Dict[str, Any]:
        return {
            "baseline_rate_per_min": self.baseline_rate_per_min,
            "spike_rate_per_min": self.spike_rate_per_min,
            "surge_multiplier": round(self.surge_multiplier, 1),
            "burst_duration_sec": self.burst_duration_sec,
            "dropped_jobs": self.dropped_jobs,
            "queue_backpressure_engaged": self.queue_backpressure_engaged,
            "graceful_degradation": self.graceful_degradation,
            "recovery_time_sec": round(self.recovery_time_sec, 2),
            "status": self.status.value,
        }


@dataclass
class EnduranceTestResult:
    """Long-term soak test stability result."""
    duration_simulated_hrs: int
    initial_p95_ms: float
    final_p95_ms: float
    latency_drift_pct: float
    initial_memory_mb: float
    final_memory_mb: float
    memory_growth_gradient_mb_hr: float
    memory_leak_detected: bool
    queue_accumulation: int
    stability_rating: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "duration_simulated_hrs": self.duration_simulated_hrs,
            "initial_p95_ms": round(self.initial_p95_ms, 2),
            "final_p95_ms": round(self.final_p95_ms, 2),
            "latency_drift_pct": round(self.latency_drift_pct, 2),
            "initial_memory_mb": round(self.initial_memory_mb, 1),
            "final_memory_mb": round(self.final_memory_mb, 1),
            "memory_growth_gradient_mb_hr": round(self.memory_growth_gradient_mb_hr, 4),
            "memory_leak_detected": self.memory_leak_detected,
            "queue_accumulation": self.queue_accumulation,
            "stability_rating": self.stability_rating,
        }


@dataclass
class ResourceEfficiencyProfile:
    """Resource consumption and efficiency analysis."""
    cpu_average_pct: float
    cpu_peak_pct: float
    cpu_returns_to_baseline: bool
    memory_allocated_mb: float
    memory_reclaimed_pct: float
    db_connection_pool_active: int
    db_connection_pool_max: int
    db_connection_exhaustion: bool
    storage_growth_mb_per_1k_docs: float
    estimated_storage_cost_monthly: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cpu_average_pct": round(self.cpu_average_pct, 1),
            "cpu_peak_pct": round(self.cpu_peak_pct, 1),
            "cpu_returns_to_baseline": self.cpu_returns_to_baseline,
            "memory_allocated_mb": round(self.memory_allocated_mb, 1),
            "memory_reclaimed_pct": round(self.memory_reclaimed_pct, 1),
            "db_connection_pool_active": self.db_connection_pool_active,
            "db_connection_pool_max": self.db_connection_pool_max,
            "db_connection_exhaustion": self.db_connection_exhaustion,
            "storage_growth_mb_per_1k_docs": round(self.storage_growth_mb_per_1k_docs, 2),
            "estimated_storage_cost_monthly": round(self.estimated_storage_cost_monthly, 4),
        }


@dataclass
class AICostProfile:
    """AI cost performance and ROI evaluation."""
    workflow_name: str
    ocr_cost_per_doc: float
    llm_cost_per_doc: float
    storage_cost_per_doc: float
    total_ai_cost_per_doc: float
    manual_baseline_cost_per_doc: float
    cost_reduction_pct: float
    prompt_tokens_avg: int
    completion_tokens_avg: int
    annual_savings_100k_docs: float
    roi_multiple: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_name": self.workflow_name,
            "ocr_cost_per_doc": round(self.ocr_cost_per_doc, 4),
            "llm_cost_per_doc": round(self.llm_cost_per_doc, 4),
            "storage_cost_per_doc": round(self.storage_cost_per_doc, 4),
            "total_ai_cost_per_doc": round(self.total_ai_cost_per_doc, 4),
            "manual_baseline_cost_per_doc": round(self.manual_baseline_cost_per_doc, 2),
            "cost_reduction_pct": round(self.cost_reduction_pct, 2),
            "prompt_tokens_avg": self.prompt_tokens_avg,
            "completion_tokens_avg": self.completion_tokens_avg,
            "annual_savings_100k_docs": round(self.annual_savings_100k_docs, 2),
            "roi_multiple": round(self.roi_multiple, 1),
        }


@dataclass
class ChaosRecoveryResult:
    """Chaos engineering injection and self-healing result."""
    failure_type: ChaosFailureType
    description: str
    injected: bool
    graceful_fallback: bool
    retry_mechanism_triggered: bool
    auto_recovered: bool
    recovery_time_ms: float
    data_corrupted: bool
    circuit_breaker_opened: bool
    status: PerformanceStatus

    def to_dict(self) -> Dict[str, Any]:
        return {
            "failure_type": self.failure_type.value,
            "description": self.description,
            "injected": self.injected,
            "graceful_fallback": self.graceful_fallback,
            "retry_mechanism_triggered": self.retry_mechanism_triggered,
            "auto_recovered": self.auto_recovered,
            "recovery_time_ms": round(self.recovery_time_ms, 2),
            "data_corrupted": self.data_corrupted,
            "circuit_breaker_opened": self.circuit_breaker_opened,
            "status": self.status.value,
        }


@dataclass
class DisasterRecoveryMetric:
    """Disaster recovery and business continuity verification."""
    backup_snapshot_valid: bool
    backup_size_mb: float
    backup_duration_sec: float
    rto_minutes_achieved: float
    rto_target_minutes: float
    rto_compliant: bool
    rpo_minutes_achieved: float
    rpo_target_minutes: float
    rpo_compliant: bool
    point_in_time_recovery_verified: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "backup_snapshot_valid": self.backup_snapshot_valid,
            "backup_size_mb": round(self.backup_size_mb, 2),
            "backup_duration_sec": round(self.backup_duration_sec, 2),
            "rto_minutes_achieved": round(self.rto_minutes_achieved, 1),
            "rto_target_minutes": round(self.rto_target_minutes, 1),
            "rto_compliant": self.rto_compliant,
            "rpo_minutes_achieved": round(self.rpo_minutes_achieved, 1),
            "rpo_target_minutes": round(self.rpo_target_minutes, 1),
            "rpo_compliant": self.rpo_compliant,
            "point_in_time_recovery_verified": self.point_in_time_recovery_verified,
        }


@dataclass
class ReliabilityMetric:
    """Platform availability and reliability calculation."""
    availability_pct: float
    mtbf_hours: float
    mttr_ms: float
    error_rate_pct: float
    total_requests_evaluated: int
    sla_availability_target_pct: float
    sla_met: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "availability_pct": round(self.availability_pct, 4),
            "mtbf_hours": round(self.mtbf_hours, 1),
            "mttr_ms": round(self.mttr_ms, 2),
            "error_rate_pct": round(self.error_rate_pct, 4),
            "total_requests_evaluated": self.total_requests_evaluated,
            "sla_availability_target_pct": self.sla_availability_target_pct,
            "sla_met": self.sla_met,
        }


@dataclass
class ObservabilityTrace:
    """Distributed tracing and telemetry validation."""
    trace_id: str
    correlation_id: str
    spans_count: int
    root_service: str
    end_to_end_duration_ms: float
    structured_logging_compliant: bool
    otel_context_propagated: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "correlation_id": self.correlation_id,
            "spans_count": self.spans_count,
            "root_service": self.root_service,
            "end_to_end_duration_ms": round(self.end_to_end_duration_ms, 2),
            "structured_logging_compliant": self.structured_logging_compliant,
            "otel_context_propagated": self.otel_context_propagated,
        }


@dataclass
class EnterpriseReadinessScore:
    """Composite Enterprise Performance, Reliability & Readiness Score."""
    performance_score: float      # Weight: 30%
    reliability_score: float      # Weight: 35%
    efficiency_score: float       # Weight: 20%
    observability_score: float    # Weight: 15%
    overall_readiness_score: float
    grade: str
    certification_status: str
    evaluated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "performance_score": round(self.performance_score, 1),
            "reliability_score": round(self.reliability_score, 1),
            "efficiency_score": round(self.efficiency_score, 1),
            "observability_score": round(self.observability_score, 1),
            "overall_readiness_score": round(self.overall_readiness_score, 1),
            "grade": self.grade,
            "certification_status": self.certification_status,
            "evaluated_at": self.evaluated_at,
        }
