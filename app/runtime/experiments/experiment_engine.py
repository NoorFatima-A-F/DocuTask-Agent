"""
Scientific Experiment Engine - Master Engine Facade
Unifies A/B testing, Bayesian decision theory, Wald's SPRT, and registry management.
"""

from typing import Dict, List, Any, Optional
from app.runtime.experiments.ab_testing import ABTestingEngine, ABTestResult
from app.runtime.experiments.bayesian_experiment import BayesianExperimentEngine, BayesianExperimentResult
from app.runtime.experiments.sequential_testing import SequentialProbabilityRatioTest, SPRTResult
from app.runtime.experiments.experiment_registry import ExperimentRegistry, ExperimentDefinition


class ExperimentEngine:
    """Master controller for scientific experimentation in production."""

    def __init__(self):
        self.registry = ExperimentRegistry()
        self.ab_engine = ABTestingEngine()
        self.bayesian_engine = BayesianExperimentEngine()
        self.sprt_engine = SequentialProbabilityRatioTest()

    def list_all_experiments(self) -> List[Dict[str, Any]]:
        return [e.to_dict() for e in self.registry.list_experiments()]

    def run_frequentist_analysis(self, experiment_id: str, alpha: float = 0.05) -> Dict[str, Any]:
        exp = self.registry.get_experiment(experiment_id)
        if not exp:
            return {"error": f"Experiment {experiment_id} not found"}

        result = self.ab_engine.evaluate(
            control_samples=exp.control_samples,
            treatment_samples=exp.treatment_samples,
            alpha=alpha,
        )
        return {
            "experiment_id": experiment_id,
            "name": exp.name,
            "frequentist_results": result.to_dict(),
        }

    def run_bayesian_analysis(
        self,
        experiment_id: str,
        prior_alpha: float = 1.0,
        prior_beta: float = 1.0,
    ) -> Dict[str, Any]:
        exp = self.registry.get_experiment(experiment_id)
        if not exp:
            return {"error": f"Experiment {experiment_id} not found"}

        # Convert continuous samples to binary benchmark threshold passes (>= 0.90)
        c_succ = sum(1 for x in exp.control_samples if x >= 0.90)
        t_succ = sum(1 for x in exp.treatment_samples if x >= 0.90)

        result = self.bayesian_engine.evaluate_bernoulli(
            control_successes=c_succ,
            control_trials=len(exp.control_samples),
            treatment_successes=t_succ,
            treatment_trials=len(exp.treatment_samples),
            prior_alpha=prior_alpha,
            prior_beta=prior_beta,
        )
        return {
            "experiment_id": experiment_id,
            "name": exp.name,
            "bayesian_results": result.to_dict(),
        }

    def run_sprt_step(self, success: bool) -> Dict[str, Any]:
        result = self.sprt_engine.observe(success)
        return result.to_dict()
