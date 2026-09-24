"""
Scientific Confidence Engine - Confidence Model
Defines explicit Bayesian updating models for multi-sensor confidence estimation.
"""

from typing import List
import math


class ConfidenceModel:
    """Explicit Bayesian evidence fusion model combining disparate verification signals."""

    @staticmethod
    def bayesian_fusion(
        prior_prob: float,
        likelihood_ratios: List[float],
    ) -> float:
        """Computes posterior probability via Bayesian log-odds accumulation.
        log_odds_post = log_odds_prior + sum(log(LR_i))
        """
        p = max(1e-5, min(1.0 - 1e-5, float(prior_prob)))
        prior_log_odds = math.log(p / (1.0 - p))

        total_log_odds = prior_log_odds
        for lr in likelihood_ratios:
            clamped_lr = max(1e-4, min(1e4, float(lr)))
            total_log_odds += math.log(clamped_lr)

        # Convert back from log odds to probability
        # P = 1 / (1 + exp(-log_odds))
        posterior = 1.0 / (1.0 + math.exp(-total_log_odds))
        return max(0.0, min(1.0, posterior))

    @staticmethod
    def calculate_evidence_likelihood_ratio(factor_confidence: float, sensor_reliability: float = 0.95) -> float:
        """Converts observation confidence & sensor reliability into a Bayesian Likelihood Ratio (LR)."""
        # True positive rate / False positive rate approximation
        c = max(0.01, min(0.99, factor_confidence))
        rel = max(0.5, min(0.99, sensor_reliability))
        # LR = P(Evidence | True) / P(Evidence | False)
        lr = (c * rel) / ((1.0 - c) * (1.0 - rel) + 1e-6)
        return lr
