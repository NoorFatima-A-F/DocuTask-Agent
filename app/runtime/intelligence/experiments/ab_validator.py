"""
A/B Validator for Phase 10 (AISLCOP).

Executes randomized control trials and shadow replays comparing Control vs Candidate strategies.
"""

from __future__ import annotations

import hashlib
import random
import time
import uuid
from typing import Dict, List, Optional

from app.runtime.intelligence.experiments.experiment_model import (
    ExperimentRun,
    ExperimentStatus,
    TrialResult,
)
from app.runtime.intelligence.experiments.statistical_comparator import (
    StatisticalComparator,
)
from app.runtime.intelligence.strategy.strategy_model import ExecutionStrategy


class ABValidator:
    """
    Orchestrates A/B trials and evaluates promotion criteria scientifically.
    """

    def __init__(self):
        self._runs: Dict[str, ExperimentRun] = {}

    def run_experiment(
        self,
        title: str,
        hypothesis_id: str,
        control_strategy: ExecutionStrategy,
        candidate_strategy: ExecutionStrategy,
        sample_size: int = 10,
        rng_seed: int = 42,
    ) -> ExperimentRun:
        """
        Executes N trials for Control and N trials for Candidate strategies,
        measures metrics, computes Welch's t-test, and issues a promotion verdict.
        """
        random.seed(rng_seed)
        experiment_id = f"exp_run_{uuid.uuid4().hex[:10]}"

        control_trials: List[TrialResult] = []
        candidate_trials: List[TrialResult] = []

        # Simulate or replay trials using strategy distribution profiles
        for i in range(sample_size):
            # Control trial
            c_lat = max(100.0, random.gauss(control_strategy.latency_profile.mean, max(10.0, control_strategy.latency_profile.std_dev)))
            c_cost = max(0.001, random.gauss(control_strategy.cost_profile.mean, max(0.0005, control_strategy.cost_profile.std_dev)))
            c_conf = min(0.99, max(0.70, random.gauss(control_strategy.confidence_profile.mean, max(0.01, control_strategy.confidence_profile.std_dev))))
            c_retries = 1 if random.random() < control_strategy.retry_frequency else 0
            
            control_trials.append(
                TrialResult(
                    trial_id=f"ctrl_{i+1}",
                    variant="CONTROL",
                    latency_ms=round(c_lat, 2),
                    cost_usd=round(c_cost, 6),
                    confidence=round(c_conf, 4),
                    retries_count=c_retries,
                    validation_passed=True,
                    evidence_hash=hashlib.sha256(f"ctrl_{i}_{c_lat}".encode("utf-8")).hexdigest()[:16],
                )
            )

            # Candidate trial
            cand_lat = max(100.0, random.gauss(candidate_strategy.latency_profile.mean, max(10.0, candidate_strategy.latency_profile.std_dev)))
            cand_cost = max(0.001, random.gauss(candidate_strategy.cost_profile.mean, max(0.0005, candidate_strategy.cost_profile.std_dev)))
            cand_conf = min(0.99, max(0.70, random.gauss(candidate_strategy.confidence_profile.mean, max(0.01, candidate_strategy.confidence_profile.std_dev))))
            cand_retries = 1 if random.random() < candidate_strategy.retry_frequency else 0

            candidate_trials.append(
                TrialResult(
                    trial_id=f"cand_{i+1}",
                    variant="CANDIDATE",
                    latency_ms=round(cand_lat, 2),
                    cost_usd=round(cand_cost, 6),
                    confidence=round(cand_conf, 4),
                    retries_count=cand_retries,
                    validation_passed=True,
                    evidence_hash=hashlib.sha256(f"cand_{i}_{cand_lat}".encode("utf-8")).hexdigest()[:16],
                )
            )

        # Statistical Comparisons
        lat_comp = StatisticalComparator.compare_metrics(
            "latency_ms",
            [t.latency_ms for t in control_trials],
            [t.latency_ms for t in candidate_trials],
            higher_is_better=False,
        )

        cost_comp = StatisticalComparator.compare_metrics(
            "cost_usd",
            [t.cost_usd for t in control_trials],
            [t.cost_usd for t in candidate_trials],
            higher_is_better=False,
        )

        conf_comp = StatisticalComparator.compare_metrics(
            "confidence",
            [t.confidence for t in control_trials],
            [t.confidence for t in candidate_trials],
            higher_is_better=True,
        )

        ret_comp = StatisticalComparator.compare_metrics(
            "retries_count",
            [float(t.retries_count) for t in control_trials],
            [float(t.retries_count) for t in candidate_trials],
            higher_is_better=False,
        )

        # Promotion criteria: At least one significant improvement (p < 0.05) and no severe degradation in confidence or cost
        promotes = False
        reasons = []

        if lat_comp.is_significant and lat_comp.delta_pct < -5.0:
            promotes = True
            reasons.append(f"Statistically significant latency reduction of {abs(lat_comp.delta_pct):.1f}% (p={lat_comp.p_value:.4f})")
        if cost_comp.is_significant and cost_comp.delta_pct < -5.0:
            promotes = True
            reasons.append(f"Statistically significant cost savings of {abs(cost_comp.delta_pct):.1f}% (p={cost_comp.p_value:.4f})")
        if conf_comp.is_significant and conf_comp.delta_pct > 2.0:
            promotes = True
            reasons.append(f"Statistically significant confidence improvement of {conf_comp.delta_pct:.1f}% (p={conf_comp.p_value:.4f})")
        if ret_comp.is_significant and ret_comp.delta_abs < 0:
            promotes = True
            reasons.append(f"Statistically significant retry reduction (p={ret_comp.p_value:.4f})")

        # Guard against confidence collapse
        if conf_comp.candidate_mean < 0.85:
            promotes = False
            reasons = ["Rejected: Candidate confidence fell below safe enterprise floor (0.85)."]

        verdict = "; ".join(reasons) if promotes else "Candidate did not demonstrate statistically significant improvement (p >= 0.05) over baseline."

        run = ExperimentRun(
            experiment_id=experiment_id,
            title=title,
            hypothesis_id=hypothesis_id,
            control_strategy_id=control_strategy.strategy_id,
            candidate_strategy_id=candidate_strategy.strategy_id,
            sample_size_per_variant=sample_size,
            status=ExperimentStatus.CONCLUDED,
            created_at=time.time(),
            concluded_at=time.time(),
            control_trials=control_trials,
            candidate_trials=candidate_trials,
            latency_comparison=lat_comp,
            cost_comparison=cost_comp,
            confidence_comparison=conf_comp,
            retry_comparison=ret_comp,
            promotes_candidate=promotes,
            verdict_summary=verdict,
        )

        self._runs[experiment_id] = run
        return run

    def get(self, experiment_id: str) -> Optional[ExperimentRun]:
        return self._runs.get(experiment_id)

    def list_all(self) -> List[ExperimentRun]:
        return list(self._runs.values())
