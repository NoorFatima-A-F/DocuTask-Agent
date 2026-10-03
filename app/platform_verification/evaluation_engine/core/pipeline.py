"""
End-to-End Evaluation Pipeline: Evidence -> Metrics -> Statistical Analysis -> Scoring -> Gate -> Report.
"""
from __future__ import annotations
import uuid
from typing import Any, Dict, List, Optional
from app.platform_verification.evaluation_engine.domain.models import (
    EvaluationReport,
    QualityGateRule,
    Severity,
)
from app.platform_verification.evaluation_engine.domain.interfaces import IEvaluationPipeline
from app.platform_verification.evaluation_engine.core.metric_registry import MetricRegistry
from app.platform_verification.evaluation_engine.core.statistical_engine import StatisticalEngine
from app.platform_verification.evaluation_engine.core.scoring_engine import ScoringEngine
from app.platform_verification.evaluation_engine.core.benchmark_engine import BenchmarkEngine
from app.platform_verification.evaluation_engine.core.quality_gate import QualityGateEngine
from app.platform_verification.evaluation_engine.core.reporting_engine import ReportingEngine
from app.platform_verification.evaluation_engine.core.evaluation_agents import (
    AccuracyEvaluatorAgent,
    PerformanceEvaluatorAgent,
    SecurityEvaluatorAgent,
    ReliabilityEvaluatorAgent,
    AiQualityEvaluatorAgent,
)


class EvaluationPipeline(IEvaluationPipeline):
    """Executes the 7-stage enterprise evaluation lifecycle."""

    def __init__(
        self,
        registry: Optional[MetricRegistry] = None,
        stat_engine: Optional[StatisticalEngine] = None,
        scoring_engine: Optional[ScoringEngine] = None,
        benchmark_engine: Optional[BenchmarkEngine] = None,
        gate_engine: Optional[QualityGateEngine] = None,
        reporting_engine: Optional[ReportingEngine] = None,
    ):
        self.registry = registry or MetricRegistry()
        self.stat_engine = stat_engine or StatisticalEngine()
        self.scoring_engine = scoring_engine or ScoringEngine()
        self.benchmark_engine = benchmark_engine or BenchmarkEngine()
        self.gate_engine = gate_engine or QualityGateEngine()
        self.reporting_engine = reporting_engine or ReportingEngine()

        # Initialize evaluation agents
        self.agents = [
            AccuracyEvaluatorAgent(self.registry),
            PerformanceEvaluatorAgent(self.registry),
            SecurityEvaluatorAgent(self.registry),
            ReliabilityEvaluatorAgent(self.registry),
            AiQualityEvaluatorAgent(self.registry),
        ]

    def run_pipeline(
        self,
        raw_evidence: Dict[str, Any],
        system_version: str,
        baseline_evidence: Optional[Dict[str, Any]] = None,
        custom_rules: Optional[List[QualityGateRule]] = None,
        evidence_links: Optional[List[str]] = None,
    ) -> EvaluationReport:
        # Stage 1 & 2: Metric Extraction via specialized agents
        metric_results = []
        for agent in self.agents:
            metric_results.extend(agent.evaluate(raw_evidence))

        # Stage 3: Statistical Validation
        # Verify sample size where applicable
        sample_size = raw_evidence.get("total_predictions", raw_evidence.get("total_runs", 100))
        self.stat_engine.validate_sample_size(sample_size, min_required=10)

        # Stage 4: Weighted Multi-Dimension Scoring
        overall_score = self.scoring_engine.compute_overall_score(metric_results)

        # Stage 5: Benchmark Comparison (if baseline provided)
        benchmark_records = []
        if baseline_evidence:
            baseline_metrics = []
            for agent in self.agents:
                baseline_metrics.extend(agent.evaluate(baseline_evidence))
            benchmark_records = self.benchmark_engine.compare(
                candidate_results=metric_results,
                baseline_results=baseline_metrics,
                system_version=system_version,
                baseline_version=baseline_evidence.get("system_version", "v1.0.0-baseline"),
            )

        # Stage 6: Quality Gate Evaluation
        rules = custom_rules or self._get_default_quality_gate_rules()
        gate_decision = self.gate_engine.evaluate_gate(metric_results, rules)

        # Stage 7: Report & Recommendation Generation
        execution_id = raw_evidence.get("execution_id", f"exec_{uuid.uuid4().hex[:8]}")
        return self.reporting_engine.generate_evaluation_report(
            execution_id=execution_id,
            system_version=system_version,
            overall_score=overall_score,
            quality_gate_decision=gate_decision,
            metric_results=metric_results,
            benchmark_comparisons=benchmark_records,
            evidence_links=evidence_links,
        )

    def _get_default_quality_gate_rules(self) -> List[QualityGateRule]:
        return [
            QualityGateRule(
                rule_id="QG-SEC-01",
                metric_id="sec_critical_vulns",
                condition="eq",
                target_value=0.0,
                severity=Severity.CRITICAL,
                required=True,
                description="Zero tolerance for critical security vulnerabilities.",
            ),
            QualityGateRule(
                rule_id="QG-FUNC-01",
                metric_id="func_accuracy",
                condition="gte",
                target_value=90.0,
                severity=Severity.CRITICAL,
                required=True,
                description="Functional accuracy must be at least 90%.",
            ),
            QualityGateRule(
                rule_id="QG-REL-01",
                metric_id="rel_failure_rate",
                condition="lte",
                target_value=5.0,
                severity=Severity.HIGH,
                required=True,
                description="Failure rate must not exceed 5%.",
            ),
            QualityGateRule(
                rule_id="QG-AI-01",
                metric_id="ai_hallucination_rate",
                condition="lte",
                target_value=5.0,
                severity=Severity.HIGH,
                required=False,
                description="AI hallucination rate must remain below 5%.",
            ),
        ]
