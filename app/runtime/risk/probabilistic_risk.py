"""
Scientific Risk Engine - Probabilistic Risk
Computes explicit joint and marginal failure probabilities across operational dimensions.
"""

from typing import Dict, Any, List
from dataclasses import dataclass, asdict
import math


@dataclass
class FailureProbabilities:
    p_timeout: float
    p_validation_failure: float
    p_ocr_failure: float
    p_retry: float
    p_memory_mismatch: float
    p_schema_violation: float
    p_worker_failure: float
    overall_failure_risk: float

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


class ProbabilisticRiskEstimator:
    """Estimates quantitative failure probabilities from runtime feature vectors."""

    @classmethod
    def estimate_probabilities(cls, normalized_features: Dict[str, float]) -> FailureProbabilities:
        # Extract features
        lat_norm = normalized_features.get("latency_p95_ms", 0.2)
        ocr_c = normalized_features.get("ocr_confidence", 0.85)
        schema_c = normalized_features.get("schema_validation_score", 1.0)
        retries = normalized_features.get("retry_count", 0.0)
        mem_sim = normalized_features.get("memory_similarity", 0.5)
        worker_rel = normalized_features.get("worker_reliability", 0.98)
        comp_flags = normalized_features.get("compliance_flags", 0.0)
        anomaly = normalized_features.get("anomaly_score", 0.05)

        # Explicit probabilistic formulas:
        # P(timeout) increases with high latency p95 and queue length
        p_timeout = min(0.95, max(0.01, 0.7 * (lat_norm ** 2) + 0.3 * anomaly))

        # P(ocr_failure) inversely relates to ocr_confidence
        p_ocr = min(0.95, max(0.01, (1.0 - ocr_c) ** 1.5))

        # P(schema_violation) inversely relates to schema validation score
        p_schema = min(0.95, max(0.01, (1.0 - schema_c) + 0.1 * comp_flags))

        # P(validation_failure) combined schema & ocr failure
        p_validation = min(0.98, max(0.01, 1.0 - (1.0 - p_ocr) * (1.0 - p_schema)))

        # P(memory_mismatch)
        p_memory = min(0.95, max(0.01, (1.0 - mem_sim) * 0.4 + 0.1 * anomaly))

        # P(worker_failure)
        p_worker = min(0.95, max(0.005, (1.0 - worker_rel) + 0.05 * retries))

        # P(retry)
        p_retry = min(0.95, max(0.01, 0.4 * p_validation + 0.3 * p_timeout + 0.3 * p_worker))

        # Overall failure risk: 1 - product of survival probabilities
        p_success_joint = (1.0 - p_timeout) * (1.0 - p_validation) * (1.0 - p_worker)
        overall_risk = min(1.0, max(0.0, 1.0 - p_success_joint))

        return FailureProbabilities(
            p_timeout=round(p_timeout, 4),
            p_validation_failure=round(p_validation, 4),
            p_ocr_failure=round(p_ocr, 4),
            p_retry=round(p_retry, 4),
            p_memory_mismatch=round(p_memory, 4),
            p_schema_violation=round(p_schema, 4),
            p_worker_failure=round(p_worker, 4),
            overall_failure_risk=round(overall_risk, 4),
        )
