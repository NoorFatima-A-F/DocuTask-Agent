"""
Unit & Reproducibility Tests for Experiment Runner (QDIOP / SDIOP).
"""

from app.runtime.benchmarking import ExperimentRunner


def test_experiment_runner_deterministic_reproducibility():
    res1 = ExperimentRunner.run_suite_experiment(suite_name="enterprise_invoices", seed=42)
    res2 = ExperimentRunner.run_suite_experiment(suite_name="enterprise_invoices", seed=42)

    assert res1["overall_win_rate_percent"] == res2["overall_win_rate_percent"]
    assert res1["is_statistically_superior"]
    assert len(res1["task_breakdown"]) == 10
