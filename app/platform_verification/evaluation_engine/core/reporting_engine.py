"""
Reporting Engine generating Verification Reports, Trend Reports, Benchmark Comparison Scorecards, and Charts.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from app.platform_verification.evaluation_engine.domain.models import (
    EvaluationReport,
    EvaluationRecommendation,
    TrendReport,
    TrendPoint,
    ComparisonTrend,
    OverallScore,
    QualityGateDecision,
    MetricResult,
    BenchmarkRecord,
    Severity,
    MetricCategory,
)


class ReportingEngine:
    """Compiles multi-format enterprise evaluation reports and visualizations."""

    def generate_evaluation_report(
        self,
        execution_id: str,
        system_version: str,
        overall_score: OverallScore,
        quality_gate_decision: QualityGateDecision,
        metric_results: List[MetricResult],
        benchmark_comparisons: Optional[List[BenchmarkRecord]] = None,
        evidence_links: Optional[List[str]] = None,
    ) -> EvaluationReport:
        recommendations: List[EvaluationRecommendation] = []
        for fail in quality_gate_decision.blocking_failures:
            recommendations.append(
                EvaluationRecommendation(
                    recommendation_id=str(uuid.uuid4())[:8],
                    category=MetricCategory.SECURITY,
                    severity=Severity.CRITICAL,
                    message=fail,
                    suggested_action="Block deployment and remediate root cause.",
                )
            )
        for warn in quality_gate_decision.warnings:
            recommendations.append(
                EvaluationRecommendation(
                    recommendation_id=str(uuid.uuid4())[:8],
                    category=MetricCategory.PERFORMANCE,
                    severity=Severity.HIGH,
                    message=warn,
                    suggested_action="Optimize component performance before SLA breach.",
                )
            )

        return EvaluationReport(
            report_id=f"rep_{uuid.uuid4().hex[:12]}",
            execution_id=execution_id,
            system_version=system_version,
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall_score=overall_score,
            quality_gate_decision=quality_gate_decision,
            metric_results=metric_results,
            benchmark_comparisons=benchmark_comparisons or [],
            recommendations=recommendations,
            evidence_links=evidence_links or [],
        )

    def generate_trend_report(
        self, metric_id: str, metric_name: str, historical_points: List[TrendPoint]
    ) -> TrendReport:
        if len(historical_points) < 2:
            return TrendReport(
                metric_id=metric_id,
                metric_name=metric_name,
                points=historical_points,
                slope=0.0,
                trend=ComparisonTrend.STABLE,
            )

        n = len(historical_points)
        x_vals = list(range(n))
        y_vals = [p.value for p in historical_points]

        mean_x = sum(x_vals) / n
        mean_y = sum(y_vals) / n

        numer = sum((x_vals[i] - mean_x) * (y_vals[i] - mean_y) for i in range(n))
        denom = sum((x_vals[i] - mean_x) ** 2 for i in range(n))

        slope = numer / denom if denom != 0 else 0.0

        if slope > 0.1:
            trend = ComparisonTrend.IMPROVED
        elif slope < -0.1:
            trend = ComparisonTrend.REGRESSED
        else:
            trend = ComparisonTrend.STABLE

        variance = sum((y - mean_y) ** 2 for y in y_vals) / (n - 1)

        return TrendReport(
            metric_id=metric_id,
            metric_name=metric_name,
            points=historical_points,
            slope=round(slope, 4),
            trend=trend,
            variance=round(variance, 4),
        )

    def generate_scorecard_dict(self, report: EvaluationReport) -> Dict[str, Any]:
        """Formats evaluation report as a structured dashboard scorecard."""
        return {
            "report_id": report.report_id,
            "system_version": report.system_version,
            "overall_score": report.overall_score.overall_score,
            "certification_band": report.overall_score.certification_band.value,
            "gate_status": report.quality_gate_decision.status.value,
            "total_metrics": report.overall_score.total_metrics,
            "passed_metrics": report.overall_score.passed_metrics,
            "dimension_scores": {
                dim.value: {
                    "score": ds.score,
                    "weight": ds.weight,
                    "weighted_score": ds.weighted_score,
                    "passed": ds.passed,
                }
                for dim, ds in report.overall_score.dimensions.items()
            },
            "blocking_failures": report.quality_gate_decision.blocking_failures,
            "warnings": report.quality_gate_decision.warnings,
        }
