"""
Pytest Suite for Phase 13.3 Scientific Confidence Engine & Governance Platform (ASCE-CGP).
Tests deterministic computation, calibration, uncertainty, lineage, and governance policies.
"""

from app.runtime.confidence.models.confidence_dimensions import ConfidenceStatus
from app.runtime.confidence.features.feature_registry import FeatureRegistry
from app.runtime.confidence.features.feature_validator import FeatureValidator
from app.runtime.confidence.formulas.formula_executor import FormulaExecutor
from app.runtime.confidence.formulas.formula_validator import FormulaValidator
from app.runtime.confidence.uncertainty.uncertainty_estimator import UncertaintyEstimator
from app.runtime.confidence.uncertainty.confidence_interval import ConfidenceIntervalEngine
from app.runtime.confidence.calibration.temperature_scaling import TemperatureScalingCalibrator
from app.runtime.confidence.calibration.isotonic_calibration import IsotonicCalibrator
from app.runtime.confidence.calibration.calibration_monitor import CalibrationMonitor
from app.runtime.confidence.governance.governance_policy import ConfidenceGovernancePolicy
from app.runtime.confidence.lineage.confidence_lineage import ConfidenceLineageEngine
from app.runtime.confidence.validation.confidence_validation import ConfidenceStatisticalValidator
from app.runtime.confidence.validation.distribution_analysis import DistributionAnalysisService
from app.runtime.confidence.validation.stability_analysis import StabilityAnalysisEngine
from app.runtime.confidence.api.confidence_api_service import ConfidenceAPIService


def test_feature_registry_and_validation():
    FeatureRegistry.initialize_defaults()
    features = FeatureRegistry.list_all()
    assert len(features) >= 8

    valid_vec = {"ocr_mean_confidence": 0.99, "extraction_schema_completeness": 1.0}
    is_valid, errors = FeatureValidator.validate_features(valid_vec)
    assert is_valid
    assert len(errors) == 0

    invalid_vec = {"ocr_mean_confidence": 1.5}
    is_valid, errors = FeatureValidator.validate_features(invalid_vec)
    assert not is_valid
    assert "ocr_mean_confidence" in errors


def test_formula_execution_and_monotonicity():
    features = {"ocr_mean_confidence": 0.95, "validation_constraint_satisfaction": 1.0}
    weights = {"ocr_mean_confidence": 0.4, "validation_constraint_satisfaction": 0.6}

    score, contribs = FormulaExecutor.execute_weighted_sum(features, weights)
    assert 0.0 <= score <= 1.0
    assert len(contribs) == 2

    improved_features = {"ocr_mean_confidence": 0.99, "validation_constraint_satisfaction": 1.0}
    improved_score, _ = FormulaExecutor.execute_weighted_sum(improved_features, weights)
    assert FormulaValidator.validate_monotonicity(score, improved_score)


def test_uncertainty_and_confidence_intervals():
    confidence = 0.98
    uncertainty, aleatoric, epistemic = UncertaintyEstimator.estimate_uncertainty(confidence, evidence_count=20)

    assert 0.0 < uncertainty < 0.20
    assert aleatoric > 0
    assert epistemic > 0

    lower, upper = ConfidenceIntervalEngine.compute_interval(confidence, uncertainty, level=0.95)
    assert 0.0 <= lower <= confidence <= upper <= 1.0


def test_calibration_and_reliability_metrics():
    calibrated_temp = TemperatureScalingCalibrator.calibrate(0.95, temperature=1.05)
    assert 0.80 <= calibrated_temp <= 1.0

    calibrated_iso = IsotonicCalibrator.calibrate(0.95)
    assert 0.80 <= calibrated_iso <= 1.0

    cal_metrics = CalibrationMonitor.compute_metrics()
    assert cal_metrics.expected_calibration_error < 0.05
    assert cal_metrics.maximum_calibration_error < 0.10
    assert cal_metrics.brier_score < 0.05
    assert len(cal_metrics.reliability_bins) == 10


def test_governance_policy_and_lineage():
    status, reason = ConfidenceGovernancePolicy.evaluate_governance(0.98, evidence_present=True, truth_hash_valid=True)
    assert status == ConfidenceStatus.VERIFIED

    status_rej, _ = ConfidenceGovernancePolicy.evaluate_governance(0.98, evidence_present=False, truth_hash_valid=True)
    assert status_rej == ConfidenceStatus.REJECTED

    record = ConfidenceLineageEngine.record_lineage(
        mission_id="test-m01",
        dimension="OCR",
        score=0.99,
        uncertainty=0.015,
        evidence_signals={"tokens": 4500},
        features={"ocr_mean_confidence": 0.99},
        formula_version="v1.3.0",
        truth_ledger_hash="hash-verified-01",
        replay_offset=1,
    )
    assert record.evidence_snapshot_hash
    assert record.feature_vector_hash


def test_statistical_validation_and_stability():
    is_valid, msg = ConfidenceStatisticalValidator.validate_confidence_consistency(0.98, evidence_count=10, invariant_failures=0)
    assert is_valid

    is_invalid, msg = ConfidenceStatisticalValidator.validate_confidence_consistency(0.995, evidence_count=0, invariant_failures=0)
    assert not is_invalid

    dist = DistributionAnalysisService.analyze_distribution([0.98, 0.99, 0.97, 0.985, 0.992])
    assert dist["mean"] > 0.95

    stab = StabilityAnalysisEngine.compute_stability([0.98, 0.985, 0.99, 0.988])
    assert stab["status"] == "STABLE"


def test_confidence_api_service():
    service = ConfidenceAPIService.get_instance("mission-test-conf")
    report = service.compute_mission_confidence()

    assert report.overall_score >= 0.85
    assert len(report.dimensions) >= 12
    assert report.is_governance_approved
    assert report.calibration_ece < 0.05

    explanation = service.get_explanation("OVERALL")
    assert "waterfall_steps" in explanation
    assert len(explanation["waterfall_steps"]) > 0
