"""
Economic Engine for Phase 13.6 (ARIA-EOP).
Coordinates comprehensive economic assessment across cost modeling, value estimation, and ROI calculations.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from app.runtime.optimization.economics.cost_model import CostModel, UnitCostBreakdown
from app.runtime.optimization.economics.value_estimator import ValueEstimator, ValueEstimation
from app.runtime.optimization.economics.roi_engine import ROIEngine, ROIMetrics
from app.runtime.optimization.economics.business_priority import BusinessPriority


class FullEconomicProfile(BaseModel):
    cost_breakdown: UnitCostBreakdown
    value_estimation: ValueEstimation
    roi_metrics: ROIMetrics
    priority_tier: str = "BALANCED_STANDARD"
    energy_joules: float = 14.2


class EconomicEngine:
    """
    Coordinates enterprise financial assessment for mission executions.
    """

    @classmethod
    def evaluate_economics(
        cls,
        model_name: str = "gemini-1.5-flash",
        input_tokens: int = 3500,
        output_tokens: int = 650,
        pages: int = 4,
        confidence: float = 0.965,
        priority_tier: str = "BALANCED_STANDARD",
    ) -> FullEconomicProfile:
        costs = CostModel.calculate_cost(model_name, input_tokens, output_tokens, pages)
        val = ValueEstimator.estimate(confidence, pages, costs.total_cost_usd)
        roi = ROIEngine.calculate_roi(costs.total_cost_usd, val.gross_business_value_usd, confidence)

        return FullEconomicProfile(
            cost_breakdown=costs,
            value_estimation=val,
            roi_metrics=roi,
            priority_tier=priority_tier,
            energy_joules=round(pages * 3.55, 2),
        )


economic_engine = EconomicEngine()
