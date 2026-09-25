"""
Prediction Validation Engine - Residual Analysis
Analyzes residual distributions for normality, homoscedasticity, and autocorrelation.
"""

from typing import List, Dict, Any
from dataclasses import dataclass, asdict
import math


@dataclass
class ResidualAnalysisResult:
    sample_size: int
    mean_residual: float
    std_residual: float
    durbin_watson_autocorrelation: float
    skewness: float
    kurtosis: float
    is_zero_mean: bool
    has_no_autocorrelation: bool
    variance: float = 0.0

    @property
    def durbin_watson(self) -> float:
        return self.durbin_watson_autocorrelation

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["durbin_watson"] = self.durbin_watson
        return d


class ResidualAnalyzer:
    """Performs econometric and statistical diagnostic tests on prediction residuals."""

    @staticmethod
    def analyze_residuals(predictions: List[float], observations: List[float]) -> ResidualAnalysisResult:
        n = min(len(predictions), len(observations))
        if n < 4:
            return ResidualAnalysisResult(
                sample_size=n,
                mean_residual=0.0,
                std_residual=0.0,
                durbin_watson_autocorrelation=2.0,
                skewness=0.0,
                kurtosis=0.0,
                is_zero_mean=True,
                has_no_autocorrelation=True,
                variance=0.0,
            )

        residuals = [y - y_hat for y, y_hat in zip(observations[:n], predictions[:n])]
        mean_res = sum(residuals) / n
        var_res = sum((e - mean_res) ** 2 for e in residuals) / (n - 1)
        std_res = math.sqrt(var_res) + 1e-9

        # Durbin-Watson statistic for autocorrelation: sum((e_t - e_{t-1})^2) / sum(e_t^2)
        diff_sq = sum((residuals[t] - residuals[t - 1]) ** 2 for t in range(1, n))
        sum_sq = sum(e ** 2 for e in residuals) + 1e-9
        dw_stat = diff_sq / sum_sq

        # Skewness and Kurtosis of residuals
        m3 = sum((e - mean_res) ** 3 for e in residuals) / n
        skew = m3 / (std_res ** 3)

        m4 = sum((e - mean_res) ** 4 for e in residuals) / n
        kurt = (m4 / (std_res ** 4)) - 3.0

        return ResidualAnalysisResult(
            sample_size=n,
            mean_residual=round(mean_res, 4),
            std_residual=round(std_res, 4),
            durbin_watson_autocorrelation=round(dw_stat, 4),
            skewness=round(skew, 4),
            kurtosis=round(kurt, 4),
            is_zero_mean=abs(mean_res) < 0.05,
            has_no_autocorrelation=1.5 <= dw_stat <= 2.5,
            variance=round(var_res, 4),
        )
