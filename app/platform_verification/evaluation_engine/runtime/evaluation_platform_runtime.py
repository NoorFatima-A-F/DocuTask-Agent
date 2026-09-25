"""
Unified Enterprise Evaluation Platform Runtime Facade (PART 5).
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from app.platform_verification.evaluation_engine.domain.models import (
    MetricResult,
    QualityGateRule,
    AIQualityAssessment,
    EvaluationReport,
    ABComparisonResult,
    RegressionAlert,
    SampleSizeValidationResult,
    MetricDashboardView,
)
from app.platform_verification.evaluation_engine.core.metric_registry import MetricRegistry
from app.platform_verification.evaluation_engine.core.statistical_engine import StatisticalEngine
from app.platform_verification.evaluation_engine.core.scoring_engine import ScoringEngine
from app.platform_verification.evaluation_engine.core.benchmark_engine import BenchmarkEngine
from app.platform_verification.evaluation_engine.core.quality_gate import QualityGateEngine
from app.platform_verification.evaluation_engine.core.reporting_engine import ReportingEngine
from app.platform_verification.evaluation_engine.core.ai_evaluators import IndependentAiEvaluator
from app.platform_verification.evaluation_engine.core.pipeline import EvaluationPipeline
from app.platform_verification.evaluation_engine.core.ab_testing import ABTestingEngine
from app.platform_verification.evaluation_engine.core.regression_detector import RegressionDetector
from app.platform_verification.evaluation_engine.core.sample_size_validator import SampleSizeValidator
from app.platform_verification.evaluation_engine.core.metric_store import MetricStore
from app.platform_verification.evaluation_engine.core.dashboard_engine import MetricsDashboardEngine
from app.platform_verification.evaluation_engine.api.metrics_api import MetricsAPI


class EvaluationPlatformRuntime:
    """Top-level enterprise facade for metrics, statistical evaluation, A/B testing, regression alerts, and dashboards."""

    def __init__(self) -> None:
        self.registry = MetricRegistry()
        self.stat_engine = StatisticalEngine()
        self.scoring_engine = ScoringEngine()
        self.benchmark_engine = BenchmarkEngine()
        self.gate_engine = QualityGateEngine()
        self.reporting_engine = ReportingEngine()
        self.ai_evaluator = IndependentAiEvaluator()
        self.ab_engine = ABTestingEngine(self.stat_engine)
        self.regression_detector = RegressionDetector()
        self.sample_size_validator = SampleSizeValidator()
        self.metric_store = MetricStore()
        self.dashboard_engine = MetricsDashboardEngine()
        self.api = MetricsAPI(
            registry=self.registry,
            ab_engine=self.ab_engine,
            scoring_engine=self.scoring_engine,
        )
        self.pipeline = EvaluationPipeline(
            registry=self.registry,
            stat_engine=self.stat_engine,
            scoring_engine=self.scoring_engine,
            benchmark_engine=self.benchmark_engine,
            gate_engine=self.gate_engine,
            reporting_engine=self.reporting_engine,
        )

    def evaluate_execution(
        self,
        raw_evidence: Dict[str, Any],
        system_version: str,
        baseline_evidence: Optional[Dict[str, Any]] = None,
        custom_rules: Optional[List[QualityGateRule]] = None,
        evidence_links: Optional[List[str]] = None,
    ) -> EvaluationReport:
        """Runs the complete evaluation pipeline for a verification execution and stores results."""
        report = self.pipeline.run_pipeline(
            raw_evidence=raw_evidence,
            system_version=system_version,
            baseline_evidence=baseline_evidence,
            custom_rules=custom_rules,
            evidence_links=evidence_links,
        )
        for res in report.metric_results:
            self.metric_store.save_result(report.execution_id, res)
        return report

    def compare_ab(
        self, variant_a_name: str, values_a: List[float], variant_b_name: str, values_b: List[float], metric_name: str
    ) -> ABComparisonResult:
        """Executes an A/B test comparison with statistical significance testing."""
        return self.ab_engine.compare_variants(variant_a_name, values_a, variant_b_name, values_b, metric_name)

    def detect_regressions(
        self, candidate_results: List[MetricResult], baseline_results: List[MetricResult]
    ) -> List[RegressionAlert]:
        """Automatically checks for quality, latency, or cost regressions."""
        return self.regression_detector.check_regressions(candidate_results, baseline_results)

    def validate_sample_power(
        self, sample_size: int, confidence: float = 0.95, margin_of_error: float = 0.05
    ) -> SampleSizeValidationResult:
        """Validates statistical sample size sufficiency."""
        return self.sample_size_validator.validate_power(sample_size, confidence, margin_of_error)

    def evaluate_ai_output(
        self, prompt: str, generated_output: str, ground_truth: Optional[str] = None, context: Optional[str] = None
    ) -> AIQualityAssessment:
        """Directly evaluates generative AI/LLM output quality."""
        return self.ai_evaluator.evaluate_output(prompt, generated_output, ground_truth, context)

    def generate_dashboards(
        self, report: EvaluationReport, alerts: Optional[List[RegressionAlert]] = None
    ) -> MetricDashboardView:
        """Generates structured dashboard payloads."""
        return self.dashboard_engine.generate_metric_dashboard(report, alerts)
