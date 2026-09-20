"""
Planning Financial & Costing Models.
"""

from pydantic import BaseModel, Field


class PlanCostEstimate(BaseModel):
    """Estimated monetary cost for complete plan execution."""
    total_cost_usd: float = Field(default=0.0, ge=0.0)
    llm_cost_usd: float = Field(default=0.0, ge=0.0)
    compute_cost_usd: float = Field(default=0.0, ge=0.0)
    tool_invocation_cost_usd: float = Field(default=0.0, ge=0.0)
    model_config = {"frozen": True}


class BudgetConstraint(BaseModel):
    """Hard ceiling budget constraint for plan feasibility."""
    max_budget_usd: float = Field(default=5.0, ge=0.0)
    currency: str = Field(default="USD")
    model_config = {"frozen": True}
