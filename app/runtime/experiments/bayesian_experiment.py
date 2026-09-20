"""
Scientific Experiment Engine - Bayesian Experimentation
Computes posterior probability distributions, Expected Loss, and Probability of Being Best.
"""

import math
import random
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class BayesianExperimentResult:
    prior_alpha: float
    prior_beta: float
    posterior_alpha: float
    posterior_beta: float
    posterior_mean: float
    credible_interval_95: List[float]
    prob_treatment_superior: float
    expected_loss: float
    decision_recommendation: str  # ADOPT_TREATMENT | RETAIN_CONTROL | CONTINUE_SAMPLING

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class BayesianExperimentEngine:
    """Bayesian A/B testing via conjugate prior posteriors and Monte Carlo sampling."""

    @classmethod
    def evaluate_bernoulli(
        cls,
        control_successes: int,
        control_trials: int,
        treatment_successes: int,
        treatment_trials: int,
        prior_alpha: float = 1.0,
        prior_beta: float = 1.0,
        num_simulations: int = 2000,
    ) -> BayesianExperimentResult:
        # Posterior distributions Beta(alpha + successes, beta + failures)
        post_ctrl_a = prior_alpha + control_successes
        post_ctrl_b = prior_beta + (control_trials - control_successes)

        post_trt_a = prior_alpha + treatment_successes
        post_trt_b = prior_beta + (treatment_trials - treatment_successes)

        # Posterior mean for treatment
        post_mean = post_trt_a / (post_trt_a + post_trt_b)

        # Standard approximation for 95% Credible Interval (Beta variance)
        var = (post_trt_a * post_trt_b) / (((post_trt_a + post_trt_b) ** 2) * (post_trt_a + post_trt_b + 1))
        sd = math.sqrt(max(1e-8, var))
        ci_lower = max(0.0, post_mean - 1.96 * sd)
        ci_upper = min(1.0, post_mean + 1.96 * sd)

        # Monte Carlo estimate of P(Treatment > Control) and Expected Loss
        random.seed(42)  # Deterministic seed for reproducible testing
        trt_wins = 0
        loss_sum = 0.0

        for _ in range(num_simulations):
            # Beta sampling via standard gamma ratio
            g_ctrl_a = random.gammavariate(post_ctrl_a, 1.0)
            g_ctrl_b = random.gammavariate(post_ctrl_b, 1.0)
            sample_ctrl = g_ctrl_a / (g_ctrl_a + g_ctrl_b)

            g_trt_a = random.gammavariate(post_trt_a, 1.0)
            g_trt_b = random.gammavariate(post_trt_b, 1.0)
            sample_trt = g_trt_a / (g_trt_a + g_trt_b)

            if sample_trt > sample_ctrl:
                trt_wins += 1
            else:
                loss_sum += (sample_ctrl - sample_trt)

        prob_superior = trt_wins / num_simulations
        expected_loss = loss_sum / num_simulations

        # Thresholds
        if prob_superior >= 0.95 and expected_loss < 0.005:
            rec = "ADOPT_TREATMENT"
        elif prob_superior <= 0.20:
            rec = "RETAIN_CONTROL"
        else:
            rec = "CONTINUE_SAMPLING"

        return BayesianExperimentResult(
            prior_alpha=prior_alpha,
            prior_beta=prior_beta,
            posterior_alpha=round(post_trt_a, 2),
            posterior_beta=round(post_trt_b, 2),
            posterior_mean=round(post_mean, 4),
            credible_interval_95=[round(ci_lower, 4), round(ci_upper, 4)],
            prob_treatment_superior=round(prob_superior, 4),
            expected_loss=round(expected_loss, 5),
            decision_recommendation=rec,
        )
