"""
Metric Validation and Monte Carlo Verification Framework for DocuTask Agent.
Provides property tests, boundary checks, and Monte Carlo convergence verification.
"""

from __future__ import annotations

import random
from typing import Any, Dict, List
from app.runtime.metrics.definitions import MetricDefinition, MetricUnit
from app.runtime.metrics.provenance import MetricProvenanceRecord
from app.runtime.metrics.statistics import ScientificStatisticsEngine


class MetricValidator:
    """
    Validates that computed metrics satisfy strict mathematical invariants.
    """

    @staticmethod
    def validate_provenance_record(record: MetricProvenanceRecord, defn: MetricDefinition) -> List[str]:
        """
        Validates all mathematical and provenance invariants for a MetricProvenanceRecord.
        Returns a list of violation errors (empty list if 100% valid).
        """
        errors: List[str] = []

        # 1. Check ID and Version consistency
        if record.metric_id != defn.id:
            errors.append(f"Metric ID mismatch: expected {defn.id}, got {record.metric_id}")
        if record.metric_version != defn.version:
            errors.append(f"Metric version mismatch: expected {defn.version}, got {record.metric_version}")

        # 2. Check value boundaries for percentages and ratios
        if defn.unit == MetricUnit.PERCENTAGE:
            val = float(record.value)
            if val < -1e-6 or val > 1.0 + 1e-6:
                errors.append(f"Percentage metric out of bounds [0.0, 1.0]: {val}")

        elif defn.unit in (MetricUnit.MILLISECONDS, MetricUnit.SECONDS, MetricUnit.COUNT, MetricUnit.HERTZ):
            val = float(record.value)
            if val < 0.0:
                errors.append(f"Non-negative metric is negative: {val}")

        # 3. Check statistical summary invariants if present
        if record.statistical_summary:
            stats = record.statistical_summary
            mean = float(stats["mean"])
            ci = stats.get("confidence_interval_95")
            if ci:
                ci_low, ci_high = float(ci[0]), float(ci[1])
                if ci_low > mean + 1e-6 or ci_high < mean - 1e-6:
                    errors.append(f"Confidence interval [{ci_low}, {ci_high}] does not enclose mean {mean}")
            if float(stats["variance"]) < -1e-6:
                errors.append(f"Sample variance is negative: {stats['variance']}")

        # 4. Check Merkle root integrity
        if not record.merkle_events_root_sha256 or len(record.merkle_events_root_sha256) != 64:
            errors.append("Invalid Merkle SHA-256 root hash length")

        return errors

    @staticmethod
    def run_monte_carlo_verification(
        true_mean: float = 120.0,
        true_stdev: float = 15.0,
        sample_size: int = 1000,
        trials: int = 500,
    ) -> Dict[str, Any]:
        """
        Executes Monte Carlo simulation to verify that ScientificStatisticsEngine estimators
        converge with zero bias to the true parameters.
        """
        random.seed(42)
        mean_estimates: List[float] = []
        variance_estimates: List[float] = []
        ci_coverage_hits = 0

        for _ in range(trials):
            sample = [random.gauss(true_mean, true_stdev) for _ in range(sample_size)]
            summary = ScientificStatisticsEngine.analyze_sample(sample)
            if not summary:
                continue

            mean_estimates.append(summary.mean)
            variance_estimates.append(summary.variance)

            # Check if true mean falls within computed 95% CI
            if summary.confidence_interval_95[0] <= true_mean <= summary.confidence_interval_95[1]:
                ci_coverage_hits += 1

        empirical_mean_of_means = sum(mean_estimates) / len(mean_estimates)
        empirical_mean_of_vars = sum(variance_estimates) / len(variance_estimates)
        empirical_ci_coverage = float(ci_coverage_hits) / float(trials)

        mean_bias = abs(empirical_mean_of_means - true_mean)
        var_bias = abs(empirical_mean_of_vars - (true_stdev ** 2))

        return {
            "trials": trials,
            "sample_size": sample_size,
            "true_mean": true_mean,
            "true_variance": true_stdev ** 2,
            "empirical_mean": empirical_mean_of_means,
            "empirical_variance": empirical_mean_of_vars,
            "mean_bias": mean_bias,
            "variance_bias": var_bias,
            "ci_95_coverage_rate": empirical_ci_coverage,  # Should be ~0.95
            "is_statistically_sound": mean_bias < 0.5 and var_bias < 2.0 and empirical_ci_coverage >= 0.92,
        }
