"""
Uncertainty Estimator for Phase 13.3 (ASCE-CGP).
Decomposes uncertainty into aleatoric (data noise) and epistemic (model knowledge) components.
"""

import math
from typing import Tuple
from dataclasses import dataclass


@dataclass
class UncertaintyDecomposition:
    total_uncertainty: float
    aleatoric_uncertainty: float
    epistemic_uncertainty: float
    entropy: float
    information_gain: float


class UncertaintyEstimator:
    """
    Computes rigorous uncertainty bounds for confidence predictions.
    """

    @classmethod
    def estimate_uncertainty(
        cls,
        confidence: float,
        evidence_count: int,
        feature_variance: float = 0.005,
    ) -> Tuple[float, float, float]:
        """
        Returns (total_uncertainty, aleatoric, epistemic).
        """
        # Aleatoric: intrinsic noise in features
        aleatoric = math.sqrt(max(0.0001, feature_variance))

        # Epistemic: inversely proportional to sample size of evidence
        epistemic = 1.0 / math.sqrt(max(1, evidence_count) + 10.0)

        total_uncertainty = round(min(0.20, math.hypot(aleatoric, epistemic)), 4)
        return total_uncertainty, round(aleatoric, 4), round(epistemic, 4)

    @classmethod
    def decompose(
        cls,
        confidence_prob: float,
        document_complexity: float,
        domain_sample_count: int,
        feature_anomaly_score: float,
    ) -> UncertaintyDecomposition:
        """
        Legacy/Decomposition compatibility helper.
        """
        p = max(1e-5, min(1.0 - 1e-5, float(confidence_prob)))

        # Shannon Binary Entropy H(p) = -p*log2(p) - (1-p)*log2(1-p)
        entropy = -(p * math.log2(p) + (1.0 - p) * math.log2(1.0 - p))

        # Aleatoric uncertainty stems from visual noise, scan artifacts, complexity
        aleatoric = min(1.0, 0.6 * entropy + 0.4 * document_complexity)

        # Epistemic uncertainty stems from rare domains (low sample count) and feature anomalies
        sample_decay = math.exp(-float(domain_sample_count) / 50.0)
        epistemic = min(1.0, 0.5 * sample_decay + 0.5 * feature_anomaly_score)

        # Combined total uncertainty
        total = min(1.0, math.hypot(aleatoric, epistemic) / math.sqrt(2.0))

        # Information gain potential
        info_gain = max(0.0, 1.0 - entropy)

        return UncertaintyDecomposition(
            total_uncertainty=round(total, 4),
            aleatoric_uncertainty=round(aleatoric, 4),
            epistemic_uncertainty=round(epistemic, 4),
            entropy=round(entropy, 4),
            information_gain=round(info_gain, 4),
        )
