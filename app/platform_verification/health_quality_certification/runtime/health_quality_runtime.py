"""
Phase 3H.5.11: Health Quality & Certification Runtime Orchestrator
"""
from typing import Dict, Any, Optional

from ..evaluators import (
    HealthQualityEvaluator,
    SREReliabilityEngine,
    RegressionDetector,
    DeploymentReadinessGate,
)
from ..scoring import HealthQualityScorer
from ..exporter import HealthQualityExporter
from ..domain.models import HealthQualityScorecard


class HealthQualityRuntime:
    """
    Main runtime orchestrator for executing Phase 3H.5.11:
    - Collects evidence across 8 dimensions
    - Computes SRE reliability metrics
    - Evaluates regression against historical baseline
    - Runs production readiness deployment gatekeeper
    - Computes master certification scorecard
    - Exports standardized evidence artifacts with cryptographic SHA-256 hashes
    """

    def __init__(
        self,
        output_dir: str = "health_quality_certification",
        evaluator: Optional[HealthQualityEvaluator] = None,
        sre_engine: Optional[SREReliabilityEngine] = None,
        regression_detector: Optional[RegressionDetector] = None,
        gatekeeper: Optional[DeploymentReadinessGate] = None,
        scorer: Optional[HealthQualityScorer] = None,
        exporter: Optional[HealthQualityExporter] = None,
    ):
        self.output_dir = output_dir
        self.evaluator = evaluator or HealthQualityEvaluator()
        self.sre_engine = sre_engine or SREReliabilityEngine()
        self.regression_detector = regression_detector or RegressionDetector()
        self.gatekeeper = gatekeeper or DeploymentReadinessGate()
        self.scorer = scorer or HealthQualityScorer()
        self.exporter = exporter or HealthQualityExporter(output_dir=self.output_dir)

    def run_full_certification(self, previous_scores: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        # Step 1: Collect 8-dimension quality metrics
        liveness = self.evaluator.evaluate_liveness()
        readiness = self.evaluator.evaluate_readiness()
        dependencies = self.evaluator.evaluate_dependencies()
        failure_detection = self.evaluator.evaluate_failure_detection()
        recovery = self.evaluator.evaluate_recovery()
        monitoring = self.evaluator.evaluate_monitoring()
        security = self.evaluator.evaluate_security()
        evidence = self.evaluator.evaluate_evidence()

        # Step 2: Calculate SRE Reliability Metrics
        sre_metrics = self.sre_engine.calculate_reliability_metrics()

        # Step 3: Check for quality regression
        current_scores = {
            "liveness": liveness.score,
            "readiness": readiness.score,
            "dependencies": dependencies.score,
            "failure_detection": failure_detection.score,
            "recovery": recovery.score,
            "monitoring": monitoring.score,
            "security": security.score,
            "evidence": evidence.score,
        }
        # Provisional overall
        weights = self.scorer.WEIGHTS
        prov_overall = sum(current_scores[k] * weights[k] for k in weights)
        current_scores["overall"] = round(prov_overall, 2)

        regression_report = self.regression_detector.detect_regression(
            current_scores=current_scores,
            previous_scores=previous_scores,
        )

        # Step 4: Run Production Readiness Deployment Gatekeeper
        gate_report = self.gatekeeper.evaluate_deployment_gate(
            overall_score=prov_overall,
            liveness_score=liveness.score,
            readiness_score=readiness.score,
            security_score=security.score,
            failure_detection_score=failure_detection.score,
            sre_metrics=sre_metrics,
            regression_report=regression_report,
        )

        # Step 5: Compute Master Scorecard & Certification Report
        scorecard: HealthQualityScorecard = self.scorer.calculate_certification_scorecard(
            liveness=liveness,
            readiness=readiness,
            dependencies=dependencies,
            failure_detection=failure_detection,
            recovery=recovery,
            monitoring=monitoring,
            security=security,
            evidence=evidence,
            sre_metrics=sre_metrics,
            regression_report=regression_report,
            gate_report=gate_report,
        )

        # Step 6: Export evidence repository & checksum manifest
        exported_files = self.exporter.export_all(scorecard=scorecard)

        return {
            "scorecard": scorecard,
            "liveness": liveness,
            "readiness": readiness,
            "dependencies": dependencies,
            "failure_detection": failure_detection,
            "recovery": recovery,
            "monitoring": monitoring,
            "security": security,
            "evidence": evidence,
            "sre_metrics": sre_metrics,
            "regression_report": regression_report,
            "deployment_gate": gate_report,
            "exported_files": exported_files,
        }
