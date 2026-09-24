"""
AOIS-HROP Phase 13.7 - Health Forecast Engine
Predicts future health degradation and time-to-degradation using slope extrapolation.
"""

from dataclasses import dataclass
from typing import Optional
from app.runtime.operations.health.health_trend import HealthTrendAnalyzer


@dataclass
class HealthForecastResult:
    predicted_score_in_1h: float
    predicted_score_in_24h: float
    risk_of_sla_breach_pct: float
    time_to_degradation_sec: Optional[float]
    recommended_proactive_action: str


class HealthForecastEngine:
    """
    Forecasting health trajectories to preempt outages before SLA impact.
    """

    def __init__(self, trend_analyzer: HealthTrendAnalyzer):
        self.trend_analyzer = trend_analyzer

    def generate_forecast(self, current_score: float) -> HealthForecastResult:
        slope = self.trend_analyzer.calculate_trend_slope()
        self.trend_analyzer.calculate_ema()

        # Extrapolate over intervals
        pred_1h = max(0.0, min(100.0, current_score + (slope * 6.0)))
        pred_24h = max(0.0, min(100.0, current_score + (slope * 144.0)))

        # Time to breach threshold (e.g. 70.0)
        time_to_breach: Optional[float] = None
        if slope < -0.01 and current_score > 70.0:
            steps = (current_score - 70.0) / abs(slope)
            time_to_breach = round(steps * 60.0, 1)

        sla_risk = 0.0
        if pred_24h < 80.0:
            sla_risk = round(min(100.0, (80.0 - pred_24h) * 2.5), 1)

        if sla_risk > 50.0:
            action = "TRIGGER_AUTONOMOUS_PREEMPTIVE_SCALING_AND_REPAIR"
        elif sla_risk > 20.0:
            action = "SCHEDULE_SUB_COMPONENT_GARBAGE_COLLECTION"
        else:
            action = "MAINTAIN_STANDARD_CADENCE"

        return HealthForecastResult(
            predicted_score_in_1h=round(pred_1h, 2),
            predicted_score_in_24h=round(pred_24h, 2),
            risk_of_sla_breach_pct=sla_risk,
            time_to_degradation_sec=time_to_breach,
            recommended_proactive_action=action,
        )
