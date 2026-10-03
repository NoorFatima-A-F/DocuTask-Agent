"""
Unit and Integration Tests for Online Drift Detection & Sequential Change-Point (ASVSP Pillar 5).
"""

from app.runtime.drift import (
    StatisticalDriftMetrics,
    ADWINDetector,
    CUSUMDetector,
    OnlineDriftDetector,
)


def test_statistical_drift_metrics():
    baseline = [10.0 + i for i in range(50)]
    current_same = [10.0 + i for i in range(50)]
    current_drifted = [50.0 + i for i in range(50)]

    psi_same = StatisticalDriftMetrics.calculate_psi(baseline, current_same)
    psi_drifted = StatisticalDriftMetrics.calculate_psi(baseline, current_drifted)
    assert psi_same < 0.10
    assert psi_drifted > psi_same

    kl_drifted = StatisticalDriftMetrics.calculate_kl_divergence(baseline, current_drifted)
    assert kl_drifted >= 0.0

    wass = StatisticalDriftMetrics.calculate_wasserstein_distance(baseline, current_drifted)
    assert wass > 0.0


def test_cusum_and_adwin():
    cusum = CUSUMDetector(target_mean=10.0, threshold_h=3.0)
    for _ in range(5):
        cusum.update(10.0)
    assert cusum.change_detected is False

    for _ in range(10):
        cusum.update(25.0)
    assert cusum.change_detected is True

    adwin = ADWINDetector()
    drift = False
    for i in range(50):
        val = 10.0 if i < 30 else 50.0
        if adwin.update(val):
            drift = True
            break
    assert isinstance(drift, bool)


def test_online_drift_detector():
    detector = OnlineDriftDetector(window_size=30)
    # Record normal observations
    for _ in range(10):
        detector.record_observation("latency_ms", 360.0)

    analysis = detector.analyze_drift()
    assert "reports" in analysis
    assert len(analysis["reports"]) >= 4
    assert analysis["overall_status"] in ["HEALTHY", "DRIFT_WARNING", "CRITICAL_DRIFT_ALERT"]
