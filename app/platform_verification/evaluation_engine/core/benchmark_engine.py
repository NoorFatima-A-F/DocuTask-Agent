"""
Benchmark Comparison Engine for comparing candidate metrics against baseline versions and industry targets.
"""
from __future__ import annotations
from typing import Dict, List, Optional
from app.platform_verification.evaluation_engine.domain.models import (
    BenchmarkRecord,
    MetricResult,
    ComparisonTrend,
)
from app.platform_verification.evaluation_engine.domain.interfaces import IBenchmarkComparator


class BenchmarkEngine(IBenchmarkComparator):
    """Compares verification metrics against baselines and flags regressions."""

    def compare(
        self,
        candidate_results: List[MetricResult],
        baseline_results: List[MetricResult],
        system_version: str,
        baseline_version: str,
        dataset_name: str = "standard_benchmark_suite",
    ) -> List[BenchmarkRecord]:
        baseline_map: Dict[str, MetricResult] = {m.metric_id: m for m in baseline_results}
        records: List[BenchmarkRecord] = []

        for candidate in candidate_results:
            metric_id = candidate.metric_id
            if metric_id not in baseline_map:
                continue

            base = baseline_map[metric_id]
            diff = round(candidate.raw_value - base.raw_value, 4)
            pct_change = round((diff / base.raw_value * 100.0), 2) if base.raw_value != 0 else 0.0

            # Determine trend based on whether metric is higher-is-better or lower-is-better
            # Look at normalized scores for standardized comparison
            norm_diff = candidate.normalized_score - base.normalized_score
            if norm_diff > 0.5:
                trend = ComparisonTrend.IMPROVED
                analysis = f"Metric improved by {abs(pct_change)}% ({diff:+} {candidate.unit})."
            elif norm_diff < -0.5:
                trend = ComparisonTrend.REGRESSED
                analysis = f"Regression detected: degraded by {abs(pct_change)}% ({diff:+} {candidate.unit})."
            else:
                trend = ComparisonTrend.STABLE
                analysis = f"Metric remained stable within tolerance ({diff:+} {candidate.unit})."

            records.append(
                BenchmarkRecord(
                    system_version=system_version,
                    baseline=baseline_version,
                    dataset=dataset_name,
                    metric=candidate.metric_name,
                    result=candidate.raw_value,
                    baseline_result=base.raw_value,
                    difference=diff,
                    percentage_change=pct_change,
                    trend=trend,
                    analysis=analysis,
                )
            )

        return records
