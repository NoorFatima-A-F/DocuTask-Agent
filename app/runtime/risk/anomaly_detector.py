"""
Scientific Risk Engine - Statistical Anomaly Detector
Detects out-of-distribution runtime feature vectors using Mahalanobis distance and robust Z-bounds.
"""

from typing import Dict, List, Tuple
import math


class StatisticalAnomalyDetector:
    """Computes multidimensional outlier and novelty scores for incoming mission requests."""

    def __init__(self):
        # Baseline reference means and standard deviations
        self.reference_stats: Dict[str, Tuple[float, float]] = {
            "latency_p95_ms": (0.20, 0.10),
            "ocr_confidence": (0.88, 0.08),
            "document_complexity": (0.45, 0.15),
            "api_cost_usd": (0.15, 0.08),
            "token_count": (0.25, 0.12),
        }

    def compute_anomaly_score(self, normalized_features: Dict[str, float]) -> float:
        """Computes quadratic Euclidean-Mahalanobis normalized distance from typical profile."""
        total_sq_z = 0.0
        dims = 0

        for key, (mean, std) in self.reference_stats.items():
            if key in normalized_features:
                val = normalized_features[key]
                z = (val - mean) / (std + 1e-6)
                total_sq_z += z ** 2
                dims += 1

        if dims == 0:
            return 0.0

        # Normalized anomaly index mapped to [0, 1]
        chi_val = math.sqrt(total_sq_z / dims)
        # Sigmoid transform around chi_val threshold of 2.0 (2 sigma)
        anomaly_score = 1.0 / (1.0 + math.exp(-2.0 * (chi_val - 2.0)))
        return round(max(0.0, min(1.0, anomaly_score)), 4)
