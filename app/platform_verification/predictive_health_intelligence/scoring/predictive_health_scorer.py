"""
Predictive Health Quality Scorer (Part 3H.3.4.15).
Computes weighted composite quality scorecards across the 6 core predictive health dimensions:
1. Telemetry Quality: 20%
2. Anomaly Detection: 20%
3. Prediction Accuracy: 20%
4. Early Warning Capability: 15%
5. Preventive Actions: 15%
6. Observability: 10%
"""
from typing import Dict, Any
from app.platform_verification.predictive_health_intelligence.domain.models import (
    TelemetryReport,
    BaselineReport,
    AnomalyReport,
    RiskPredictionReport,
    EarlyWarningReport,
    RecommendationReport,
    AccuracyReport,
    PredictiveHealthScorecard,
    PredictiveHealthTier,
)


class PredictiveHealthScorer:
    """
    Computes quality scorecards for enterprise predictive reliability verification.
    """

    def compute_scorecard(
        self,
        telemetry_rep: TelemetryReport,
        baseline_rep: BaselineReport,
        anomaly_rep: AnomalyReport,
        risk_rep: RiskPredictionReport,
        warning_rep: EarlyWarningReport,
        rec_rep: RecommendationReport,
        accuracy_rep: AccuracyReport,
        observability_valid: bool = True,
    ) -> PredictiveHealthScorecard:
        # 1. Telemetry Quality (20%)
        # Multi-dimensional coverage across 5 categories, schema compliance
        telem_pts = 0.0
        if telemetry_rep.schema_compliant and len(telemetry_rep.categories_covered) == 5:
            telem_pts += 50.0
        if telemetry_rep.passed and telemetry_rep.total_metrics_collected >= 10:
            telem_pts += 50.0
        telem_score = min(100.0, telem_pts)

        # 2. Anomaly Detection (20%)
        # Multi-algorithm: statistical z-score + trend slope + threshold
        anom_pts = 0.0
        if anomaly_rep.statistical_detection_active and anomaly_rep.trend_detection_active:
            anom_pts += 50.0
        if anomaly_rep.passed and anomaly_rep.total_anomalies_detected >= 3:
            anom_pts += 50.0
        anom_score = min(100.0, anom_pts)

        # 3. Prediction Accuracy (20%)
        # Precision >= 95%, Recall >= 95%, FPR < 5%
        acc_pts = 0.0
        if accuracy_rep.metrics.precision >= 0.95 and accuracy_rep.metrics.recall >= 0.95:
            acc_pts += 50.0
        if accuracy_rep.metrics.false_positive_rate <= 0.05 and accuracy_rep.passed:
            acc_pts += 50.0
        acc_score = min(100.0, acc_pts)

        # 4. Early Warning Capability (15%)
        # All 5 early warning risk categories covered with time horizons
        warn_pts = 0.0
        if warning_rep.total_warnings == 5:
            warn_pts += 50.0
        if warning_rep.passed and all(w.predicted_impact_time for w in warning_rep.warnings):
            warn_pts += 50.0
        warn_score = min(100.0, warn_pts)

        # 5. Preventive Actions (15%)
        # Actionable recommendations + closed-loop automated verification
        rec_pts = 0.0
        if rec_rep.automation_pipeline_verified and rec_rep.total_recommendations >= 4:
            rec_pts += 50.0
        if rec_rep.passed and all(r.expected_risk_reduction_pct >= 50.0 for r in rec_rep.recommendations):
            rec_pts += 50.0
        rec_score = min(100.0, rec_pts)

        # 6. Observability (10%)
        obs_score = 100.0 if observability_valid else 0.0

        # Weighted calculation
        overall = (
            (telem_score * 0.20)
            + (anom_score * 0.20)
            + (acc_score * 0.20)
            + (warn_score * 0.15)
            + (rec_score * 0.15)
            + (obs_score * 0.10)
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = PredictiveHealthTier.ENTERPRISE_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = PredictiveHealthTier.PRODUCTION_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 80.0:
            tier = PredictiveHealthTier.NEEDS_IMPROVEMENT
            verdict = "REJECTED"
            passed = False
        else:
            tier = PredictiveHealthTier.FAILED
            verdict = "REJECTED"
            passed = False

        return PredictiveHealthScorecard(
            telemetry_quality_score=round(telem_score, 2),
            anomaly_detection_score=round(anom_score, 2),
            prediction_accuracy_score=round(acc_score, 2),
            early_warning_score=round(warn_score, 2),
            preventive_actions_score=round(rec_score, 2),
            observability_score=round(obs_score, 2),
            overall_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
            details={
                "weights": {
                    "telemetry_quality": 0.20,
                    "anomaly_detection": 0.20,
                    "prediction_accuracy": 0.20,
                    "early_warning": 0.15,
                    "preventive_actions": 0.15,
                    "observability": 0.10,
                },
                "minimum_required_for_enterprise": 95.0,
            },
        )
