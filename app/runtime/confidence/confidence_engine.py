"""
Scientific Confidence Engine - Unified Engine
Computes posterior confidence, calibration, confidence intervals, uncertainty, and evidence weighting.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from app.runtime.confidence.confidence_model import ConfidenceModel
from app.runtime.confidence.confidence_calibration import PlattCalibrator
from app.runtime.confidence.confidence_interval import ConfidenceIntervalEstimator
from app.runtime.confidence.uncertainty_estimator import UncertaintyEstimator, UncertaintyDecomposition
from app.runtime.confidence.evidence_weighting import EvidenceWeighter, EvidentiaryFactor
from app.runtime.confidence.reliability_tracker import reliability_tracker
from app.runtime.confidence.confidence_validator import ConfidenceValidator


@dataclass
class ScientificConfidenceReport:
    raw_confidence: float
    calibrated_confidence: float
    ci_95_lower: float
    ci_95_upper: float
    uncertainty: UncertaintyDecomposition
    evidence_factors: List[EvidentiaryFactor]
    historical_reliability: float
    is_statistically_sound: bool
    formula_reference: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["evidence_factors"] = [asdict(f) for f in self.evidence_factors]
        d["uncertainty"] = asdict(self.uncertainty)
        return d


class ScientificConfidenceEngine:
    """Orchestrates comprehensive multi-factor confidence computation and verification."""

    def __init__(self):
        self.calibrator = PlattCalibrator()

    def evaluate(
        self,
        normalized_features: Dict[str, float],
        entity_key: str = "default_worker",
    ) -> ScientificConfidenceReport:
        # 1. Extract component signals
        ocr_c = normalized_features.get("ocr_confidence", 0.85)
        schema_c = normalized_features.get("schema_validation_score", 1.0)
        mem_c = normalized_features.get("memory_similarity", 0.5)
        hist_rel = normalized_features.get("historical_success_rate", 0.95)

        observations = {
            "ocr_engine": ocr_c,
            "schema_validation": schema_c,
            "memory_grounding": mem_c,
            "worker_reliability": normalized_features.get("worker_reliability", 0.98),
        }

        # 2. Evidence factors & Bayesian fusion
        factors = EvidenceWeighter.evaluate_factors(observations)
        lrs = [f.likelihood_ratio for f in factors]
        posterior_prob = ConfidenceModel.bayesian_fusion(prior_prob=hist_rel, likelihood_ratios=lrs)

        # 3. Platt Calibration
        calibrated_prob = self.calibrator.calibrate(posterior_prob)

        # 4. Confidence Interval
        sample_count = reliability_tracker.get_sample_size(entity_key) or 50
        ci_lower, ci_upper = ConfidenceIntervalEstimator.normal_approximation_interval(
            prob=calibrated_prob,
            sample_size=sample_count,
            confidence_level=0.95,
        )

        # 5. Uncertainty Decomposition
        doc_complexity = normalized_features.get("document_complexity", 0.5)
        anomaly_score = normalized_features.get("anomaly_score", 0.05)
        uncertainty = UncertaintyEstimator.decompose(
            confidence_prob=calibrated_prob,
            document_complexity=doc_complexity,
            domain_sample_count=sample_count,
            feature_anomaly_score=anomaly_score,
        )

        # 6. Mathematical validation
        is_valid, _ = ConfidenceValidator.validate_bounds(calibrated_prob, ci_lower, ci_upper)

        return ScientificConfidenceReport(
            raw_confidence=round(posterior_prob, 4),
            calibrated_confidence=round(calibrated_prob, 4),
            ci_95_lower=round(ci_lower, 4),
            ci_95_upper=round(ci_upper, 4),
            uncertainty=uncertainty,
            evidence_factors=factors,
            historical_reliability=round(hist_rel, 4),
            is_statistically_sound=is_valid,
            formula_reference="P(Y=1|E) = Platt(Logistic(LogOdds(Prior) + Sum(log(LR_i))))",
        )


scientific_confidence_engine = ScientificConfidenceEngine()
