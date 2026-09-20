"""
Phase 3H.5.9: Predictive Health Intelligence Scorer
"""
from ..domain.interfaces import IPredictiveHealthScorer
from ..domain.models import (
    PredictiveArchitectureReport,
    FeatureEngineeringReport,
    AnomalyDetectionReport,
    FailurePredictionReport,
    CapacityPredictionReport,
    ProactiveRemediationReport,
    PredictionAccuracyReport,
    PredictiveIncidentReport,
    ReliabilityTwinReport,
    ChaosPredictionReport,
    PredictiveDashboardReport,
    PredictiveHealthScorecard,
    PredictiveCertificationTier,
)


class PredictiveHealthScorer(IPredictiveHealthScorer):
    def calculate_scorecard(
        self,
        arch_report: PredictiveArchitectureReport,
        feature_report: FeatureEngineeringReport,
        anomaly_report: AnomalyDetectionReport,
        prediction_report: FailurePredictionReport,
        capacity_report: CapacityPredictionReport,
        remediation_report: ProactiveRemediationReport,
        accuracy_report: PredictionAccuracyReport,
        incident_report: PredictiveIncidentReport,
        twin_report: ReliabilityTwinReport,
        chaos_report: ChaosPredictionReport,
        dashboard_report: PredictiveDashboardReport,
    ) -> PredictiveHealthScorecard:
        # 1. Prediction accuracy (25%)
        pred_accuracy_score = 100.0 if (
            accuracy_report.prediction_accuracy_valid
            and accuracy_report.accuracy_threshold_met
            and accuracy_report.metrics.precision >= 0.90
            and accuracy_report.metrics.recall >= 0.90
            and prediction_report.failure_prediction_valid
            and prediction_report.mean_confidence >= 0.80
        ) else 80.0

        # 2. Anomaly detection (20%)
        anomaly_score = 100.0 if (
            anomaly_report.anomaly_detection_valid
            and anomaly_report.statistical_detection_active
            and anomaly_report.trend_detection_active
            and anomaly_report.behavioral_detection_active
            and anomaly_report.total_anomalies_detected >= 3
        ) else 80.0

        # 3. Preventive actions (20%)
        preventive_score = 100.0 if (
            remediation_report.proactive_remediation_valid
            and remediation_report.all_actions_successful
            and remediation_report.total_preventive_actions >= 4
            and incident_report.predictive_incident_valid
            and incident_report.all_incidents_actionable
        ) else 80.0

        # 4. False alarm control (15%)
        false_alarm_score = 100.0 if (
            accuracy_report.false_alarm_rate_pct <= 10.0
            and accuracy_report.metrics.false_positive_rate <= 0.10
        ) else 80.0

        # 5. Reliability improvement (10%)
        reliability_score = 100.0 if (
            twin_report.reliability_twin_valid
            and twin_report.total_components_modeled >= 5
            and chaos_report.chaos_prediction_valid
            and chaos_report.all_chaos_predictions_passed
            and capacity_report.capacity_prediction_valid
        ) else 80.0

        # 6. Security (10%)
        security_score = 100.0 if (
            arch_report.architecture_valid
            and feature_report.feature_engineering_valid
            and dashboard_report.dashboard_valid
            and dashboard_report.all_dashboards_active
        ) else 80.0

        composite = (
            pred_accuracy_score * 0.25
            + anomaly_score * 0.20
            + preventive_score * 0.20
            + false_alarm_score * 0.15
            + reliability_score * 0.10
            + security_score * 0.10
        )

        composite = round(composite, 2)

        if composite >= 95.0:
            tier = PredictiveCertificationTier.PREDICTIVE_RELIABILITY_READY
            certified = True
        elif composite >= 90.0:
            tier = PredictiveCertificationTier.ADVANCED_AIOPS_READY
            certified = True
        elif composite >= 80.0:
            tier = PredictiveCertificationTier.IMPROVEMENT_REQUIRED
            certified = False
        else:
            tier = PredictiveCertificationTier.FAILED
            certified = False

        return PredictiveHealthScorecard(
            prediction_accuracy_score=round(pred_accuracy_score, 2),
            anomaly_detection_score=round(anomaly_score, 2),
            preventive_actions_score=round(preventive_score, 2),
            false_alarm_control_score=round(false_alarm_score, 2),
            reliability_improvement_score=round(reliability_score, 2),
            security_score=round(security_score, 2),
            composite_score=composite,
            tier=tier,
            certified_predictive_ready=certified,
        )
