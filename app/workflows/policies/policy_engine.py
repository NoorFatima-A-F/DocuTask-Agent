"""
Enterprise Workflow Policy Engine.
Enforces organizational policies on cost limits, security boundaries, AI model usage, and data residency.
"""

from typing import Any, Dict, List, Optional
from ..domain.models import WorkflowDefinition
from ..domain.exceptions import WorkflowValidationException


class WorkflowPolicyEngine:
    """Evaluates and enforces enterprise governance policies on workflow definitions."""

    def __init__(self):
        self.max_cost_limit_cents: int = 5000  # $50 max cost per single execution
        self.allowed_ai_models: set = {"gemini-1.5-flash", "gemini-1.5-pro", "gpt-4o", "claude-3.5-sonnet"}

    def validate_policy_compliance(self, definition: WorkflowDefinition) -> None:
        """Validate workflow against governance policy constraints."""
        cost_limit = definition.policies.get("max_cost_cents", 0)
        if cost_limit > self.max_cost_limit_cents:
            raise WorkflowValidationException(
                f"Workflow declared cost limit ({cost_limit}c) exceeds organization cap ({self.max_cost_limit_cents}c)"
            )
