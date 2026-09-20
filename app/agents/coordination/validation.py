"""
Coordination Validation Report.
Aggregates validation outcomes across coordination requests, teams, and message envelopes.
"""

from typing import List
from pydantic import BaseModel, Field


class CoordinationValidationReport(BaseModel):
    """Validation outcome report."""
    is_valid: bool = True
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}
