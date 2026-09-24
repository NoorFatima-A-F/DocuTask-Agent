"""
Phase 3O: Runtime Orchestrator for Enterprise Infrastructure Quality Scoring & Certification.
"""

import time
from typing import Any, Dict, List, Optional

from ..core.evidence_collector import EvidenceCollector
from ..core.evidence_normalizer import EvidenceNormalizer
from ..scoring.infrastructure_quality_scorer import InfrastructureQualityScorer
from ..risk.infrastructure_risk_analyzer import InfrastructureRiskAnalyzer
from ..certification.infrastructure_certifier import InfrastructureCertifier
from ..certification.maturity_evaluator import MaturityEvaluator
from ..regression.quality_regression_detector import QualityRegressionDetector
from ..reports.readiness_markdown_generator import ReadinessMarkdownGenerator
from ..exporter.infrastructure_certification_exporter import InfrastructureCertificationExporter
from ..domain.models import (
    CertificationDecision,
    MaturityAssessment,
    QualityRegressionReport,
    QualityScorecard,
    RiskAssessmentReport,
    VerificationManifest,
)


class InfrastructureCertificationRuntime:
    """
    Master Runtime Orchestrator for Phase 3O:
    Collects raw evidence across all prior verification phases (3A-3N),
    normalizes into canonical 6-pillar format, evaluates quality scores, analyzes operational risks,
    computes maturity levels, checks regression delta, generates markdown/JSON reports,
    and exports signed artifacts with SHA-256 validation.
    """

    def __init__(
        self,
        collector: Optional[EvidenceCollector] = None,
        normalizer: Optional[EvidenceNormalizer] = None,
        scorer: Optional[InfrastructureQualityScorer] = None,
        risk_analyzer: Optional[InfrastructureRiskAnalyzer] = None,
        certifier: Optional[InfrastructureCertifier] = None,
        maturity_evaluator: Optional[MaturityEvaluator] = None,
        regression_detector: Optional[QualityRegressionDetector] = None,
        report_generator: Optional[ReadinessMarkdownGenerator] = None,
        exporter: Optional[InfrastructureCertificationExporter] = None,
    ):
        self.collector = collector or EvidenceCollector()
        self.normalizer = normalizer or EvidenceNormalizer()
        self.scorer = scorer or InfrastructureQualityScorer()
        self.risk_analyzer = risk_analyzer or InfrastructureRiskAnalyzer()
        self.certifier = certifier or InfrastructureCertifier()
        self.maturity_evaluator = maturity_evaluator or MaturityEvaluator()
        self.regression_detector = regression_detector or QualityRegressionDetector()
        self.report_generator = report_generator or ReadinessMarkdownGenerator()
        self.exporter = exporter or InfrastructureCertificationExporter()

        self._latest_scorecard: Optional[QualityScorecard] = None
        self._latest_decision: Optional[CertificationDecision] = None
        self._latest_risk_report: Optional[RiskAssessmentReport] = None
        self._latest_maturity: Optional[MaturityAssessment] = None
        self._latest_regression: Optional[QualityRegressionReport] = None
        self._latest_manifest: Optional[VerificationManifest] = None

    def run_full_certification(
        self,
        search_paths: Optional[List[str]] = None,
        export_dir: str = "infrastructure_certification",
    ) -> Dict[str, Any]:
        start_time = time.time()

        # 1. Collect Raw Evidence
        raw_bundles = self.collector.collect_all_evidence(search_paths=search_paths)

        # 2. Normalize Evidence into 6 Pillars
        normalized_items = self.normalizer.normalize(raw_bundles)

        # 3. Calculate 6-Pillar Quality Score
        scorecard = self.scorer.calculate_score(normalized_items, execution_time_seconds=time.time() - start_time)
        self._latest_scorecard = scorecard

        # 4. Assess Operational Risks & Critical Failure Conditions
        risk_report = self.risk_analyzer.assess_risks(scorecard, normalized_items)
        self._latest_risk_report = risk_report

        # 5. Evaluate Production Certification & Deployment Decision
        decision = self.certifier.evaluate_certification(scorecard, risk_report)
        self._latest_decision = decision

        # 6. Assess Operational Maturity (Level 0 - Level 5)
        maturity = self.maturity_evaluator.assess_maturity(scorecard, risk_report)
        self._latest_maturity = maturity

        # 7. Check for Quality Regressions
        regression = self.regression_detector.detect_regressions(scorecard)
        self._latest_regression = regression

        # 8. Generate Human-Readable Markdown Report
        markdown_content = self.report_generator.generate_report(
            decision, scorecard, risk_report, maturity, regression
        )

        # 9. Export All Structured Artifacts & Manifest
        self.exporter.set_base_dir(export_dir)
        manifest = self.exporter.export_all(
            raw_bundles=raw_bundles,
            normalized_items=normalized_items,
            scorecard=scorecard,
            risk_report=risk_report,
            decision=decision,
            maturity=maturity,
            regression=regression,
            markdown_content=markdown_content,
        )
        self._latest_manifest = manifest

        return {
            "scorecard": scorecard,
            "decision": decision,
            "risk_report": risk_report,
            "maturity": maturity,
            "regression": regression,
            "manifest": manifest,
            "passed": decision.deployment_approved,
            "overall_score": scorecard.overall_score,
            "certification": decision.certification.value,
        }

    def get_latest_scorecard(self) -> Optional[QualityScorecard]:
        return self._latest_scorecard

    def get_latest_decision(self) -> Optional[CertificationDecision]:
        return self._latest_decision

    def get_latest_risk_report(self) -> Optional[RiskAssessmentReport]:
        return self._latest_risk_report

    def get_latest_maturity(self) -> Optional[MaturityAssessment]:
        return self._latest_maturity

    def get_latest_manifest(self) -> Optional[VerificationManifest]:
        return self._latest_manifest

    async def run_all(self, export_dir: str = "infrastructure_certification") -> VerificationManifest:
        res = self.run_full_certification(export_dir=export_dir)
        return res["manifest"]
