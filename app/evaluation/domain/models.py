"""Domain Models for Phase 6: AI System Evaluation, Benchmarking & Portfolio Certification Framework."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class EvaluationStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"


class CertificationTier(str, Enum):
    ENTERPRISE_AI_PLATFORM_CERTIFIED = "Enterprise AI Platform Certified"
    HIGH_PERFORMANCE_AI_SYSTEM = "High Performance AI System"
    QUALIFIED_AI_SYSTEM = "Qualified AI System"
    REMEDIATION_REQUIRED = "Remediation Required"


class EvaluationCheck(BaseModel):
    check_id: str
    name: str
    status: EvaluationStatus
    score: float = Field(ge=0.0, le=100.0)
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part A: AI Capability Benchmark Models
class BenchmarkMetric(BaseModel):
    category: str
    dataset_name: str
    sample_count: int
    precision: float
    recall: float
    f1_score: float
    accuracy_pct: float


class AICapabilityBenchmarkReport(BaseModel):
    evaluator_id: str
    name: str
    status: EvaluationStatus
    score: float
    overall_accuracy_pct: float
    overall_f1_score: float
    benchmarks: List[BenchmarkMetric] = Field(default_factory=list)
    checks: List[EvaluationCheck] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part B: LLM Evaluation Models
class LLMEvalMetric(BaseModel):
    metric_name: str
    score: float
    threshold: float
    status: str
    details: str


class LLMEvaluationReport(BaseModel):
    evaluator_id: str
    name: str
    status: EvaluationStatus
    score: float
    faithfulness_score: float
    grounding_score: float
    hallucination_rate_pct: float
    semantic_similarity: float
    metrics: List[LLMEvalMetric] = Field(default_factory=list)
    checks: List[EvaluationCheck] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part C: Agent Evaluation Models
class AgentPerformanceScorecard(BaseModel):
    agent_name: str
    task_decomposition_efficiency: float
    goal_achievement_rate_pct: float
    tool_invocation_accuracy_pct: float
    error_recovery_rate_pct: float


class AgentEvaluationReport(BaseModel):
    evaluator_id: str
    name: str
    status: EvaluationStatus
    score: float
    overall_planning_success_rate_pct: float
    task_efficiency_score: float
    memory_recall_relevance_pct: float
    agent_scorecards: List[AgentPerformanceScorecard] = Field(default_factory=list)
    checks: List[EvaluationCheck] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part D: RAG Evaluation Models
class RAGBenchmarkMetric(BaseModel):
    metric_name: str
    value: float
    target: float
    description: str


class RAGEvaluationReport(BaseModel):
    evaluator_id: str
    name: str
    status: EvaluationStatus
    score: float
    precision_at_k: float
    recall_at_k: float
    mrr_score: float
    ndcg_score: float
    context_noise_ratio_pct: float
    with_vs_without_rag_improvement_pct: float
    metrics: List[RAGBenchmarkMetric] = Field(default_factory=list)
    checks: List[EvaluationCheck] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part E: Performance Benchmarking Models
class LatencyPercentile(BaseModel):
    operation_name: str
    p50_ms: float
    p95_ms: float
    p99_ms: float
    sla_target_ms: float


class PerformanceBenchmarkReport(BaseModel):
    evaluator_id: str
    name: str
    status: EvaluationStatus
    score: float
    e2e_p95_latency_ms: float
    throughput_wps: float
    documents_per_minute: float
    cpu_utilization_pct: float
    ram_usage_mb: float
    latencies: List[LatencyPercentile] = Field(default_factory=list)
    checks: List[EvaluationCheck] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part F & Q: Cost & Business Intelligence Models
class BusinessROISpec(BaseModel):
    use_case: str
    manual_cost_per_doc_usd: float
    ai_cost_per_doc_usd: float
    annual_savings_usd: float
    hours_saved_annual: float


class CostBusinessReport(BaseModel):
    evaluator_id: str
    name: str
    status: EvaluationStatus
    score: float
    cost_per_document_usd: float
    cost_reduction_pct: float
    annual_roi_multiple: float
    total_hours_liberated_annual: float
    use_cases: List[BusinessROISpec] = Field(default_factory=list)
    checks: List[EvaluationCheck] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part G: Reliability Evaluation Models
class ReliabilityMetric(BaseModel):
    scenario: str
    injected_fault: str
    recovery_time_sec: float
    recovered_successfully: bool


class ReliabilityEvaluationReport(BaseModel):
    evaluator_id: str
    name: str
    status: EvaluationStatus
    score: float
    availability_pct: float
    fault_recovery_rate_pct: float
    mean_time_to_recovery_sec: float
    scenarios: List[ReliabilityMetric] = Field(default_factory=list)
    checks: List[EvaluationCheck] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part H: Security Evaluation Models
class SecurityAuditMetric(BaseModel):
    vector_name: str
    test_count: int
    prevented_count: int
    success_rate_pct: float


class SecurityEvaluationReport(BaseModel):
    evaluator_id: str
    name: str
    status: EvaluationStatus
    score: float
    prompt_injection_resistance_pct: float
    tenant_data_leakage_events: int
    rbac_privilege_escalations_prevented: int
    audits: List[SecurityAuditMetric] = Field(default_factory=list)
    checks: List[EvaluationCheck] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part I: Explainability Models
class DecisionTraceEntry(BaseModel):
    trace_id: str
    document_type: str
    decision_summary: str
    bounding_box_citations_count: int
    policy_reference: str
    confidence: float


class ExplainabilityReport(BaseModel):
    evaluator_id: str
    name: str
    status: EvaluationStatus
    score: float
    decision_trace_coverage_pct: float
    citation_precision_pct: float
    traces: List[DecisionTraceEntry] = Field(default_factory=list)
    checks: List[EvaluationCheck] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part J & K: Human Experience & Comparison Benchmark Models
class ApproachComparison(BaseModel):
    approach_name: str
    accuracy_pct: float
    automation_capability: str
    reliability: str
    business_roi: str


class HumanExperienceReport(BaseModel):
    evaluator_id: str
    name: str
    status: EvaluationStatus
    score: float
    system_usability_scale_score: float
    average_clicks_per_workflow: float
    user_error_rate_pct: float
    comparisons: List[ApproachComparison] = Field(default_factory=list)
    checks: List[EvaluationCheck] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Overall Certification & Portfolio Score Models
class CategoryScore(BaseModel):
    name: str
    weight: float
    score: float
    weighted_score: float
    checks_total: int
    checks_passed: int
    status: EvaluationStatus


class PlatformCertificationScore(BaseModel):
    overall_score: float = Field(ge=0.0, le=100.0)
    certification_tier: CertificationTier
    evaluation_status: EvaluationStatus
    categories: List[CategoryScore] = Field(default_factory=list)
    calculated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PortfolioShowcaseReport(BaseModel):
    project_name: str = "DocuTask Agent"
    phase: str = "Phase 6 - AI System Evaluation, Benchmarking & Portfolio Certification"
    evaluation_id: str
    status: EvaluationStatus
    score: PlatformCertificationScore
    reports: Dict[str, Any] = Field(default_factory=dict)
    summary_markdown: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
