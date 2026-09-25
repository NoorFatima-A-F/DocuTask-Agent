"""
Compliance Checking Subsystem.
"""

from typing import List
from pydantic import BaseModel, Field


class PolicyViolation(BaseModel):
    policy_name: str
    violation_message: str
    model_config = {"frozen": True}


ComplianceViolation = PolicyViolation


class ComplianceCheck(BaseModel):
    is_compliant: bool = Field(default=True)
    violations: List[PolicyViolation] = Field(default_factory=list)
    model_config = {"frozen": True}
