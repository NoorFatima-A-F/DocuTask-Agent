"""
Scientific Statistics - Distribution Fitter
Fits parametric probability distributions (Normal, Log-Normal, Exponential, Beta) to telemetry data.
"""

from typing import List, Dict, Any, Tuple
import math


class DistributionFitter:
    """Fits analytical continuous distributions via maximum likelihood estimation (MLE)."""

    @staticmethod
    def fit_normal(data: List[float]) -> Dict[str, float]:
        n = len(data)
        if n == 0:
            return {"mean": 0.0, "std_dev": 0.0, "log_likelihood": 0.0}

        mean = sum(data) / n
        var = sum((x - mean) ** 2 for x in data) / n
        std = math.sqrt(var) + 1e-9

        ll = sum(-0.5 * math.log(2 * math.pi * var + 1e-9) - ((x - mean) ** 2) / (2 * var + 1e-9) for x in data)

        return {
            "distribution": "Normal",
            "mean": round(mean, 4),
            "std_dev": round(std, 4),
            "log_likelihood": round(ll, 2),
            "aic": round(2 * 2 - 2 * ll, 2),
        }

    @staticmethod
    def fit_log_normal(data: List[float]) -> Dict[str, float]:
        pos_data = [math.log(x) for x in data if x > 0]
        n = len(pos_data)
        if n == 0:
            return {"mu": 0.0, "sigma": 0.0, "log_likelihood": 0.0}

        mu = sum(pos_data) / n
        var = sum((y - mu) ** 2 for y in pos_data) / n
        sigma = math.sqrt(var) + 1e-9

        return {
            "distribution": "Log-Normal",
            "mu": round(mu, 4),
            "sigma": round(sigma, 4),
            "median": round(math.exp(mu), 4),
        }
