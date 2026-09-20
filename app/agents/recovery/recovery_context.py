"""
Recovery Context Details.
"""

from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class RecoveryContextDetails(BaseModel):
    """Execution context and constraints around the recovery attempt."""
    max_recovery_attempts: int = Field(default=3, ge=1)
    timeout_seconds: float = Field(default=300.0, gt=0.0)
    allow_human_escalation: bool = Field(default=True)
    allow_rollback: bool = Field(default=True)
    custom_parameters: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}
