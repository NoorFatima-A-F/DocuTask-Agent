"""
Message Retry Policies.
"""

from pydantic import BaseModel, Field


class MessageRetryPolicy(BaseModel):
    """Retry policy for message delivery failures."""

    max_retries: int = Field(default=3, ge=0)
    initial_backoff_seconds: float = Field(default=1.0, gt=0.0)
    backoff_multiplier: float = Field(default=2.0, ge=1.0)
    model_config = {"frozen": True}
