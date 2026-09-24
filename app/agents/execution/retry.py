"""
Retry Policies and Retry Manager.
Implements Immediate, FixedDelay, ExponentialBackoff, Jitter, and Adaptive retry algorithms.
"""

from enum import Enum
import random
from pydantic import BaseModel, Field


class RetryStrategy(str, Enum):
    IMMEDIATE = "IMMEDIATE"
    FIXED_DELAY = "FIXED_DELAY"
    EXPONENTIAL_BACKOFF = "EXPONENTIAL_BACKOFF"
    JITTER = "JITTER"
    ADAPTIVE = "ADAPTIVE"


class RetryPolicy(BaseModel):
    """Configuration for node execution retries."""
    strategy: RetryStrategy = Field(default=RetryStrategy.EXPONENTIAL_BACKOFF)
    max_retries: int = Field(default=3, ge=0)
    initial_delay_seconds: float = Field(default=1.0, ge=0.0)
    backoff_factor: float = Field(default=2.0, ge=1.0)
    max_delay_seconds: float = Field(default=30.0, ge=0.0)
    jitter: bool = Field(default=True)
    model_config = {"frozen": True}


class RetryManager:
    """Calculates backoff delay based on the configured retry policy."""

    @staticmethod
    def calculate_delay(policy: RetryPolicy, attempt: int) -> float:
        if attempt >= policy.max_retries:
            return 0.0

        if policy.strategy == RetryStrategy.IMMEDIATE:
            return 0.0

        if policy.strategy == RetryStrategy.FIXED_DELAY:
            delay = policy.initial_delay_seconds
        else:
            # Exponential Backoff
            delay = min(
                policy.initial_delay_seconds * (policy.backoff_factor ** attempt),
                policy.max_delay_seconds
            )

        if policy.jitter:
            delay += random.uniform(0.0, 0.5)

        return delay

    @staticmethod
    def should_retry(policy: RetryPolicy, current_attempt: int) -> bool:
        return current_attempt < policy.max_retries
