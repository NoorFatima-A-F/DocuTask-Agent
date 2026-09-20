"""
Enterprise Reusable Policies for Autonomous Agent Framework.
Defines ExecutionPolicy, RetryPolicy, ApprovalPolicy, CostPolicy, SecurityPolicy,
CompliancePolicy, PrivacyPolicy, DataPolicy, ToolSelectionPolicy, WorkflowPolicy,
PlannerPolicy, HumanReviewPolicy, EscalationPolicy, ResourcePolicy, and SchedulingPolicy.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ExecutionPolicy(BaseModel):
    """Task dispatch and execution boundary policy."""
    max_parallel_tasks: int = Field(default=10, ge=1)
    timeout_seconds: float = Field(default=300.0, gt=0.0)
    enforce_idempotency: bool = Field(default=True)
    model_config = {"frozen": True}


class RetryPolicy(BaseModel):
    """Retry policy for failed operations."""
    max_retries: int = Field(default=3, ge=0)
    initial_backoff_seconds: float = Field(default=1.0, gt=0.0)
    backoff_multiplier: float = Field(default=2.0, ge=1.0)
    model_config = {"frozen": True}


class CostPolicy(BaseModel):
    """Cost and financial quota policy."""
    max_cost_per_execution_usd: float = Field(default=5.0, ge=0.0)
    max_daily_budget_usd: float = Field(default=100.0, ge=0.0)
    enforce_budget_limits: bool = Field(default=True)
    model_config = {"frozen": True}


class SecurityPolicy(BaseModel):
    """Zero-trust security and data protection policy."""
    allow_external_api_calls: bool = Field(default=True)
    require_encryption: bool = Field(default=True)
    min_security_level: str = Field(default="INTERNAL")
    model_config = {"frozen": True}


class CompliancePolicy(BaseModel):
    """Regulatory and data residency compliance policy."""
    enforce_pii_masking: bool = Field(default=True)
    allowed_data_residency_regions: List[str] = Field(default_factory=lambda: ["us-central1", "global"])
    model_config = {"frozen": True}


class PrivacyPolicy(BaseModel):
    """Data privacy and retention policy."""
    anonymize_user_data: bool = Field(default=True)
    retention_days: int = Field(default=30, ge=1)
    model_config = {"frozen": True}


class DataPolicy(BaseModel):
    """Data schema and governance policy."""
    allow_unstructured_input: bool = Field(default=True)
    max_payload_size_mb: float = Field(default=25.0, gt=0.0)
    model_config = {"frozen": True}


class ToolSelectionPolicy(BaseModel):
    """Tool capability and resolution policy."""
    prefer_deterministic_tools: bool = Field(default=True)
    min_tool_confidence: float = Field(default=0.7, ge=0.0, le=1.0)
    model_config = {"frozen": True}


class WorkflowPolicy(BaseModel):
    """DAG workflow orchestration policy."""
    max_workflow_depth: int = Field(default=20, ge=1)
    allow_dynamic_replanning: bool = Field(default=True)
    model_config = {"frozen": True}


class PlannerPolicy(BaseModel):
    """High-level goal decomposition and planner policy."""
    max_subgoals: int = Field(default=10, ge=1)
    strict_dependency_ordering: bool = Field(default=True)
    model_config = {"frozen": True}


class ApprovalPolicy(BaseModel):
    """Automated and human approval threshold policy."""
    require_human_approval_above_cost_usd: float = Field(default=2.0, ge=0.0)
    require_approval_for_high_risk: bool = Field(default=True)
    approver_role: str = Field(default="ADMIN")
    model_config = {"frozen": True}


class HumanReviewPolicy(BaseModel):
    """Human-in-the-loop review criteria policy."""
    sample_review_rate: float = Field(default=0.05, ge=0.0, le=1.0)
    model_config = {"frozen": True}


class EscalationPolicy(BaseModel):
    """Escalation routing policy for severe exceptions."""
    escalate_on_repeated_failures: bool = Field(default=True)
    failure_threshold: int = Field(default=3, ge=1)
    model_config = {"frozen": True}


class ResourcePolicy(BaseModel):
    """Compute and token quota resource policy."""
    max_tokens_per_minute: int = Field(default=100000, ge=1000)
    max_concurrent_processes: int = Field(default=8, ge=1)
    model_config = {"frozen": True}


class SchedulingPolicy(BaseModel):
    """Job scheduling and queue priority policy."""
    priority_boost_enabled: bool = Field(default=True)
    model_config = {"frozen": True}
