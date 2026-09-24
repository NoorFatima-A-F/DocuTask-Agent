"""
Unit Tests for Scientific Confidence Calibration (QDIOP / SDIOP).
Tests Platt scaling, reliability diagrams, ECE, MCE, and Brier scoring.
"""

from app.runtime.calibration import (
    CalibrationStatistics,
    scientific_calibration_engine,
)
from app.runtime.confidence.confidence_calibration import PlattCalibrator


def test_platt_calibrator_logistic_bounds():
    calibrator = PlattCalibrator()
    for raw in [0.01, 0.1, 0.5, 0.9, 0.99]:
        cal = calibrator.calibrate(raw)
        assert 0.0 <= cal <= 1.0


def test_calibration_statistics_metrics():
    # Perfectly calibrated synthetic data
    preds = [0.1, 0.1, 0.5, 0.5, 0.9, 0.9]
    labels = [0, 0, 1, 0, 1, 1]
    metrics = CalibrationStatistics.compute_metrics(preds, labels, num_bins=5)

    assert "ece" in metrics
    assert "mce" in metrics
    assert "brier_score" in metrics
    assert metrics["ece"] >= 0.0
    assert metrics["brier_score"] >= 0.0


def test_scientific_calibration_engine_lab():
    lab_data = scientific_calibration_engine.evaluate_calibration(num_bins=10)
    assert lab_data["sample_size"] > 0
    assert len(lab_data["bins"]) == 10
    assert lab_data["is_calibrated"]
    assert lab_data["metrics"]["ece"] < 0.08
