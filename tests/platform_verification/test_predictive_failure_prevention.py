"""
Comprehensive Unit and Integration Tests for Phase 3H.5.9:
Predictive Health Intelligence & Proactive Failure Prevention Verification Framework.
"""
import os
import json
from app.platform_verification.predictive_failure_prevention.domain.models import (
    PredictionRiskLevel,
    SystemReliabilityState,
    RemediationApprovalLevel,
    DetectionMethod,
    PredictiveCertificationTier,
)
from app.platform_verification.predictive_failure_prevention.verifiers.predictive_architecture_verifier import (
    PredictiveArchitectureVerifier,
)
from app.platform_verification.predictive_failure_prevention.verifiers.feature_engineering_verifier import (
    FeatureEngineeringVerifier,
)
from app.platform_verification.predictive_failure_prevention.verifiers.anomaly_detection_verifier import (
    AnomalyDetectionVerifier,
)
from app.platform_verification.predictive_failure_prevention.verifiers.failure_prediction_verifier import (
    FailurePredictionVerifier,
)
from app.platform_verification.predictive_failure_prevention.verifiers.capacity_prediction_verifier import (
    CapacityPredictionVerifier,
)
from app.platform_verification.predictive_failure_prevention.verifiers.proactive_remediation_verifier import (
    ProactiveRemediationVerifier,
)
from app.platform_verification.predictive_failure_prevention.verifiers.prediction_accuracy_verifier import (
    PredictionAccuracyVerifier,
)
from app.platform_verification.predictive_failure_prevention.verifiers.predictive_incident_verifier import (
    PredictiveIncidentVerifier,
)
from app.platform_verification.predictive_failure_prevention.verifiers.reliability_twin_verifier import (
    ReliabilityTwinVerifier,
)
from app.platform_verification.predictive_failure_prevention.verifiers.chaos_prediction_verifier import (
    ChaosPredictionVerifier,
)
from app.platform_verification.predictive_failure_prevention.verifiers.predictive_dashboard_verifier import (
    PredictiveDashboardVerifier,
)
from app.platform_verification.predictive_failure_prevention.runtime.predictive_health_runtime import (
    PredictiveHealthRuntime,
)


class TestPredictiveFailurePrevention:
    """Test suite for Phase 3H.5.9: Predictive Health Intelligence & Proactive Failure Prevention."""

    def test_predictive_architecture_verifier(self):
        verifier = PredictiveArchitectureVerifier()
        report = verifier.verify_architecture()
        assert report.architecture_valid is True
        assert len(report.pipeline_stages) == 7
        assert report.total_signal_sources >= 12
        assert len(report.metric_categories) == 5
        assert len(report.application_signals) == 4
        assert len(report.dependency_signals) == 3
        assert "Telemetry Aggregation Layer" in report.pipeline_stages
        assert "Prediction Engine" in report.pipeline_stages
        assert "Preventive Action Engine" in report.pipeline_stages

    def test_feature_engineering_verifier(self):
        verifier = FeatureEngineeringVerifier()
        report = verifier.verify_feature_engineering()
        assert report.feature_engineering_valid is True
        assert report.total_features_extracted >= 12
        assert report.resource_features_count >= 3
        assert report.performance_features_count >= 3
        assert report.reliability_features_count >= 3
        assert report.ai_features_count >= 3
        categories = {f.category for f in report.features}
        assert categories == {"resource", "performance", "reliability", "ai"}

    def test_anomaly_detection_verifier(self):
        verifier = AnomalyDetectionVerifier()
        report = verifier.verify_anomaly_detection()
        assert report.anomaly_detection_valid is True
        assert report.total_anomalies_detected >= 5
        assert report.statistical_detection_active is True
        assert report.trend_detection_active is True
        assert report.behavioral_detection_active is True
        methods = {a.detection_method for a in report.anomalies}
        assert DetectionMethod.STANDARD_DEVIATION in methods
        assert DetectionMethod.TREND_ANALYSIS in methods
        assert DetectionMethod.BEHAVIORAL_ANALYSIS in methods

    def test_failure_prediction_verifier(self):
        verifier = FailurePredictionVerifier()
        report = verifier.verify_failure_predictions()
        assert report.failure_prediction_valid is True
        assert report.total_predictions >= 5
        assert report.high_risk_predictions >= 2
        assert report.mean_confidence >= 0.80
        risk_levels = {p.risk_level for p in report.predictions}
        assert PredictionRiskLevel.HIGH in risk_levels
        assert PredictionRiskLevel.CRITICAL in risk_levels
        for p in report.predictions:
            assert 0.0 <= p.probability <= 1.0
            assert 0.0 <= p.confidence <= 1.0

    def test_capacity_prediction_verifier(self):
        verifier = CapacityPredictionVerifier()
        report = verifier.verify_capacity_predictions()
        assert report.capacity_prediction_valid is True
        assert report.total_capacity_predictions >= 4
        assert report.critical_resources >= 2
        resources = {p.resource for p in report.predictions}
        assert "database_connections" in resources
        assert "worker_memory" in resources

    def test_proactive_remediation_verifier(self):
        verifier = ProactiveRemediationVerifier()
        report = verifier.verify_proactive_remediation()
        assert report.proactive_remediation_valid is True
        assert report.total_preventive_actions >= 5
        assert report.all_actions_successful is True
        assert report.automatic_actions_count >= 3
        assert report.approval_required_count >= 2
        levels = {a.approval_level for a in report.actions}
        assert RemediationApprovalLevel.SAFE_AUTOMATIC in levels
        assert RemediationApprovalLevel.APPROVAL_REQUIRED in levels

    def test_prediction_accuracy_verifier(self):
        verifier = PredictionAccuracyVerifier()
        report = verifier.verify_prediction_accuracy()
        assert report.prediction_accuracy_valid is True
        assert report.accuracy_threshold_met is True
        assert report.metrics.precision >= 0.90
        assert report.metrics.recall >= 0.90
        assert report.metrics.false_positive_rate <= 0.10
        assert report.false_alarm_rate_pct <= 10.0

    def test_predictive_incident_verifier(self):
        verifier = PredictiveIncidentVerifier()
        report = verifier.verify_predictive_incidents()
        assert report.predictive_incident_valid is True
        assert report.total_predictive_incidents >= 4
        assert report.all_incidents_actionable is True
        for inc in report.incidents:
            assert inc.incident_type == "PREDICTIVE"
            assert inc.incident_created is True
            assert 0.0 <= inc.failure_probability <= 1.0

    def test_reliability_twin_verifier(self):
        verifier = ReliabilityTwinVerifier()
        report = verifier.verify_reliability_twin()
        assert report.reliability_twin_valid is True
        assert report.total_components_modeled >= 6
        assert report.healthy_components >= 5
        states = {c.current_state for c in report.component_states}
        assert SystemReliabilityState.HEALTHY in states

    def test_chaos_prediction_verifier(self):
        verifier = ChaosPredictionVerifier()
        report = verifier.verify_chaos_predictions()
        assert report.chaos_prediction_valid is True
        assert report.total_chaos_scenarios >= 4
        assert report.all_chaos_predictions_passed is True
        assert report.mean_prediction_lead_time_seconds > 0.0
        for s in report.scenarios:
            assert s.prediction_triggered is True
            assert s.scenario_passed is True
            assert s.prediction_accuracy_pct >= 90.0

    def test_predictive_dashboard_verifier(self):
        verifier = PredictiveDashboardVerifier()
        report = verifier.verify_predictive_dashboards()
        assert report.dashboard_valid is True
        assert report.total_dashboards == 3
        assert report.all_dashboards_active is True
        names = {d.dashboard_name for d in report.dashboards}
        assert "Risk Forecast Dashboard" in names
        assert "Capacity Forecast Dashboard" in names
        assert "Prevention Dashboard" in names

    def test_predictive_health_scorer(self):
        runtime = PredictiveHealthRuntime()
        results = runtime.run_full_verification()
        scorecard = results["scorecard"]

        assert scorecard.composite_score >= 95.0
        assert scorecard.tier == PredictiveCertificationTier.PREDICTIVE_RELIABILITY_READY
        assert scorecard.certified_predictive_ready is True
        assert scorecard.prediction_accuracy_score == 100.0
        assert scorecard.anomaly_detection_score == 100.0
        assert scorecard.preventive_actions_score == 100.0
        assert scorecard.false_alarm_control_score == 100.0
        assert scorecard.reliability_improvement_score == 100.0
        assert scorecard.security_score == 100.0

    def test_full_runtime_and_export(self, tmp_path):
        out_dir = str(tmp_path / "predictive_failure_prevention_verification")
        runtime = PredictiveHealthRuntime()
        results = runtime.run_full_verification(output_dir=out_dir)

        assert results["composite_score"] >= 95.0
        assert results["certified"] is True
        assert len(results["exported_files"]) == 12

        for file_path in results["exported_files"]:
            assert os.path.exists(file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, dict)
