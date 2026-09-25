"""Phase 3J.7: Enterprise Performance Bottleneck Discovery & Capacity Engineering — Domain Models."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class VerificationStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"


PerformanceVerificationStatus = VerificationStatus


class EnterprisePerformanceTier(str, Enum):
    ENTERPRISE_PERFORMANCE_READY = "Enterprise Performance Engineering Ready"  # 95-100
    PRODUCTION_PERFORMANCE_READY = "Production Performance Ready"              # 90-94.99
    OPTIMIZATION_REQUIRED = "Optimization Required"                            # 80-89.99
    FAILED = "Failed"                                                          # <80


CertificationTier = EnterprisePerformanceTier


class CheckResult(BaseModel):
    name: str
    passed: bool
    details: str
    metrics: Dict[str, Any] = Field(default_factory=dict)


class BaseVerificationReport(BaseModel):
    verifier_id: str = ""
    phase_id: str = ""
    phase_name: str = ""
    status: VerificationStatus = VerificationStatus.PASSED
    score: float = 100.0
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    execution_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    summary: str = ""


# ─── 3J.7.1: Performance Architecture Profiling Models ──────────────────────

class ServiceDependency(BaseModel):
    source: str
    target: str
    protocol: str
    avg_latency_ms: float
    is_critical_path: bool = False


class PerformanceArchitectureReport(BaseVerificationReport):
    report_title: str = "Performance Architecture Profiling Report"
    services_count: int = 8
    dependencies_count: int = 12
    critical_path: List[str] = Field(default_factory=list)
    dependencies: List[ServiceDependency] = Field(default_factory=list)


# ─── 3J.7.2: Resource Saturation Analysis Models ────────────────────────────

class ResourceSaturationMetric(BaseModel):
    resource_type: str          # CPU, Memory, Disk, Network
    current_utilization_pct: float
    saturation_threshold_pct: float
    headroom_pct: float
    bottleneck_detected: bool = False
    details: str = ""


class ResourceSaturationReport(BaseVerificationReport):
    report_title: str = "Resource Saturation Analysis Report"
    resource_metrics: List[ResourceSaturationMetric] = Field(default_factory=list)
    cpu_saturation_detected: bool = False
    memory_saturation_detected: bool = False
    disk_saturation_detected: bool = False
    network_saturation_detected: bool = False


# ─── 3J.7.3: Application-Level Bottleneck Models ────────────────────────────

class ApplicationBottleneck(BaseModel):
    layer: str                  # API, Agent Runtime, Worker
    metric_name: str
    observed_value: float
    threshold: float
    is_bottleneck: bool = False
    recommendation: str = ""


class ApplicationBottleneckReport(BaseVerificationReport):
    report_title: str = "Application-Level Bottleneck Analysis Report"
    bottlenecks: List[ApplicationBottleneck] = Field(default_factory=list)
    api_bottleneck_detected: bool = False
    agent_runtime_bottleneck_detected: bool = False
    worker_bottleneck_detected: bool = False


# ─── 3J.7.4: Database Bottleneck Models ─────────────────────────────────────

class SlowQuery(BaseModel):
    query_id: str
    query_summary: str
    avg_duration_ms: float
    execution_count: int
    recommendation: str = ""


class DatabaseBottleneckReport(BaseVerificationReport):
    report_title: str = "Database Bottleneck Verification Report"
    slow_queries: List[SlowQuery] = Field(default_factory=list)
    slow_queries_count: int = 0
    connection_utilization_pct: float = 0.0
    deadlocks_detected: int = 0
    long_transactions_count: int = 0
    blocking_queries_count: int = 0
    pool_exhaustion_detected: bool = False


# ─── 3J.7.5: Queue Bottleneck Models ────────────────────────────────────────

class QueueBottleneckReport(BaseVerificationReport):
    report_title: str = "Queue Bottleneck Analysis Report"
    queue_depth_current: int = 0
    enqueue_rate_jobs_min: int = 0
    processing_rate_jobs_min: int = 0
    consumer_lag_jobs: int = 0
    queue_growth_detected: bool = False
    worker_capacity_shortage: bool = False


# ─── 3J.7.6: Worker Capacity Modeling Models ────────────────────────────────

class WorkerCapacityModel(BaseModel):
    single_worker_throughput_dpm: float
    expected_load_dpm: float
    required_workers: int
    current_workers: int
    surplus_deficit: int
    scaling_recommendation: str = ""


class WorkerCapacityReport(BaseVerificationReport):
    report_title: str = "Worker Capacity Modeling Report"
    capacity_model: Optional[WorkerCapacityModel] = None
    horizontal_scaling_validated: bool = True
    optimal_worker_count: int = 0
    max_effective_workers: int = 0


# ─── 3J.7.7: AI Provider Performance Models ─────────────────────────────────

class AIProviderMetric(BaseModel):
    provider_name: str
    avg_request_latency_ms: float
    p95_request_latency_ms: float
    token_processing_time_ms: float
    retry_overhead_ms: float
    failure_rate_pct: float


class AIProviderPerformanceReport(BaseVerificationReport):
    report_title: str = "AI Provider Performance Analysis Report"
    providers: List[AIProviderMetric] = Field(default_factory=list)
    latency_stress_impact: str = ""
    queue_growth_under_ai_stress: bool = False
    worker_blocking_under_ai_stress: bool = False
    optimization_recommendations: List[str] = Field(default_factory=list)


# ─── 3J.7.8: Performance Regression Detection Models ────────────────────────

class RegressionComparison(BaseModel):
    metric_name: str
    baseline_value: float
    current_value: float
    change_pct: float
    tolerance_pct: float
    regression_detected: bool = False


class PerformanceRegressionReport(BaseVerificationReport):
    report_title: str = "Performance Regression Detection Report"
    baseline_version: str = "v1.0"
    current_version: str = "v1.1"
    comparisons: List[RegressionComparison] = Field(default_factory=list)
    regressions_found: int = 0
    within_tolerance: bool = True


# ─── 3J.7.9: Capacity Boundary Discovery Models ─────────────────────────────

class CapacityBoundaryStage(BaseModel):
    concurrent_users: int
    p95_latency_ms: float
    error_rate_pct: float
    cpu_pct: float
    memory_pct: float
    queue_size: int
    zone: str            # Normal, Warning, Failure


class CapacityBoundaryReport(BaseVerificationReport):
    report_title: str = "Capacity Boundary Discovery Report"
    stages: List[CapacityBoundaryStage] = Field(default_factory=list)
    normal_capacity_max_users: int = 0
    warning_zone_start_users: int = 0
    failure_zone_start_users: int = 0
    operating_boundary_defined: bool = True


# ─── 3J.7.10: Performance Optimization Recommendations Models ───────────────

class OptimizationRecommendation(BaseModel):
    issue: str
    evidence: str
    recommendation: str
    category: str        # architecture, infrastructure, database, caching, ai
    priority: str = "HIGH"


class OptimizationRecommendationsReport(BaseVerificationReport):
    report_title: str = "Performance Optimization Recommendations Report"
    recommendations: List[OptimizationRecommendation] = Field(default_factory=list)
    total_recommendations: int = 0
    high_priority_count: int = 0
    architecture_changes: int = 0
    infrastructure_scaling: int = 0
    database_optimizations: int = 0
    caching_opportunities: int = 0
    ai_optimizations: int = 0


# ─── Quality Scoring & Certification Models ──────────────────────────────────

class CategoryScore(BaseModel):
    category: str
    weight: float
    score: float
    weighted_score: float
    description: str


class EnterpriseBottleneckCertificationReport(BaseVerificationReport):
    report_title: str = "Enterprise Bottleneck Discovery & Capacity Engineering Certification Report"
    system: str = "DocuTask Agent"
    version: str = "v3.14.0"
    commit: str = "HEAD"
    environment: str = "Enterprise SRE Bottleneck Analysis Environment"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    test_duration: str = "Comprehensive Bottleneck Discovery & Capacity Engineering Suite"
    overall_score: float = 100.0
    certification_tier: EnterprisePerformanceTier = EnterprisePerformanceTier.ENTERPRISE_PERFORMANCE_READY
    passed: bool = True
    summary: str = ""
    category_scores: List[CategoryScore] = Field(default_factory=list)


# ─── Manifest Model ─────────────────────────────────────────────────────────

class BottleneckVerificationManifest(BaseModel):
    system: str = "DocuTask Agent"
    version: str = "v3.14.0"
    environment: str = "Enterprise SRE Bottleneck Analysis Environment"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    overall_score: float = 100.0
    certification_tier: str = "Enterprise Performance Engineering Ready"
    passed: bool = True
    reports_generated: List[str] = Field(default_factory=list)
    file_hashes: Dict[str, str] = Field(default_factory=dict)


# Aliases
PerformanceCertificationReport = EnterpriseBottleneckCertificationReport
