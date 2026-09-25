"""
Reflection Extended Context and Execution Trace Models.
Provides structured models representing completed execution traces, task events, and reasoning steps.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class TaskTrace(BaseModel):
    """Execution trace of an individual task node in the plan."""
    task_id: str
    task_name: str
    status: str = Field(default="COMPLETED")  # COMPLETED, FAILED, CANCELLED, TIMED_OUT
    duration_ms: float = Field(default=0.0, ge=0.0)
    retry_count: int = Field(default=0, ge=0)
    worker_id: Optional[str] = None
    tool_name: Optional[str] = None
    input_parameters: Dict[str, Any] = Field(default_factory=dict)
    output_result: Optional[Any] = None
    error_message: Optional[str] = None
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

    model_config = {"frozen": True}


class ToolCallTrace(BaseModel):
    """Detailed trace of an external tool invocation."""
    call_id: UUID = Field(default_factory=uuid4)
    tool_name: str
    action: str = Field(default="execute")
    duration_ms: float = Field(default=0.0, ge=0.0)
    success: bool = True
    input_payload: Dict[str, Any] = Field(default_factory=dict)
    output_payload: Optional[Dict[str, Any]] = None
    error_details: Optional[str] = None
    retry_attempt: int = 0

    model_config = {"frozen": True}


class ReasoningStepTrace(BaseModel):
    """Cognitive reasoning and inference trace from planner or decision engine."""
    step_id: str
    rationale: str
    hypotheses: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    conclusion: str
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    assumptions: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}


class DecisionTrace(BaseModel):
    """Trace of policy evaluation or operational decision."""
    decision_id: str
    policy_name: str
    outcome: str = Field(default="ALLOWED")
    risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    evaluated_rules: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}


class ExecutionTraceEnvelope(BaseModel):
    """Complete, immutable envelope capturing all trace details of a finished execution."""
    execution_id: UUID
    plan_id: Optional[UUID] = None
    goal: str = Field(default="")
    final_state: str = Field(default="COMPLETED")
    total_duration_ms: float = Field(default=0.0, ge=0.0)
    token_usage: Dict[str, int] = Field(default_factory=dict)
    cost_usd: float = Field(default=0.0, ge=0.0)
    tasks: List[TaskTrace] = Field(default_factory=list)
    tool_calls: List[ToolCallTrace] = Field(default_factory=list)
    reasoning_steps: List[ReasoningStepTrace] = Field(default_factory=list)
    decisions: List[DecisionTrace] = Field(default_factory=list)
    recovery_actions: List[Dict[str, Any]] = Field(default_factory=list)
    checkpoints: List[Dict[str, Any]] = Field(default_factory=list)
    final_outputs: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}
