"""
Workflow Validation Report.
Aggregates validation outcomes across workflow definitions, node structures, graph connectivity, and saga paths.
"""

from typing import List
from pydantic import BaseModel, Field


class WorkflowValidationReport(BaseModel):
    """Validation outcome report for workflow definitions and instances."""
    is_valid: bool = True
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}
