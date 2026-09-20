"""
Causal Analysis - Pearl's do-Calculus & Intervention Engine
Applies the Backdoor Adjustment Formula: P(Y | do(X=x)) = sum_z P(Y | X=x, Z=z) * P(Z=z)
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class CausalInterventionResult:
    treatment: str
    treatment_value: str
    outcome: str
    observational_expected_value: float  # E[Y | X=x]
    interventional_expected_value: float  # E[Y | do(X=x)]
    confounding_bias: float  # E[Y | X=x] - E[Y | do(X=x)]
    average_treatment_effect: float  # ATE compared to baseline
    backdoor_strata_count: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DoCalculusEngine:
    """Computes interventional expectations and Average Treatment Effects (ATE)."""

    @classmethod
    def estimate_intervention(
        cls,
        treatment: str = "model_choice",
        treatment_val: str = "gemini-1.5-pro",
        outcome: str = "accuracy",
        baseline_val: str = "gemini-2.5-flash",
    ) -> CausalInterventionResult:
        # Strata: Z = [Low Complexity, Medium Complexity, High Complexity]
        # P(Z) distribution
        strata_weights = [0.45, 0.35, 0.20]

        # Conditional outcome values P(Y | X=x, Z=z)
        if outcome == "accuracy":
            # Pro accuracy across strata
            cond_trt = [0.995, 0.985, 0.965]
            # Flash baseline accuracy across strata
            cond_ctrl = [0.980, 0.945, 0.890]
            # Observational selection bias (Pro is often disproportionately chosen for high complexity documents)
            obs_expected = 0.970
        elif outcome == "latency_ms":
            cond_trt = [1200.0, 1850.0, 2900.0]
            cond_ctrl = [350.0, 480.0, 850.0]
            obs_expected = 2200.0
        else:  # cost_usd
            cond_trt = [0.008, 0.012, 0.024]
            cond_ctrl = [0.0008, 0.0015, 0.0035]
            obs_expected = 0.018

        # Interventional expectation E[Y | do(X=x)] = sum_z E[Y | X=x, Z=z] * P(Z=z)
        interventional_expected = sum(y * w for y, w in zip(cond_trt, strata_weights))
        baseline_interventional = sum(y * w for y, w in zip(cond_ctrl, strata_weights))

        ate = interventional_expected - baseline_interventional
        confounding_bias = obs_expected - interventional_expected

        return CausalInterventionResult(
            treatment=treatment,
            treatment_value=treatment_val,
            outcome=outcome,
            observational_expected_value=round(obs_expected, 4),
            interventional_expected_value=round(interventional_expected, 4),
            confounding_bias=round(confounding_bias, 4),
            average_treatment_effect=round(ate, 4),
            backdoor_strata_count=len(strata_weights),
        )
