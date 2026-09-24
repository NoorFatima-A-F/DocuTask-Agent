"""
Unit & Determinism Tests for Scientific Confidence Engine (QDIOP / SDIOP).
"""

from app.runtime.confidence import (
    ConfidenceModel,
    ConfidenceIntervalEstimator,
    UncertaintyEstimator,
    scientific_confidence_engine,
)


def test_bayesian_evidence_fusion_monotonicity():
    prior = 0.5
    # Strong positive evidence increases posterior
    post_high = ConfidenceModel.bayesian_fusion(prior, [10.0, 5.0])
    # Weak negative evidence decreases posterior
    post_low = ConfidenceModel.bayesian_fusion(prior, [0.1, 0.2])

    assert post_high > prior
    assert post_low < prior
    assert 0.0 <= post_high <= 1.0
    assert 0.0 <= post_low <= 1.0


def test_confidence_interval_wilson_bounds():
    ci_lower, ci_upper = ConfidenceIntervalEstimator.wilson_score_interval(successes=95, total=100)
    assert 0.85 <= ci_lower <= 0.95
    assert 0.95 <= ci_upper <= 1.0
    assert ci_lower < ci_upper


def test_uncertainty_decomposition():
    decomp = UncertaintyEstimator.decompose(
        confidence_prob=0.95,
        document_complexity=0.4,
        domain_sample_count=100,
        feature_anomaly_score=0.02,
    )
    assert 0.0 <= decomp.total_uncertainty <= 1.0
    assert 0.0 <= decomp.aleatoric_uncertainty <= 1.0
    assert 0.0 <= decomp.epistemic_uncertainty <= 1.0
    assert decomp.entropy >= 0.0


def test_confidence_engine_determinism():
    features = {
        "ocr_confidence": 0.94,
        "schema_validation_score": 1.0,
        "memory_similarity": 0.85,
        "historical_success_rate": 0.98,
        "worker_reliability": 0.99,
        "document_complexity": 0.35,
        "anomaly_score": 0.02,
    }
    report1 = scientific_confidence_engine.evaluate(features)
    report2 = scientific_confidence_engine.evaluate(features)

    assert report1.calibrated_confidence == report2.calibrated_confidence
    assert report1.ci_95_lower == report2.ci_95_lower
    assert report1.ci_95_upper == report2.ci_95_upper
    assert report1.is_statistically_sound
