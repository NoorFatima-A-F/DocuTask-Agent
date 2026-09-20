"""Comprehensive Unit and Integration Tests for Phase 3H.4.6 — Enterprise Alert Accuracy Verification Framework."""

import json
import os
import pytest

from app.platform_verification.alert_accuracy_verification.domain.models import (
    AlertAccuracyTier,
)
from app.platform_verification.alert_accuracy_verification.evaluators.ground_truth_evaluator import (
    GroundTruthEvaluator,
)
from app.platform_verification.alert_accuracy_verification.evaluators.true_positive_verifier import (
    TruePositiveVerifier,
)
from app.platform_verification.alert_accuracy_verification.evaluators.false_positive_verifier import (
    FalsePositiveVerifier,
)
from app.platform_verification.alert_accuracy_verification.evaluators.false_negative_verifier import (
    FalseNegativeVerifier,
)
from app.platform_verification.alert_accuracy_verification.evaluators.precision_recall_calculator import (
    PrecisionRecallCalculator,
)
from app.platform_verification.alert_accuracy_verification.evaluators.severity_accuracy_verifier import (
    SeverityAccuracyVerifier,
)
from app.platform_verification.alert_accuracy_verification.evaluators.alert_timing_verifier import (
    AlertTimingVerifier,
)
from app.platform_verification.alert_accuracy_verification.evaluators.alert_correlation_verifier import (
    AlertCorrelationVerifier,
)
from app.platform_verification.alert_accuracy_verification.evaluators.alert_noise_evaluator import (
    AlertNoiseEvaluator,
)
from app.platform_verification.alert_accuracy_verification.evaluators.anomaly_detection_verifier import (
    AnomalyDetectionVerifier,
)
from app.platform_verification.alert_accuracy_verification.evaluators.alert_recovery_verifier import (
    AlertRecoveryVerifier,
)
from app.platform_verification.alert_accuracy_verification.scoring.alert_accuracy_scorer import (
    AlertAccuracyScorer,
)
from app.platform_verification.alert_accuracy_verification.runtime.alert_accuracy_verification_runtime import (
    AlertAccuracyVerificationRuntime,
)


class TestAlertAccuracyVerification:
    """Test suite for validating Enterprise Alert Accuracy & Intelligence verification components."""

    def test_ground_truth_confusion_matrix(self):
        """3H.4.6.1: Verify confusion matrix calculation against ground truth states."""
        evaluator = GroundTruthEvaluator()
        report = evaluator.evaluate_ground_truth()
        assert report.status == "PASS"
        assert report.total_evaluations >= 100
        assert report.overall_accuracy_percentage >= 95.0
        assert report.true_positives > 90

    def test_true_positive_verification(self):
        """3H.4.6.2: Verify true positive alert triggers for real failures (PostgreSQL, Redis, Worker, Gemini)."""
        verifier = TruePositiveVerifier()
        report = verifier.verify_true_positives()
        assert report.status == "PASS"
        assert report.total_scenarios == 4
        assert report.true_positive_rate == 1.00
        for s in report.scenarios:
            assert s.passed is True
            assert s.correct_severity is True
            assert s.correct_owner is True

    def test_false_positive_control(self):
        """3H.4.6.3: Verify transient spikes and planned events do not create false alarms (< 5%)."""
        verifier = FalsePositiveVerifier()
        report = verifier.verify_false_positives()
        assert report.status == "PASS"
        assert report.false_positive_rate <= 0.05
        assert report.false_positive_control_passed is True
        for s in report.scenarios:
            assert s.alert_suppressed is True
            assert s.false_alarm_triggered is False

    def test_false_negative_prevention(self):
        """3H.4.6.4: Verify detection of silent/subtle failures (TCP socket hang, zombie worker, queue deadlock)."""
        verifier = FalseNegativeVerifier()
        report = verifier.verify_false_negatives()
        assert report.status == "PASS"
        assert report.zero_undetected_silent_failures is True
        assert report.false_negative_rate <= 0.05
        for s in report.scenarios:
            assert s.alert_generated is True

    def test_precision_and_recall_calculation(self):
        """3H.4.6.5 & 3H.4.6.6: Verify statistical precision (>= 90%) and recall (>= 95%)."""
        calculator = PrecisionRecallCalculator(tp=96, fp=2, fn=2)
        p_report = calculator.calculate_precision()
        r_report = calculator.calculate_recall()
        assert p_report.status == "PASS"
        assert p_report.precision_score >= 0.90
        assert p_report.precision_target_met is True
        assert r_report.status == "PASS"
        assert r_report.recall_score >= 0.95
        assert r_report.recall_target_met is True

    def test_severity_accuracy_verification(self):
        """3H.4.6.7: Verify severity matches true operational impact with 0 misclassifications."""
        verifier = SeverityAccuracyVerifier()
        report = verifier.verify_severity_accuracy()
        assert report.status == "PASS"
        assert report.critical_misclassifications == 0
        assert report.severity_accuracy_score == 100.0

    def test_alert_timing_and_mttd(self):
        """3H.4.6.8: Verify detection latency meets SLA (MTTD < 30s)."""
        verifier = AlertTimingVerifier()
        report = verifier.verify_timing()
        assert report.status == "PASS"
        assert report.mttd_seconds < 30.0
        assert report.detection_sla_met is True

    def test_alert_correlation_and_grouping(self):
        """3H.4.6.9: Verify cascading alerts are correlated to the root cause."""
        verifier = AlertCorrelationVerifier()
        report = verifier.verify_correlation()
        assert report.status == "PASS"
        assert report.root_causes_identified_correctly == report.cascade_scenarios_tested
        assert report.correlation_efficiency_ratio >= 0.90

    def test_alert_noise_and_fatigue(self):
        """3H.4.6.10: Verify alert fatigue metrics and duplicate suppression rate."""
        evaluator = AlertNoiseEvaluator()
        report = evaluator.evaluate_noise()
        assert report.status == "PASS"
        assert report.alerts_per_incident_ratio < 2.0
        assert report.duplicate_suppression_rate >= 0.90

    def test_anomaly_detection_verification(self):
        """3H.4.6.11: Verify dynamic ML throughput baseline anomaly detection."""
        verifier = AnomalyDetectionVerifier()
        report = verifier.verify_anomaly_detection()
        assert report.status == "PASS"
        assert report.anomaly_detected is True
        assert report.false_anomaly_rate <= 0.02
        assert report.baseline_learning_active is True

    def test_alert_recovery_and_closure(self):
        """3H.4.6.12: Verify auto-recovery resolution and incident closure."""
        verifier = AlertRecoveryVerifier()
        report = verifier.verify_recovery()
        assert report.status == "PASS"
        assert report.auto_resolved_count == report.recovery_scenarios_tested
        assert report.incident_auto_closure_verified is True

    def test_quality_scorecard_calculation(self):
        """3H.4.6.14: Verify 6-category weighted quality scorecard and certification tier."""
        runtime = AlertAccuracyVerificationRuntime()
        scorecard, _ = runtime.execute_full_verification()
        assert scorecard.overall_score >= 95.0
        assert scorecard.certification_tier == AlertAccuracyTier.ENTERPRISE_ALERT_INTELLIGENCE_CERTIFIED
        assert scorecard.passed is True
        assert scorecard.true_positive_score == 100.0
        assert scorecard.false_positive_score == 100.0

    def test_evidence_exporter_and_manifests(self, tmp_path):
        """3H.4.6.15: Verify export of all 14 JSON evidence manifests."""
        runtime = AlertAccuracyVerificationRuntime(output_dir=str(tmp_path))
        scorecard, manifests = runtime.execute_full_verification()
        assert scorecard.passed is True
        assert len(manifests) == 14

        expected_files = [
            "ground_truth_report.json",
            "true_positive_report.json",
            "false_positive_report.json",
            "false_negative_report.json",
            "precision_report.json",
            "recall_report.json",
            "severity_report.json",
            "timing_report.json",
            "correlation_report.json",
            "noise_report.json",
            "anomaly_report.json",
            "recovery_report.json",
            "certification_report.json",
            "metadata.json",
        ]

        for fname in expected_files:
            fpath = tmp_path / fname
            assert fpath.exists(), f"Missing manifest: {fname}"
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, dict)
