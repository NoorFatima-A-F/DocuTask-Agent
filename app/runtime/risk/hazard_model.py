"""
Scientific Risk Engine - Hazard Model
Models time-to-failure and Cox proportional hazard rates across execution runtime.
"""

from typing import Dict, List, Tuple
import math


class HazardRateModel:
    """Computes instant hazard rates h(t) and survival functions S(t) = exp(-H(t))."""

    @staticmethod
    def hazard_rate(time_elapsed_ms: float, baseline_hazard: float = 0.0001, covariate_factor: float = 1.0) -> float:
        """h(t) = h_0(t) * exp(beta * x). Hazard increases exponentially with elapsed time past SLA."""
        t_sec = max(0.0, time_elapsed_ms / 1000.0)
        # Accelerated failure time model
        time_acceleration = math.exp(0.15 * max(0.0, t_sec - 5.0))
        return baseline_hazard * covariate_factor * time_acceleration

    @staticmethod
    def survival_curve(max_time_ms: float = 10000.0, steps: int = 10, covariate_factor: float = 1.0) -> List[Dict[str, float]]:
        """Generates survival curve S(t) points over execution horizon."""
        curve = []
        dt = max_time_ms / float(steps)
        cum_hazard = 0.0

        for i in range(steps + 1):
            t = i * dt
            h = HazardRateModel.hazard_rate(t, covariate_factor=covariate_factor)
            cum_hazard += h * (dt / 1000.0)
            survival = math.exp(-cum_hazard)
            curve.append({
                "time_ms": round(t, 1),
                "hazard_rate": round(h, 6),
                "survival_probability": round(max(0.0, min(1.0, survival)), 4),
            })

        return curve
