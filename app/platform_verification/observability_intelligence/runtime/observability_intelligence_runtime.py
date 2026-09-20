"""
Phase 3I.9: Observability Intelligence, Predictive Reliability & AIOps Maturity Runtime
Orchestrates all 13 predictive verifiers, the 6-pillar scoring engine, and the SHA-256 evidence exporter.
"""
import logging
from typing import Dict, Any

from ..verifiers.aiops_architecture_verifier import AIOpsArchitectureVerifier
from ..verifiers.data_quality_verifier import OperationalDataQualityVerifier
from ..verifiers.failure_prediction_verifier import FailurePredictionVerifier
from ..verifiers.capacity_forecasting_verifier import CapacityForecastingVerifier
from ..verifiers.behavior_baseline_verifier import BehaviorBaselineVerifier
from ..verifiers.predictive_anomaly_verifier import PredictiveAnomalyVerifier
from ..verifiers.reliability_score_verifier import ReliabilityScoreVerifier
from ..verifiers.incident_prevention_verifier import IncidentPreventionVerifier
from ..verifiers.deployment_intelligence_verifier import DeploymentIntelligenceVerifier
from ..verifiers.ai_reliability_verifier import AIReliabilityVerifier
from ..verifiers.continuous_optimization_verifier import ContinuousOptimizationVerifier
from ..verifiers.aiops_explainability_verifier import AIOpsExplainabilityVerifier
from ..verifiers.aiops_validation_verifier import AIOpsValidationVerifier
from ..scoring.predictive_reliability_scorer import PredictiveReliabilityScorer
from ..exporter.observability_intelligence_evidence_exporter import ObservabilityIntelligenceEvidenceExporter

logger = logging.getLogger(__name__)


class ObservabilityIntelligenceRuntime:
    def __init__(
        self,
        output_dir: str = "observability_intelligence_verification",
    ):
        self.output_dir = output_dir
        self.arch_verifier = AIOpsArchitectureVerifier()
        self.data_verifier = OperationalDataQualityVerifier()
        self.pred_verifier = FailurePredictionVerifier()
        self.capacity_verifier = CapacityForecastingVerifier()
        self.baseline_verifier = BehaviorBaselineVerifier()
        self.anomaly_verifier = PredictiveAnomalyVerifier()
        self.score_verifier = ReliabilityScoreVerifier()
        self.prevention_verifier = IncidentPreventionVerifier()
        self.deploy_verifier = DeploymentIntelligenceVerifier()
        self.ai_verifier = AIReliabilityVerifier()
        self.opt_verifier = ContinuousOptimizationVerifier()
        self.explain_verifier = AIOpsExplainabilityVerifier()
        self.val_verifier = AIOpsValidationVerifier()
        self.scorer = PredictiveReliabilityScorer()
        self.exporter = ObservabilityIntelligenceEvidenceExporter()

    def run_full_verification(self) -> Dict[str, Any]:
        logger.info("Starting Phase 3I.9 Observability Intelligence & Predictive Reliability Verification Suite...")

        # 1. Execute all 13 verification stages
        arch_report = self.arch_verifier.verify_aiops_architecture()
        data_report = self.data_verifier.verify_data_quality()
        pred_report = self.pred_verifier.verify_failure_prediction()
        capacity_report = self.capacity_verifier.verify_capacity_forecasting()
        baseline_report = self.baseline_verifier.verify_behavior_baselines()
        anomaly_report = self.anomaly_verifier.verify_predictive_anomalies()
        score_report = self.score_verifier.verify_reliability_score()
        prevention_report = self.prevention_verifier.verify_incident_prevention()
        deploy_report = self.deploy_verifier.verify_deployment_intelligence()
        ai_report = self.ai_verifier.verify_ai_reliability()
        opt_report = self.opt_verifier.verify_continuous_optimization()
        explain_report = self.explain_verifier.verify_aiops_explainability()
        val_report = self.val_verifier.verify_aiops_validation()

        # 2. Compute 6-pillar score and certification
        cert_report = self.scorer.calculate_certification_score(
            arch_report=arch_report,
            data_report=data_report,
            pred_report=pred_report,
            capacity_report=capacity_report,
            baseline_report=baseline_report,
            anomaly_report=anomaly_report,
            score_report=score_report,
            prevention_report=prevention_report,
            deploy_report=deploy_report,
            ai_report=ai_report,
            opt_report=opt_report,
            explain_report=explain_report,
            val_report=val_report,
        )

        # 3. Export all JSON artifacts with SHA-256 signatures to output directory
        metadata = self.exporter.export_all_reports(
            output_dir=self.output_dir,
            arch_report=arch_report,
            data_report=data_report,
            pred_report=pred_report,
            capacity_report=capacity_report,
            baseline_report=baseline_report,
            anomaly_report=anomaly_report,
            score_report=score_report,
            prevention_report=prevention_report,
            deploy_report=deploy_report,
            ai_report=ai_report,
            opt_report=opt_report,
            explain_report=explain_report,
            val_report=val_report,
            certification_report=cert_report,
        )

        return {
            "status": "SUCCESS" if cert_report.certification_granted else "FAILED",
            "certification_tier": cert_report.certification_tier.value,
            "overall_score_pct": cert_report.overall_score_pct,
            "certification_granted": cert_report.certification_granted,
            "aiops_architecture_report": arch_report.model_dump(mode="json"),
            "data_quality_report": data_report.model_dump(mode="json"),
            "prediction_report": pred_report.model_dump(mode="json"),
            "capacity_report": capacity_report.model_dump(mode="json"),
            "baseline_report": baseline_report.model_dump(mode="json"),
            "anomaly_prediction_report": anomaly_report.model_dump(mode="json"),
            "reliability_score_report": score_report.model_dump(mode="json"),
            "prevention_report": prevention_report.model_dump(mode="json"),
            "deployment_intelligence_report": deploy_report.model_dump(mode="json"),
            "ai_reliability_report": ai_report.model_dump(mode="json"),
            "optimization_report": opt_report.model_dump(mode="json"),
            "explainability_report": explain_report.model_dump(mode="json"),
            "validation_report": val_report.model_dump(mode="json"),
            "certification_report": cert_report.model_dump(mode="json"),
            "metadata": metadata,
        }
