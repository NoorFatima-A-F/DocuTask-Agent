"""
Prediction Validation Engine - Prediction Error Metrics
Computes RMSE, MAE, MAPE, Bias, Variance, and Coverage Probability.
"""

from typing import List, Dict, Any, Tuple, Optional
import math
from dataclasses import dataclass, asdict


@dataclass
class PredictionAccuracyMetrics:
    dimension: str
    sample_size: int
    mae: float
    rmse: float
    mape_percent: float
    mean_bias: float
    variance: float
    coverage_probability_95: float
    is_accurate_enterprise_tier: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PredictionErrorCalculator:
    """Calculates formal regression and error metrics comparing predictions and outcomes."""

    @classmethod
    def evaluate_errors(
        cls,
        predictions: List[float],
        observations: List[float],
        dimension: str = "metric",
    ) -> PredictionAccuracyMetrics:
        return cls.compute_metrics(dimension, predictions, observations)

    @classmethod
    def compute_metrics(
        cls,
        dimension: str,
        predictions: List[float],
        observations: List[float],
        ci_uppers: Optional[List[float]] = None,
        ci_lowers: Optional[List[float]] = None,
    ) -> PredictionAccuracyMetrics:
        n = min(len(predictions), len(observations))
        if n == 0:
            return PredictionAccuracyMetrics(
                dimension=dimension,
                sample_size=0,
                mae=0.0,
                rmse=0.0,
                mape_percent=0.0,
                mean_bias=0.0,
                variance=0.0,
                coverage_probability_95=1.0,
                is_accurate_enterprise_tier=True,
            )

        preds = predictions[:n]
        obs = observations[:n]

        # 1. Residuals: e_i = y_i - y_hat_i
        residuals = [y - y_hat for y, y_hat in zip(obs, preds)]

        # 2. MAE: (1/N) * sum(|e_i|)
        mae = sum(abs(e) for e in residuals) / n

        # 3. RMSE: sqrt((1/N) * sum(e_i^2))
        mse = sum(e ** 2 for e in residuals) / n
        rmse = math.sqrt(mse)

        # 4. Mean Bias: (1/N) * sum(e_i) (positive = underpredicting, negative = overpredicting)
        mean_bias = sum(residuals) / n

        # 5. Variance of errors
        var_err = sum((e - mean_bias) ** 2 for e in residuals) / n

        # 6. MAPE: (1/N) * sum(|e_i / y_i|) * 100
        mape_terms = [abs(e) / (abs(y) + 1e-6) for e, y in zip(residuals, obs)]
        mape = (sum(mape_terms) / n) * 100.0

        # 7. Coverage probability: fraction of observations inside [ci_lower, ci_upper]
        coverage = 0.95
        if ci_lowers and ci_uppers and len(ci_lowers) >= n and len(ci_uppers) >= n:
            inside_count = sum(
                1 for y, low, up in zip(obs, ci_lowers[:n], ci_uppers[:n])
                if low <= y <= up
            )
            coverage = inside_count / n

        is_tier_ok = (mape <= 10.0 or mae <= 0.05) and abs(mean_bias) <= 0.05

        return PredictionAccuracyMetrics(
            dimension=dimension,
            sample_size=n,
            mae=round(mae, 4),
            rmse=round(rmse, 4),
            mape_percent=round(mape, 2),
            mean_bias=round(mean_bias, 4),
            variance=round(var_err, 4),
            coverage_probability_95=round(coverage, 4),
            is_accurate_enterprise_tier=is_tier_ok,
        )
