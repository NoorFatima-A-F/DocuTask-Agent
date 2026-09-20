"""
Reflection Context, Request, and Result Models.
Defines canonical boundaries for invoking and obtaining results from the reflection engine.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.reflection.lifecycle import ReflectionLifecycleState
from app.agents.reflection.metadata import ReflectionIdentity, ReflectionMetadata, ReflectionStatistics
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class ReflectionContext(BaseModel):
    """Operational context and environment limits for reflection processing."""
    tenant_id: str = Field(default="default")
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    max_evaluation_timeout_sec: float = Field(default=300.0, gt=0.0)
    enable_hallucination_detection: bool = True
    enable_deep_critique: bool = True
    enable_learning_extraction: bool = True
    parameters: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class ReflectionRequest(BaseModel):
    """Request payload to initiate reflection on a completed execution."""
    trace: ExecutionTraceEnvelope
    context: ReflectionContext = Field(default_factory=ReflectionContext)
    historical_traces: List[ExecutionTraceEnvelope] = Field(default_factory=list)

    model_config = {"frozen": True}


class ReflectionResult(BaseModel):
    """Structured, immutable outcome produced by the reflection engine."""
    identity: ReflectionIdentity
    lifecycle_state: ReflectionLifecycleState = Field(default=ReflectionLifecycleState.COMPLETED)
    evaluation_report: Optional[Any] = None
    critique: Optional[Any] = None
    learning_artifacts: List[Any] = Field(default_factory=list)
    recommendations: List[Any] = Field(default_factory=list)
    adaptation_proposals: List[Any] = Field(default_factory=list)
    planner_feedback: Optional[Any] = None
    execution_feedback: Optional[Any] = None
    memory_feedback: Optional[Any] = None
    tool_feedback: Optional[Any] = None
    statistics: ReflectionStatistics = Field(default_factory=ReflectionStatistics)
    errors: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}
