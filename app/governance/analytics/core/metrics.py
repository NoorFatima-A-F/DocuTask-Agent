"""Governance Metrics Definitions, Summaries, and Periods."""

from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class MetricPeriod(str, Enum):
    LAST_HOUR = "LAST_HOUR"
    LAST_24_HOURS = "LAST_24_HOURS"
    LAST_7_DAYS = "LAST_7_DAYS"
    LAST_30_DAYS = "LAST_30_DAYS"
    LAST_90_DAYS = "LAST_90_DAYS"
    CUSTOM = "CUSTOM"


class MetricTrend(str, Enum):
    IMPROVING = "IMPROVING"
    STABLE = "STABLE"
    DEGRADING = "DEGRADING"
    CRITICAL_SPIKE = "CRITICAL_SPIKE"


class MetricValue(BaseModel):
    name: str
    value: float
    unit: str = "count"
    previous_value: Optional[float] = None
    change_pct: Optional[float] = None
    trend: MetricTrend = MetricTrend.STABLE
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DecisionMetricsSummary(BaseModel):
    total_decisions: int = 0
    allowed_decisions: int = 0
    denied_decisions: int = 0
    blocked_actions: int = 0
    approval_required_count: int = 0
    escalations_count: int = 0
    override_count: int = 0
    allow_rate: float = 1.0
    block_rate: float = 0.0
    override_rate: float = 0.0


class PolicyMetricsSummary(BaseModel):
    active_policies_count: int = 0
    total_policy_violations: int = 0
    most_triggered_policies: List[Dict[str, Any]] = Field(default_factory=list)
    unused_policies_count: int = 0
    policy_effectiveness_score: float = 1.0
    policy_conflict_frequency: int = 0


class AgentMetricsSummary(BaseModel):
    total_agent_executions: int = 0
    failed_agent_executions: int = 0
    avg_agent_risk_score: float = 0.0
    agent_approval_rate: float = 1.0
    agent_override_rate: float = 0.0
    agent_breakdown: Dict[str, Dict[str, Any]] = Field(default_factory=dict)


class ModelMetricsSummary(BaseModel):
    total_model_invocations: int = 0
    model_failure_count: int = 0
    avg_model_risk_score: float = 0.0
    avg_latency_ms: float = 0.0
    total_cost_usd: float = 0.0
    model_drift_signals_count: int = 0
    model_usage_breakdown: Dict[str, int] = Field(default_factory=dict)


class PromptMetricsSummary(BaseModel):
    total_prompt_executions: int = 0
    prompt_failures_count: int = 0
    avg_evaluation_score: float = 1.0
    prompt_safety_violations: int = 0
    prompt_drift_alerts: int = 0
    prompt_usage_breakdown: Dict[str, int] = Field(default_factory=dict)
