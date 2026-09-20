"""
Visualization Layer compiling Metric, Benchmark, and AI Quality Dashboards.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from app.platform_verification.evaluation_engine.domain.models import (
    EvaluationReport,
    MetricDashboardView,
    BenchmarkDashboardView,
    AiQualityDashboardView,
    RegressionAlert,
)


class MetricsDashboardEngine:
    """Generates structured dashboard payloads for UI visualization and observability."""

    def generate_metric_dashboard(
        self, report: EvaluationReport, alerts: Optional[List[RegressionAlert]] = None
    ) -> MetricDashboardView:
        cards = [
            {
                "metric_id": m.metric_id,
                "name": m.metric_name,
                "category": m.category.value,
                "value": m.raw_value,
                "normalized_score": m.normalized_score,
                "unit": m.unit,
                "passed": m.passed,
                "threshold": m.threshold,
            }
            for m in report.metric_results
        ]
        alert_dicts = [
            {
                "alert_id": a.alert_id,
                "metric_name": a.metric_name,
                "category": a.category.value,
                "delta_pct": a.delta_percentage,
                "message": a.message,
            }
            for a in (alerts or [])
        ]
        return MetricDashboardView(
            title=f"Verification Intelligence Dashboard - {report.system_version}",
            overall_score=report.overall_score.overall_score,
            certification_band=report.overall_score.certification_band.value,
            metric_cards=cards,
            recent_alerts=alert_dicts,
        )

    def generate_benchmark_dashboard(
        self, report: EvaluationReport, candidate_ver: str, baseline_ver: str
    ) -> BenchmarkDashboardView:
        cards = [
            {
                "metric": b.metric,
                "candidate_result": b.result,
                "baseline_result": b.baseline_result,
                "delta": b.difference,
                "pct_change": b.percentage_change,
                "trend": b.trend.value,
                "analysis": b.analysis,
            }
            for b in report.benchmark_comparisons
        ]
        reg_count = sum(1 for b in report.benchmark_comparisons if b.trend.value == "REGRESSED")
        imp_count = sum(1 for b in report.benchmark_comparisons if b.trend.value == "IMPROVED")

        return BenchmarkDashboardView(
            title=f"Benchmark Comparison: {candidate_ver} vs {baseline_ver}",
            candidate_version=candidate_ver,
            baseline_version=baseline_ver,
            comparison_cards=cards,
            regression_count=reg_count,
            improvement_count=imp_count,
        )

    def generate_ai_quality_dashboard(
        self, ai_metrics: Dict[str, float]
    ) -> AiQualityDashboardView:
        radar = {
            "Grounding": ai_metrics.get("grounding_score", 95.0),
            "Faithfulness": ai_metrics.get("faithfulness_score", 94.0),
            "Completeness": ai_metrics.get("completeness_score", 92.0),
            "Consistency": ai_metrics.get("consistency_score", 95.0),
            "Safety": ai_metrics.get("safety_score", 100.0),
            "Context Utilization": ai_metrics.get("context_utilization_score", 90.0),
        }
        return AiQualityDashboardView(
            title="Generative AI Quality & Safety Intelligence Dashboard",
            grounding_score=ai_metrics.get("grounding_score", 95.0),
            faithfulness_score=ai_metrics.get("faithfulness_score", 94.0),
            hallucination_rate=ai_metrics.get("hallucination_rate", 2.0),
            completeness_score=ai_metrics.get("completeness_score", 92.0),
            consistency_score=ai_metrics.get("consistency_score", 95.0),
            safety_score=ai_metrics.get("safety_score", 100.0),
            radar_chart_data=radar,
        )
