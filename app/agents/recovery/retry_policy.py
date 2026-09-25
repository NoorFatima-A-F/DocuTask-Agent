"""
Recovery Retry Policy Models.
"""

from enum import Enum
from pydantic import BaseModel, Field


class RecoveryBackoffType(str, Enum):
    IMMEDIATE = "IMMEDIATE"
    FIXED = "FIXED"
    LINEAR = "LINEAR"
    EXPONENTIAL_JITTER = "EXPONENTIAL_JITTER"
    ADAPTIVE = "ADAPTIVE"


class RecoveryRetryPolicy(BaseModel):
    """Configuration for autonomous recovery retries."""
    backoff_type: RecoveryBackoffType = Field(default=RecoveryBackoffType.EXPONENTIAL_JITTER)
    max_retries: int = Field(default=3, ge=0)
    initial_delay_seconds: float = Field(default=1.0, ge=0.0)
    max_delay_seconds: float = Field(default=30.0, ge=0.0)
    model_config = {"frozen": True}
