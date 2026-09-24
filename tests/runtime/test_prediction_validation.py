"""
Unit and Integration Tests for Prediction Error Quantification & Residual Analysis (ASVSP Pillar 2).
"""

from app.runtime.predictions import (
    PredictionErrorEngine,
    ResidualAnalyzer,
    CalibrationDriftMonitor,
    PredictionValidator,
)


def test_prediction_error_metrics():
    engine = PredictionErrorEngine()
    preds = [0.95, 0.90, 0.85, 0.92]
    actuals = [0.94, 0.91, 0.83, 0.90]

    metrics = engine.evaluate_errors(preds, actuals)
    assert metrics.mae >= 0.0
    assert metrics.rmse >= metrics.mae
    assert metrics.coverage_probability_95 >= 0.0
    assert metrics.sample_size == 4


def test_residual_analysis():
    preds = [500.0, 520.0, 480.0, 510.0, 490.0]
    actuals = [505.0, 515.0, 485.0, 508.0, 492.0]

    residuals = ResidualAnalyzer.analyze_residuals(preds, actuals)
    assert residuals.durbin_watson >= 0.0
    assert residuals.variance >= 0.0


def test_calibration_drift_monitor():
    monitor = CalibrationDriftMonitor(num_bins=5)
    probs = [0.9, 0.8, 0.7, 0.95, 0.6]
    labels = [1, 1, 0, 1, 0]

    metrics = monitor.calculate_online_calibration(probs, labels)
    assert metrics.expected_calibration_error >= 0.0
    assert metrics.brier_score >= 0.0
    assert isinstance(metrics.is_well_calibrated, bool)


def test_prediction_validator_tolerance():
    validator = PredictionValidator(max_allowed_mae_accuracy=0.08, max_allowed_mae_latency=150.0)
    engine = PredictionErrorEngine()

    acc_metrics = engine.evaluate_errors([0.95, 0.92], [0.94, 0.91])
    lat_metrics = engine.evaluate_errors([450.0, 500.0], [460.0, 510.0])

    report = validator.validate_prediction_bounds(acc_metrics, lat_metrics)
    assert report.is_within_tolerance is True
    assert len(report.breach_reasons) == 0
