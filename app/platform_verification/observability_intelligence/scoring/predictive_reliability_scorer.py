"""
Phase 3I.9.15: Predictive Reliability Quality Scorer
Calculates weighted scores across the 6 enterprise predictive intelligence pillars:
1. Prediction Accuracy (25%)
2. Data Quality (15%)
3. Failure Prevention (20%)
4. Capacity Intelligence (15%)
5. Explainability (10%)
6. Optimization Capability (15%)
"""
from typing import List
from ..domain.interfaces import IPredictiveReliabilityScorer
from ..domain.models import (
    AIOpsArchitectureReport,
    OperationalDataQualityReport,
    FailurePredictionReport,
    CapacityForecastingReport,
    BehaviorBaselineReport,
    PredictiveAnomalyReport,
    ReliabilityIntelligenceReport,
    IncidentPreventionReport,
    DeploymentIntelligenceReport,
    AIReliabilityMonitoringReport,
    ContinuousOptimizationReport,
    AIOpsExplainabilityReport,
    AIOpsValidationReport,
    PredictivePillarScore,
    PredictiveCertificationReport,
    PredictiveCertificationTier,
)


class PredictiveReliabilityScorer(IPredictiveReliabilityScorer):
    def calculate_certification_score(
        self,
        arch_report: AIOpsArchitectureReport,
        data_report: OperationalDataQualityReport,
        pred_report: FailurePredictionReport,
        capacity_report: CapacityForecastingReport,
        baseline_report: BehaviorBaselineReport,
        anomaly_report: PredictiveAnomalyReport,
        score_report: ReliabilityIntelligenceReport,
        prevention_report: IncidentPreventionReport,
        deploy_report: DeploymentIntelligenceReport,
        ai_report: AIReliabilityMonitoringReport,
        opt_report: ContinuousOptimizationReport,
        explain_report: AIOpsExplainabilityReport,
        val_report: AIOpsValidationReport,
    ) -> PredictiveCertificationReport:
        pillar_scores: List[PredictivePillarScore] = []

        # Pillar 1: Prediction Accuracy (25%)
        p1_achieved = 100.0 if (
            pred_report.average_prediction_confidence >= 0.85
            and pred_report.status == "PASS"
            and anomaly_report.proactive_detection_active
            and arch_report.status == "PASS"
        ) else 85.0
        p1_weighted = round((p1_achieved * 25.0) / 100.0, 2)
        pillar_scores.append(
            PredictivePillarScore(
                pillar_name="Failure Prediction Accuracy & Predictive Anomaly Detection",
                weight_pct=25.0,
                achieved_score_pct=p1_achieved,
                weighted_score_pct=p1_weighted,
                status="PASSED" if p1_achieved >= 95.0 else "WARNING",
            )
        )

        # Pillar 2: Data Quality (15%)
        p2_achieved = 100.0 if (
            data_report.overall_quality_score_pct >= 95.0
            and data_report.status == "PASS"
        ) else 85.0
        p2_weighted = round((p2_achieved * 15.0) / 100.0, 2)
        pillar_scores.append(
            PredictivePillarScore(
                pillar_name="Operational Telemetry Data Quality & Consistency",
                weight_pct=15.0,
                achieved_score_pct=p2_achieved,
                weighted_score_pct=p2_weighted,
                status="PASSED" if p2_achieved >= 95.0 else "WARNING",
            )
        )

        # Pillar 3: Failure Prevention & Deployment Intelligence (20%)
        p3_achieved = 100.0 if (
            prevention_report.prevention_success_rate_pct >= 95.0
            and deploy_report.zero_regression_verified
            and score_report.system_health_score >= 95.0
        ) else 88.0
        p3_weighted = round((p3_achieved * 20.0) / 100.0, 2)
        pillar_scores.append(
            PredictivePillarScore(
                pillar_name="Proactive Failure Prevention & Deployment Intelligence",
                weight_pct=20.0,
                achieved_score_pct=p3_achieved,
                weighted_score_pct=p3_weighted,
                status="PASSED" if p3_achieved >= 95.0 else "WARNING",
            )
        )

        # Pillar 4: Capacity Intelligence & Dynamic Baselines (15%)
        p4_achieved = 100.0 if (
            capacity_report.headroom_guaranteed
            and capacity_report.forecast_accuracy_pct >= 95.0
            and baseline_report.adaptive_baselines_verified
        ) else 80.0
        p4_weighted = round((p4_achieved * 15.0) / 100.0, 2)
        pillar_scores.append(
            PredictivePillarScore(
                pillar_name="Multi-Horizon Capacity Forecasting & Adaptive Baselines",
                weight_pct=15.0,
                achieved_score_pct=p4_achieved,
                weighted_score_pct=p4_weighted,
                status="PASSED" if p4_achieved >= 95.0 else "WARNING",
            )
        )

        # Pillar 5: Explainability (10%)
        p5_achieved = 100.0 if (
            explain_report.all_decisions_explainable
        ) else 85.0
        p5_weighted = round((p5_achieved * 10.0) / 100.0, 2)
        pillar_scores.append(
            PredictivePillarScore(
                pillar_name="AIOps Decision Explainability & Transparency",
                weight_pct=10.0,
                achieved_score_pct=p5_achieved,
                weighted_score_pct=p5_weighted,
                status="PASSED" if p5_achieved >= 95.0 else "WARNING",
            )
        )

        # Pillar 6: Optimization Capability & Validation Testing (15%)
        p6_achieved = 100.0 if (
            opt_report.optimization_engine_active
            and ai_report.ai_pipeline_healthy
            and val_report.all_evaluations_passed
        ) else 80.0
        p6_weighted = round((p6_achieved * 15.0) / 100.0, 2)
        pillar_scores.append(
            PredictivePillarScore(
                pillar_name="Continuous Optimization, AI Health & Simulation Validation",
                weight_pct=15.0,
                achieved_score_pct=p6_achieved,
                weighted_score_pct=p6_weighted,
                status="PASSED" if p6_achieved >= 95.0 else "WARNING",
            )
        )

        overall_score = round(sum(p.weighted_score_pct for p in pillar_scores), 2)
        min_threshold = 95.0
        certification_granted = overall_score >= min_threshold

        if overall_score >= 95.0:
            tier = PredictiveCertificationTier.PREDICTIVE_RELIABILITY_READY
        elif overall_score >= 90.0:
            tier = PredictiveCertificationTier.ADVANCED_AIOPS_CAPABILITY
        elif overall_score >= 80.0:
            tier = PredictiveCertificationTier.IMPROVEMENT_REQUIRED
        else:
            tier = PredictiveCertificationTier.FAILED

        return PredictiveCertificationReport(
            report_title="Phase 3I.9 Enterprise Observability Intelligence & Predictive Reliability Certification",
            certification_tier=tier,
            overall_score_pct=overall_score,
            minimum_passing_threshold_pct=min_threshold,
            pillar_scores=pillar_scores,
            certification_granted=certification_granted,
            auditor="DocuTask Enterprise Observability Intelligence & Predictive AIOps Certification Engine",
        )
