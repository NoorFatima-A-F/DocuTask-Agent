"""
Test Suite: Mathematical Confidence Formulation & Calibration Curve
Validates composite confidence derivation, 95% confidence interval propagation, and calibration metrics.
"""
import pytest
from app.runtime.mathematical_confidence.confidence_formulation import MathematicalConfidenceEngine
from app.runtime.mathematical_confidence.calibration_curve_builder import CalibrationCurveBuilder


def test_confidence_derivation_mathematical_guarantees():
    dossier = MathematicalConfidenceEngine.derive_confidence_with_proof(
        ocr_confidence=0.96,
        schema_validation=0.98,
        cross_doc_agreement=0.95,
        memory_similarity=0.92,
        multi_agent_consensus=1.0,
        historical_sample_size=200,
    )

    assert 0.0 <= dossier.derived_confidence <= 1.0
    assert len(dossier.confidence_interval_95) == 2
    ci_low, ci_high = dossier.confidence_interval_95
    assert ci_low <= dossier.derived_confidence <= ci_high
    assert dossier.total_propagated_uncertainty > 0.0
    assert dossier.is_mathematically_certified is True
    assert "ocr_confidence" in dossier.evidence_breakdown
    assert dossier.calibration_status == "WELL_CALIBRATED_NOMINAL"


def test_calibration_curve_and_ece():
    curve = CalibrationCurveBuilder.get_canonical_calibration_curve()
    
    assert curve["expected_calibration_error"] < 0.05
    assert curve["is_calibrated"] is True
    assert curve["total_calibration_trials"] > 1000
    assert len(curve["bins"]) == 5
