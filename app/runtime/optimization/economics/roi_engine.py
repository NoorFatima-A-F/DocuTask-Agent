"""
ROI Engine for Phase 13.6 (ARIA-EOP).
Calculates expected Return on Investment, Marginal Value, Cost per Confidence Point, and Cost per Minute Saved.
"""

from pydantic import BaseModel


class ROIMetrics(BaseModel):
    expected_roi_ratio: float = 54.2
    marginal_value_usd: float = 16.49
    cost_per_confidence_point_usd: float = 0.000031
    cost_per_minute_saved_usd: float = 0.0012
    efficiency_multiple: float = 14.8


class ROIEngine:
    """
    Computes financial and computational return metrics.
    """

    @classmethod
    def calculate_roi(
        cls,
        total_cost_usd: float,
        gross_value_usd: float,
        confidence: float,
        time_saved_sec: float = 120.0,
    ) -> ROIMetrics:
        cost = max(total_cost_usd, 0.0001)
        roi = round((gross_value_usd - cost) / cost, 2)
        cost_per_conf = round(cost / max(confidence * 100.0, 1.0), 6)
        cost_per_min = round(cost / max(time_saved_sec / 60.0, 0.1), 4)

        return ROIMetrics(
            expected_roi_ratio=roi,
            marginal_value_usd=round(gross_value_usd - cost, 2),
            cost_per_confidence_point_usd=cost_per_conf,
            cost_per_minute_saved_usd=cost_per_min,
            efficiency_multiple=round(gross_value_usd / cost, 1),
        )
