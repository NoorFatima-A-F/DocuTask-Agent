"""
Immutable Agent Domain Value Objects.
Eliminates primitive obsession by providing strongly typed, validated immutable value objects using Pydantic v2.
"""

from typing import Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, field_validator


class GoalID(BaseModel):
    """Strongly typed Goal Identifier."""
    value: UUID = Field(default_factory=uuid4)
    model_config = {"frozen": True}

    def __str__(self) -> str:
        return str(self.value)


class TaskID(BaseModel):
    """Strongly typed Task Identifier."""
    value: UUID = Field(default_factory=uuid4)
    model_config = {"frozen": True}

    def __str__(self) -> str:
        return str(self.value)


class WorkflowID(BaseModel):
    """Strongly typed Workflow Identifier."""
    value: UUID = Field(default_factory=uuid4)
    model_config = {"frozen": True}

    def __str__(self) -> str:
        return str(self.value)


class ExecutionID(BaseModel):
    """Strongly typed Execution Identifier."""
    value: UUID = Field(default_factory=uuid4)
    model_config = {"frozen": True}

    def __str__(self) -> str:
        return str(self.value)


class CorrelationID(BaseModel):
    """Strongly typed Correlation Identifier."""
    value: str = Field(default_factory=lambda: str(uuid4()))
    model_config = {"frozen": True}

    def __str__(self) -> str:
        return self.value


class ArtifactID(BaseModel):
    """Strongly typed Artifact Identifier."""
    value: UUID = Field(default_factory=uuid4)
    model_config = {"frozen": True}

    def __str__(self) -> str:
        return str(self.value)


class ConfidenceScore(BaseModel):
    """Validated confidence score value object between 0.0 and 1.0."""
    value: float = Field(default=1.0, ge=0.0, le=1.0)
    model_config = {"frozen": True}


class ExecutionDuration(BaseModel):
    """Execution duration in milliseconds."""
    duration_ms: float = Field(default=0.0, ge=0.0)
    model_config = {"frozen": True}


class RetryCount(BaseModel):
    """Non-negative retry attempts counter."""
    attempts: int = Field(default=0, ge=0)
    max_allowed: int = Field(default=3, ge=0)
    model_config = {"frozen": True}

    def can_retry(self) -> bool:
        return self.attempts < self.max_allowed


class TokenUsage(BaseModel):
    """LLM Token consumption value object."""
    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
    model_config = {"frozen": True}

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


class ExecutionCost(BaseModel):
    """Execution cost in USD."""
    cost_usd: float = Field(default=0.0, ge=0.0)
    currency: str = Field(default="USD")
    model_config = {"frozen": True}


class Latency(BaseModel):
    """Latency measurement value object."""
    latency_ms: float = Field(default=0.0, ge=0.0)
    model_config = {"frozen": True}
