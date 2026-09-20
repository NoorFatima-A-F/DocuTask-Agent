"""
Bayesian Evidence Fusion and Confidence Engine Test Suite.
Verifies calibrated log-odds fusion, sample size attenuation, likelihood ratios, and zero-fabrication sentinels.
"""

import pytest
from app.runtime.metrics.confidence import (
    BayesianConfidenceEngine,
    EvidenceSignal,
    _logit,
    _sigmoid,
)


def test_sigmoid_logit_inverses():
    for p in [0.05, 0.25, 0.5, 0.75, 0.95]:
        val = _sigmoid(_logit(p))
        assert abs(val - p) < 1e-4


def test_bayesian_evidence_fusion_single_strong_signal():
    signals = [
        EvidenceSignal(
            source_name="OCR_Validation",
            category="OCR",
            observed_score=0.98,
            sample_size=100,
            reliability_coefficient=0.95,
            description="Character recognition high confidence",
        )
    ]
    result = BayesianConfidenceEngine.fuse_evidence(signals, prior=0.50)
    assert result.posterior_confidence > 0.50
    assert result.log_odds_delta > 0.0
    assert result.sample_size_total == 100
    assert not result.is_sentinel_active
    assert result.confidence_interval_95[0] <= result.posterior_confidence <= result.confidence_interval_95[1]


def test_bayesian_evidence_fusion_multi_source():
    signals = [
        EvidenceSignal("OCR", "OCR", 0.95, 50, 0.90, "OCR clean"),
        EvidenceSignal("Schema", "SCHEMA", 0.99, 80, 0.98, "Schema exact"),
        EvidenceSignal("Memory", "MEMORY", 0.92, 30, 0.85, "Memory matched"),
    ]
    result = BayesianConfidenceEngine.fuse_evidence(signals, prior=0.50)
    assert result.posterior_confidence > 0.90
    assert len(result.signals) == 3
    assert "OCR" in result.signal_weights
    assert "Schema" in result.signal_weights


def test_bayesian_confidence_sentinel_handling():
    signals = [
        EvidenceSignal(
            source_name="Offline_Dataset",
            category="VALIDATION",
            observed_score=0.0,
            sample_size=0,
            reliability_coefficient=0.9,
            description="Partition offline",
            sentinel_state="DATASET_UNAVAILABLE",
        )
    ]
    result = BayesianConfidenceEngine.fuse_evidence(signals, prior=0.50)
    assert result.is_sentinel_active is True
    assert result.posterior_confidence == 0.0
    assert "DATASET_UNAVAILABLE" in result.sentinel_reason
