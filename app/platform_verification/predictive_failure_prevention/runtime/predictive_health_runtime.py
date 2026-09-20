"""
Phase 3H.5.9: Predictive Health Intelligence Runtime Orchestrator
"""
from typing import Dict, Any, List
from ..verifiers import (
    PredictiveArchitectureVerifier,
    FeatureEngineeringVerifier,
    AnomalyDetectionVerifier,
    FailurePredictionVerifier,
    CapacityPredictionVerifier,
    ProactiveRemediationVerifier,
    PredictionAccuracyVerifier,
    PredictiveIncidentVerifier,
    ReliabilityTwinVerifier,
    ChaosPredictionVerifier,
    PredictiveDashboardVerifier,
)
from ..scoring.predictive_health_scorer import PredictiveHealthScorer
from ..exporter.predictive_health_exporter import PredictiveHealthExporter


class PredictiveHealthRuntime:
    def __init__(self):
        self.arch_verifier = PredictiveArchitectureVerifier()
        self.feature_verifier = FeatureEngineeringVerifier()
        self.anomaly_verifier = AnomalyDetectionVerifier()
        self.prediction_verifier = FailurePredictionVerifier()
        self.capacity_verifier = CapacityPredictionVerifier()
        self.remediation_verifier = ProactiveRemediationVerifier()
        self.accuracy_verifier = PredictionAccuracyVerifier()
        self.incident_verifier = PredictiveIncidentVerifier()
        self.twin_verifier = ReliabilityTwinVerifier()
        self.chaos_verifier = ChaosPredictionVerifier()
        self.dashboard_verifier = PredictiveDashboardVerifier()
        self.scorer = PredictiveHealthScorer()
        self.exporter = PredictiveHealthExporter()

    def run_full_verification(
        self, output_dir: str = "predictive_failure_prevention_verification"
    ) -> Dict[str, Any]:
        arch_report = self.arch_verifier.verify_architecture()
        feature_report = self.feature_verifier.verify_feature_engineering()
        anomaly_report = self.anomaly_verifier.verify_anomaly_detection()
        prediction_report = self.prediction_verifier.verify_failure_predictions()
        capacity_report = self.capacity_verifier.verify_capacity_predictions()
        remediation_report = self.remediation_verifier.verify_proactive_remediation()
        accuracy_report = self.accuracy_verifier.verify_prediction_accuracy()
        incident_report = self.incident_verifier.verify_predictive_incidents()
        twin_report = self.twin_verifier.verify_reliability_twin()
        chaos_report = self.chaos_verifier.verify_chaos_predictions()
        dashboard_report = self.dashboard_verifier.verify_predictive_dashboards()

        scorecard = self.scorer.calculate_scorecard(
            arch_report=arch_report,
            feature_report=feature_report,
            anomaly_report=anomaly_report,
            prediction_report=prediction_report,
            capacity_report=capacity_report,
            remediation_report=remediation_report,
            accuracy_report=accuracy_report,
            incident_report=incident_report,
            twin_report=twin_report,
            chaos_report=chaos_report,
            dashboard_report=dashboard_report,
        )

        exported_files = self.exporter.export_evidence_manifests(
            output_dir=output_dir,
            arch_report=arch_report,
            feature_report=feature_report,
            anomaly_report=anomaly_report,
            prediction_report=prediction_report,
            capacity_report=capacity_report,
            remediation_report=remediation_report,
            accuracy_report=accuracy_report,
            incident_report=incident_report,
            twin_report=twin_report,
            chaos_report=chaos_report,
            dashboard_report=dashboard_report,
            scorecard=scorecard,
        )

        return {
            "scorecard": scorecard,
            "arch_report": arch_report,
            "feature_report": feature_report,
            "anomaly_report": anomaly_report,
            "prediction_report": prediction_report,
            "capacity_report": capacity_report,
            "remediation_report": remediation_report,
            "accuracy_report": accuracy_report,
            "incident_report": incident_report,
            "twin_report": twin_report,
            "chaos_report": chaos_report,
            "dashboard_report": dashboard_report,
            "exported_files": exported_files,
            "composite_score": scorecard.composite_score,
            "tier": scorecard.tier.value,
            "certified": scorecard.certified_predictive_ready,
        }
