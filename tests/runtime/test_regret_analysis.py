"""
Unit & Asymptotic Tests for Regret Analysis (QDIOP / SDIOP).
"""

import pytest
from app.runtime.evaluation import RegretAnalyzer


def test_regret_computation_and_sublinearity():
    selected = [0.85, 0.90, 0.92, 0.95, 0.96]
    oracle = [0.95, 0.95, 0.95, 0.96, 0.97]

    regret_res = RegretAnalyzer.compute_regret(selected, oracle)
    assert len(regret_res["instantaneous_regrets"]) == 5
    assert len(regret_res["cumulative_regrets"]) == 5
    assert regret_res["total_regret"] > 0.0
    assert regret_res["instantaneous_regrets"][-1] < regret_res["instantaneous_regrets"][0]
    assert regret_res["sublinear_rate"]
