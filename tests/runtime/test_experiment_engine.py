"""
Unit and Integration Tests for Scientific Experiment Engine & Testing (ASVSP Pillar 6).
"""

import pytest
from app.runtime.experiments import (
    ABTestingEngine,
    BayesianExperimentEngine,
    SequentialProbabilityRatioTest,
    ExperimentRegistry,
    ExperimentEngine,
)


def test_ab_testing_frequentist():
    ctrl = [0.80, 0.82, 0.81, 0.83, 0.80, 0.82, 0.81]
    trt = [0.95, 0.96, 0.94, 0.97, 0.95, 0.96, 0.95]

    result = ABTestingEngine.evaluate(ctrl, trt, alpha=0.05)
    assert result.treatment_mean > result.control_mean
    assert result.statistically_significant is True
    assert result.cohens_d > 0.0


def test_bayesian_experiment():
    result = BayesianExperimentEngine.evaluate_bernoulli(
        control_successes=80,
        control_trials=100,
        treatment_successes=96,
        treatment_trials=100,
    )
    assert result.prob_treatment_superior > 0.90
    assert result.decision_recommendation == "ADOPT_TREATMENT"


def test_sprt_sequential():
    sprt = SequentialProbabilityRatioTest(p0=0.80, p1=0.95)
    # Feed continuous successes
    dec = "CONTINUE_TESTING"
    for _ in range(25):
        res = sprt.observe(True)
        dec = res.decision
        if dec != "CONTINUE_TESTING":
            break
    assert dec in ["ACCEPT_H1_TREATMENT", "CONTINUE_TESTING"]


def test_experiment_engine_facade():
    engine = ExperimentEngine()
    exps = engine.list_all_experiments()
    assert len(exps) >= 1
    exp_id = exps[0]["experiment_id"]

    freq = engine.run_frequentist_analysis(exp_id)
    assert "frequentist_results" in freq

    bayes = engine.run_bayesian_analysis(exp_id)
    assert "bayesian_results" in bayes
