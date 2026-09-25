"""
Scientific Experiment Engine - Wald's Sequential Probability Ratio Test (SPRT)
Enables online early-stopping decisions with strict error rate guarantees.
"""

import math
from typing import Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class SPRTResult:
    log_likelihood_ratio: float
    upper_boundary_a: float
    lower_boundary_b: float
    decision: str  # ACCEPT_H1_TREATMENT | ACCEPT_H0_CONTROL | CONTINUE_TESTING
    trials_consumed: int
    alpha_bound: float
    beta_bound: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SequentialProbabilityRatioTest:
    """Wald's SPRT for testing H0: p = p0 vs H1: p = p1 with early stopping."""

    def __init__(self, p0: float = 0.90, p1: float = 0.95, alpha: float = 0.05, beta: float = 0.10):
        self.p0 = p0
        self.p1 = p1
        self.alpha = alpha
        self.beta = beta

        # Wald boundaries
        # A = ln((1 - beta) / alpha)
        # B = ln(beta / (1 - alpha))
        self.upper_a = math.log((1.0 - beta) / alpha)
        self.lower_b = math.log(beta / (1.0 - alpha))
        self.log_llr = 0.0
        self.trials = 0

    def observe(self, success: bool) -> SPRTResult:
        self.trials += 1
        if success:
            step_llr = math.log(self.p1 / self.p0)
        else:
            step_llr = math.log((1.0 - self.p1) / (1.0 - self.p0))

        self.log_llr += step_llr

        if self.log_llr >= self.upper_a:
            decision = "ACCEPT_H1_TREATMENT"
        elif self.log_llr <= self.lower_b:
            decision = "ACCEPT_H0_CONTROL"
        else:
            decision = "CONTINUE_TESTING"

        return SPRTResult(
            log_likelihood_ratio=round(self.log_llr, 4),
            upper_boundary_a=round(self.upper_a, 4),
            lower_boundary_b=round(self.lower_b, 4),
            decision=decision,
            trials_consumed=self.trials,
            alpha_bound=self.alpha,
            beta_bound=self.beta,
        )

    def reset(self):
        self.log_llr = 0.0
        self.trials = 0
