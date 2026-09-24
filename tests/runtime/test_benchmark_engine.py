"""
Unit & Significance Tests for Scientific Benchmark Engine (QDIOP / SDIOP).
"""

from app.runtime.benchmarking import (
    BenchmarkStatistics,
    BENCHMARK_SUITES,
)


def test_benchmark_suites_availability():
    assert "enterprise_invoices" in BENCHMARK_SUITES
    assert "tax_forms_multilingual" in BENCHMARK_SUITES
    assert len(BENCHMARK_SUITES["enterprise_invoices"]) >= 10


def test_benchmark_statistics_hypothesis_testing():
    optimizer_scores = [0.95, 0.96, 0.94, 0.98, 0.95, 0.97, 0.96, 0.95, 0.99, 0.94]
    greedy_scores = [0.75, 0.78, 0.76, 0.80, 0.72, 0.79, 0.77, 0.76, 0.81, 0.74]

    stats = BenchmarkStatistics.compute_comparative_stats(optimizer_scores, greedy_scores)
    assert stats["win_rate_percent"] == 100.0
    assert stats["p_value"] < 0.01
    assert stats["is_statistically_significant"]
    assert stats["cohens_d"] > 0.80
