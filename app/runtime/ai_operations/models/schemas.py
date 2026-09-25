"""
Phase 13.17: AI Operations Models & Schemas
Enterprise Agent Observability, Evaluation, Optimization & Improvement Platform.
"""

from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
import uuid


class SpanType(str, Enum):
    AGENT_RUN = "AGENT_RUN"
    LLM_CALL = "LLM_CALL"
    TOOL_EXECUTION = "TOOL_EXECUTION"
    RETRIEVAL = "RETRIEVAL"
    REASONING_STEP = "REASONING_STEP"
    EVALUATION = "EVALUATION"
    GUARDRAIL_CHECK = "GUARDRAIL_CHECK"


class SpanStatus(str, Enum):
    OK = "OK"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"
    CANCELLED = "CANCELLED"


class AgentHealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    CRITICAL = "CRITICAL"
    OFFLINE = "OFFLINE"


class FailureCategory(str, Enum):
    TOOL_TIMEOUT = "TOOL_TIMEOUT"
    TOOL_SCHEMA_VIOLATION = "TOOL_SCHEMA_VIOLATION"
    RECURSIVE_LOOP = "RECURSIVE_LOOP"
    CONTEXT_WINDOW_OVERFLOW = "CONTEXT_WINDOW_OVERFLOW"
    CONFIDENCE_DECAY = "CONFIDENCE_DECAY"
    HALLUCINATION_DETECTED = "HALLUCINATION_DETECTED"
    PII_POLICY_VIOLATION = "PII_POLICY_VIOLATION"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    UNSPECIFIED_RUNTIME_ERROR = "UNSPECIFIED_RUNTIME_ERROR"


class ModelTier(str, Enum):
    FLASH_LITE = "gemini-2.0-flash-lite"
    FLASH = "gemini-2.0-flash"
    PRO = "gemini-1.5-pro"
    OMNI = "gemini-omni-1.1-flash"
    LOCAL_EMBED = "local-granite-embed"


class ProposalStatus(str, Enum):
    DRAFT = "DRAFT"
    CANARY_TESTING = "CANARY_TESTING"
    PENDING_HITL_APPROVAL = "PENDING_HITL_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DEPLOYED = "DEPLOYED"
    ROLLED_BACK = "ROLLED_BACK"


class ExperimentStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    STOPPED_EARLY = "STOPPED_EARLY"


# ---------------------------------------------------------
# Telemetry & Distributed Tracing
# ---------------------------------------------------------

class Span(BaseModel):
    span_id: str = Field(default_factory=lambda: f"span_{uuid.uuid4().hex[:10]}")
    trace_id: str
    parent_span_id: Optional[str] = None
    name: str
    span_type: SpanType
    agent_id: str
    start_time: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    end_time: Optional[str] = None
    duration_ms: float = 0.0
    status: SpanStatus = SpanStatus.OK
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    token_usage: Dict[str, int] = Field(default_factory=lambda: {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0})
    cost_usd: float = 0.0
    error_message: Optional[str] = None


class ExecutionTrace(BaseModel):
    trace_id: str = Field(default_factory=lambda: f"trace_{uuid.uuid4().hex[:12]}")
    session_id: str
    agent_id: str
    root_span_name: str
    start_time: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    end_time: Optional[str] = None
    total_duration_ms: float = 0.0
    status: SpanStatus = SpanStatus.OK
    spans: List[Span] = Field(default_factory=list)
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_cost_usd: float = 0.0
    tags: Dict[str, str] = Field(default_factory=dict)


class AgentTelemetry(BaseModel):
    agent_id: str
    agent_name: str
    role: str
    version: str = "v1.0.0"
    health_status: AgentHealthStatus = AgentHealthStatus.HEALTHY
    uptime_seconds: float = 0.0
    active_invocations: int = 0
    total_invocations: int = 0
    success_rate: float = 1.0
    error_rate: float = 0.0
    avg_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    total_tokens_consumed: int = 0
    total_cost_usd: float = 0.0
    last_active: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    resource_utilization: Dict[str, float] = Field(default_factory=lambda: {"cpu_pct": 12.5, "memory_mb": 256.0})


# ---------------------------------------------------------
# Evaluation Models
# ---------------------------------------------------------

class MetricScore(BaseModel):
    metric_name: str
    score: float  # 0.0 - 1.0
    passed: bool
    threshold: float
    confidence: float = 1.0
    details: Dict[str, Any] = Field(default_factory=dict)


class EvaluationResult(BaseModel):
    eval_id: str = Field(default_factory=lambda: f"eval_{uuid.uuid4().hex[:10]}")
    trace_id: Optional[str] = None
    agent_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    task_success_score: float = 1.0
    accuracy_score: float = 1.0
    grounding_score: float = 1.0
    hallucination_index: float = 0.0
    safety_score: float = 1.0
    tool_efficiency_score: float = 1.0
    cost_efficiency_score: float = 1.0
    llm_judge_score: float = 1.0
    composite_quality_score: float = 1.0
    status: str = "PASSED"
    metrics: List[MetricScore] = Field(default_factory=list)
    judge_critique: Optional[str] = None


# ---------------------------------------------------------
# Root Cause & Failure Analysis
# ---------------------------------------------------------

class FailureAnalysisResult(BaseModel):
    analysis_id: str = Field(default_factory=lambda: f"fail_{uuid.uuid4().hex[:10]}")
    trace_id: str
    agent_id: str
    category: FailureCategory
    root_cause_summary: str
    failing_span_id: Optional[str] = None
    critical_path: List[str] = Field(default_factory=list)
    confidence: float = 0.95
    suggested_remediation: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ---------------------------------------------------------
# Optimization & Model Routing
# ---------------------------------------------------------

class ModelRouteDecision(BaseModel):
    decision_id: str = Field(default_factory=lambda: f"route_{uuid.uuid4().hex[:10]}")
    task_id: str
    selected_model: str
    selected_tier: ModelTier
    estimated_cost_usd: float
    estimated_latency_ms: float
    estimated_quality_score: float
    pareto_score: float
    weights: Dict[str, float] = Field(default_factory=lambda: {"quality": 0.5, "latency": 0.3, "cost": 0.2})
    fallback_models: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PromptVersion(BaseModel):
    prompt_id: str
    version: str
    agent_id: str
    system_instruction: str
    few_shot_examples: List[Dict[str, str]] = Field(default_factory=list)
    active: bool = False
    average_score: float = 0.0
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    created_by: str = "system"
    mutation_notes: Optional[str] = None


# ---------------------------------------------------------
# Improvement & A/B Canary Experiments
# ---------------------------------------------------------

class ImprovementProposal(BaseModel):
    proposal_id: str = Field(default_factory=lambda: f"prop_{uuid.uuid4().hex[:10]}")
    target_agent_id: str
    title: str
    description: str
    proposal_type: str  # PROMPT_REFINEMENT, MODEL_UPGRADE, TOOL_ROUTING, CONTEXT_COMPRESSION
    status: ProposalStatus = ProposalStatus.PENDING_HITL_APPROVAL
    proposed_changes: Dict[str, Any] = Field(default_factory=dict)
    diff_summary: str = ""
    expected_quality_delta: float = 0.0
    expected_latency_delta_ms: float = 0.0
    expected_cost_delta_pct: float = 0.0
    experiment_id: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    rejection_reason: Optional[str] = None


class ExperimentRecord(BaseModel):
    experiment_id: str = Field(default_factory=lambda: f"exp_{uuid.uuid4().hex[:10]}")
    name: str
    agent_id: str
    control_version: str
    candidate_version: str
    sample_size: int = 100
    control_success_rate: float = 0.0
    candidate_success_rate: float = 0.0
    control_avg_latency_ms: float = 0.0
    candidate_avg_latency_ms: float = 0.0
    control_avg_cost_usd: float = 0.0
    candidate_avg_cost_usd: float = 0.0
    p_value: float = 0.05
    effect_size_cohen_d: float = 0.0
    statistically_significant: bool = False
    status: ExperimentStatus = ExperimentStatus.COMPLETED
    started_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None


# ---------------------------------------------------------
# Governance, Compliance & Auditing
# ---------------------------------------------------------

class GovernanceAuditRecord(BaseModel):
    audit_id: str = Field(default_factory=lambda: f"audit_{uuid.uuid4().hex[:10]}")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_type: str
    actor: str
    agent_id: Optional[str] = None
    action_summary: str
    compliance_passed: bool = True
    pii_detected: bool = False
    pii_types_redacted: List[str] = Field(default_factory=list)
    policy_name: Optional[str] = None
    signature_hash: str = Field(default_factory=lambda: uuid.uuid4().hex)
