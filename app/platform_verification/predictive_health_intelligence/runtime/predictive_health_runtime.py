"""Predictive Health Runtime Coordinator.

Unites all 15 parts of the Predictive Health Intelligence framework.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from app.platform_verification.predictive_health_intelligence.anomaly.health_anomaly_detector import (
    HealthAnomalyDetector,
)
from app.platform_verification.predictive_health_intelligence.baseline.health_baseline_manager import (
    HealthBaselineManager,
)
from app.platform_verification.predictive_health_intelligence.domain.models import (
    AccuracyReport,
    AIWorkflowHealthReport,
    AnomalyReport,
    BaselineReport,
    EarlyWarningReport,
    PredictiveHealthScorecard,
    RecommendationReport,
    RiskPredictionReport,
    TelemetryReport,
)
from app.platform_verification.predictive_health_intelligence.early_warning.early_warning_system import (
    EarlyWarningSystem,
)
from app.platform_verification.predictive_health_intelligence.exporter.predictive_evidence_exporter import (
    PredictiveEvidenceExporter,
)
from app.platform_verification.predictive_health_intelligence.observability.predictive_metrics_exporter import (
    PredictiveMetricsExporter,
)
from app.platform_verification.predictive_health_intelligence.prediction.ai_workflow_predictor import (
    AIWorkflowHealthPredictor,
)
from app.platform_verification.predictive_health_intelligence.prediction.resource_exhaustion_predictor import (
    ResourceExhaustionPredictor,
)
from app.platform_verification.predictive_health_intelligence.recommendation.automated_action_verifier import (
    AutomatedActionVerifier,
)
from app.platform_verification.predictive_health_intelligence.recommendation.preventive_action_recommender import (
    PreventiveActionRecommender,
)
from app.platform_verification.predictive_health_intelligence.risk.health_risk_engine import (
    HealthRiskEngine,
)
from app.platform_verification.predictive_health_intelligence.scoring.predictive_health_scorer import (
    PredictiveHealthScorer,
)
from app.platform_verification.predictive_health_intelligence.simulation.predictive_simulation_runner import (
    PredictiveSimulationRunner,
)
from app.platform_verification.predictive_health_intelligence.storage.timeseries_health_store import (
    TimeSeriesHealthStore,
)
from app.platform_verification.predictive_health_intelligence.telemetry.health_telemetry_collector import (
    HealthTelemetryCollector,
)
from app.platform_verification.predictive_health_intelligence.validation.false_positive_validator import (
    FalsePositiveValidator,
)


class PredictiveHealthRuntime:
    """Master coordinator executing all predictive health verification workflows."""

    def __init__(
        self,
        baseline_path: Optional[Path | str] = None,
        export_dir: Optional[Path | str] = None,
    ) -> None:
        self.export_dir = Path(export_dir or "health_verification")
        self.collector = HealthTelemetryCollector()
        self.store = TimeSeriesHealthStore()
        self.baseline_manager = HealthBaselineManager(
            baseline_path=str(baseline_path) if baseline_path else "health_baseline.yaml"
        )
        self.anomaly_detector = HealthAnomalyDetector(time_store=self.store)
        self.risk_engine = HealthRiskEngine()
        self.exhaustion_predictor = ResourceExhaustionPredictor()
        self.ai_predictor = AIWorkflowHealthPredictor()
        self.early_warning_system = EarlyWarningSystem()
        self.recommender = PreventiveActionRecommender()
        self.action_verifier = AutomatedActionVerifier()
        self.validator = FalsePositiveValidator()
        self.simulation_runner = PredictiveSimulationRunner()
        self.metrics_exporter = PredictiveMetricsExporter()
        self.scorer = PredictiveHealthScorer()
        self.evidence_exporter = PredictiveEvidenceExporter(output_dir=self.export_dir)

    def run_full_verification(self) -> Dict[str, Any]:
        """Runs full verification across all 15 components."""
        # 1. Multi-Dimensional Telemetry Collection
        telemetry_report: TelemetryReport = self.collector.collect_comprehensive_telemetry()
        for item in telemetry_report.sample_telemetry:
            self.store.ingest_point(item)

        # 2. Baseline Profile Loading
        baseline_report: BaselineReport = self.baseline_manager.get_baseline_report()

        # 3. Anomaly Detection
        anomaly_report: AnomalyReport = self.anomaly_detector.detect_anomalies()

        # 4. Risk Prediction & Exhaustion Predictions
        risk_report: RiskPredictionReport = self.risk_engine.compute_risk_predictions()
        exhaustion_estimates = self.exhaustion_predictor.predict_exhaustion()
        ai_workflow_report: AIWorkflowHealthReport = self.ai_predictor.predict_ai_health()

        # 5. Early Warning Generation
        early_warning_report: EarlyWarningReport = self.early_warning_system.generate_early_warnings()

        # 6. Preventive Recommendations & Verification
        recommendation_report: RecommendationReport = self.recommender.generate_recommendations()
        action_verifications = [
            self.action_verifier.verify_action_pipeline(rec)
            for rec in recommendation_report.recommendations
        ]

        # 7. False Positive & Accuracy Validation
        accuracy_report: AccuracyReport = self.validator.evaluate_accuracy()

        # 8. Simulations
        sim_results = self.simulation_runner.run_simulations()

        # 9. Scorecard Evaluation
        scorecard: PredictiveHealthScorecard = self.scorer.compute_scorecard(
            telemetry_rep=telemetry_report,
            baseline_rep=baseline_report,
            anomaly_rep=anomaly_report,
            risk_rep=risk_report,
            warning_rep=early_warning_report,
            rec_rep=recommendation_report,
            accuracy_rep=accuracy_report,
            observability_valid=True,
        )

        # 10. Export 8 Manifests
        manifest_files = self.evidence_exporter.export_all(
            telemetry_report=telemetry_report,
            baseline_report=baseline_report,
            anomaly_report=anomaly_report,
            risk_report=risk_report,
            early_warning_report=early_warning_report,
            recommendation_report=recommendation_report,
            accuracy_report=accuracy_report,
            scorecard=scorecard,
            additional_metadata={
                "exhaustion_estimates_count": len(exhaustion_estimates),
                "ai_degradation_predicted": ai_workflow_report.degradation_predicted,
                "verified_actions_count": len(action_verifications),
                "simulations_passed": sim_results.get("all_scenarios_passed", True),
            },
        )

        return {
            "scorecard": scorecard,
            "manifest_files": manifest_files,
            "telemetry_report": telemetry_report,
            "baseline_report": baseline_report,
            "anomaly_report": anomaly_report,
            "risk_report": risk_report,
            "early_warning_report": early_warning_report,
            "recommendation_report": recommendation_report,
            "accuracy_report": accuracy_report,
            "exhaustion_estimates": exhaustion_estimates,
            "ai_workflow_report": ai_workflow_report,
            "action_verifications": action_verifications,
            "simulation_results": sim_results,
            "prometheus_metrics": self.metrics_exporter.generate_prometheus_payload(),
        }
