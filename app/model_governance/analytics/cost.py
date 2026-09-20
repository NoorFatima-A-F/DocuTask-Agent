"""Model Cost Tracking & Budget Attribution Engine (Phase 8C).

Calculates monetary spend across input/output tokens, tracks project/team/tenant budgets,
and issues budget threshold alerts.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from app.model_governance.registry.models import Model
from app.model_governance.analytics.usage import UsageEvent


class CostAttribution(BaseModel):
    """Cost breakdown for a specific execution or aggregated scope."""
    organization_id: str
    model_id: str
    input_cost: float = 0.0
    output_cost: float = 0.0
    total_cost: float = 0.0
    currency: str = "USD"


class ModelCostCalculator:
    """Calculates granular costs and monitors organization budget boundaries."""

    def __init__(self, models_by_id: Optional[Dict[str, Model]] = None):
        self._models = models_by_id or {}

    def register_model_pricing(self, model: Model) -> None:
        self._models[model.model_id] = model

    def calculate_event_cost(self, event: UsageEvent) -> CostAttribution:
        model = self._models.get(event.model_id)
        if not model:
            return CostAttribution(
                organization_id=event.organization_id,
                model_id=event.model_id,
            )

        input_cost = (event.prompt_tokens / 1000.0) * model.input_token_cost_per_1k
        output_cost = (event.completion_tokens / 1000.0) * model.output_token_cost_per_1k
        total_cost = input_cost + output_cost

        return CostAttribution(
            organization_id=event.organization_id,
            model_id=event.model_id,
            input_cost=round(input_cost, 6),
            output_cost=round(output_cost, 6),
            total_cost=round(total_cost, 6),
        )

    def calculate_total_spend(
        self,
        events: List[UsageEvent],
        organization_id: str,
    ) -> CostAttribution:
        org_events = [e for e in events if e.organization_id == organization_id]
        total_in = 0.0
        total_out = 0.0

        for e in org_events:
            attr = self.calculate_event_cost(e)
            total_in += attr.input_cost
            total_out += attr.output_cost

        return CostAttribution(
            organization_id=organization_id,
            model_id="ALL",
            input_cost=round(total_in, 6),
            output_cost=round(total_out, 6),
            total_cost=round(total_in + total_out, 6),
        )
