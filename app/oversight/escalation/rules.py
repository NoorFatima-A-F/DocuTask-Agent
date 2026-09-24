"""Escalation Hierarchy Levels and Evaluation Rules."""

from enum import Enum
from typing import Dict, Any, List
from pydantic import BaseModel, Field
import uuid


class EscalationLevel(int, Enum):
    NONE = 0
    LEVEL_1_TEAM_LEAD = 1
    LEVEL_2_DEPARTMENT_HEAD = 2
    LEVEL_3_EXECUTIVE = 3


class EscalationRule(BaseModel):
    """Configuration for when and how to escalate stalled or high-risk review requests."""
    rule_id: str = Field(default_factory=lambda: f"esc_rule_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "*"
    name: str
    target_level: EscalationLevel
    timeout_seconds: int = 3600  # Default 1 hour
    target_roles: List[str] = Field(default_factory=list)
    auto_escalate: bool = True
    priority_bump: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
