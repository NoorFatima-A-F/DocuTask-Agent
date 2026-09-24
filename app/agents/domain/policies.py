"""
Reusable Execution Policy Domain Models.
Defines Execution, Retry, Timeout, Concurrency, Failure, Escalation, Human Review, Fallback, Checkpoint, and Cancellation Policies.
"""

from typing import Optional
from pydantic import BaseModel, Field
from app.agents.domain.enums import RetryStrategy


class RetryPolicy(BaseModel):
    """Retry policy configuration."""
    max_retries: int = Field(default=3, ge=0)
    strategy: RetryStrategy = Field(default=RetryStrategy.EXPONENTIAL_BACKOFF)
    initial_interval_seconds: float = Field(default=2.0, gt=0.0)
    backoff_multiplier: float = Field(default=2.0, ge=1.0)
    max_interval_seconds: float = Field(default=60.0, gt=0.0)
    model_config = {"frozen": True}


class TimeoutPolicy(BaseModel):
    """Timeout policy configuration."""
    timeout_seconds: float = Field(default=300.0, gt=0.0)
    model_config = {"frozen": True}


class ConcurrencyPolicy(BaseModel):
    """Concurrency policy configuration."""
    max_parallel_tasks: int = Field(default=4, ge=1)
    model_config = {"frozen": True}


class FailurePolicy(BaseModel):
    """Failure policy configuration."""
    allow_partial_failure: bool = Field(default=False)
    fail_fast: bool = Field(default=True)
    model_config = {"frozen": True}


class HumanReviewPolicy(BaseModel):
    """Human-in-the-loop review policy configuration."""
    require_human_review: bool = Field(default=False)
    confidence_threshold_for_review: float = Field(default=0.8, ge=0.0, le=1.0)
    model_config = {"frozen": True}


class FallbackPolicy(BaseModel):
    """Fallback policy configuration."""
    enable_fallback: bool = Field(default=True)
    fallback_handler_name: Optional[str] = Field(default=None)
    model_config = {"frozen": True}


class CheckpointPolicy(BaseModel):
    """State checkpoint policy configuration."""
    enable_checkpointing: bool = Field(default=True)
    checkpoint_frequency_steps: int = Field(default=1, ge=1)
    model_config = {"frozen": True}


class ExecutionPolicy(BaseModel):
    """Aggregate Execution Policy combining sub-policies."""
    retry: RetryPolicy = Field(default_factory=RetryPolicy)
    timeout: TimeoutPolicy = Field(default_factory=TimeoutPolicy)
    concurrency: ConcurrencyPolicy = Field(default_factory=ConcurrencyPolicy)
    failure: FailurePolicy = Field(default_factory=FailurePolicy)
    human_review: HumanReviewPolicy = Field(default_factory=HumanReviewPolicy)
    fallback: FallbackPolicy = Field(default_factory=FallbackPolicy)
    checkpoint: CheckpointPolicy = Field(default_factory=CheckpointPolicy)
    model_config = {"frozen": True}
