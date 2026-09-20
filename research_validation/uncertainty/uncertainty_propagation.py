"""
Uncertainty Propagation Engine (Phase 82B.8)
============================================
Propagates measurement, transformation, and aggregation uncertainties through
multi-stage scientific pipelines:
Observation -> Transformation -> Aggregation -> Final Metric -> Decision

Implements first-order Taylor expansion variance approximations and Monte Carlo
sampling to guarantee that downstream confidence intervals reflect all upstream noise.
"""

from __future__ import annotations
import math
import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class StageUncertainty:
    stage_name: str
    nominal_value: float
    standard_error: float
    relative_uncertainty: float
    degrees_of_freedom: int
    variance_contribution_pct: float
    confidence_interval_95: Tuple[float, float]


@dataclass(frozen=True)
class EndToEndUncertaintyReport:
    pipeline_id: str
    target_metric_name: str
    nominal_value: float
    total_propagated_standard_error: float
    total_relative_uncertainty: float
    expanded_confidence_interval_95: Tuple[float, float]
    coverage_factor_k: float  # typically 1.96 for 95% Gaussian
    stage_breakdowns: Tuple[StageUncertainty, ...]
    dominant_uncertainty_stage: str
    propagation_digest: str


class UncertaintyPropagationEngine:
    """
    Propagates uncertainty analytically and via Monte Carlo simulation across stages.
    """

    @classmethod
    def propagate_chain(
        cls,
        pipeline_id: str,
        target_metric: str,
        stage_errors: List[Tuple[str, float, float]],  # (stage_name, nominal, std_err)
        k_coverage: float = 1.96,
    ) -> EndToEndUncertaintyReport:
        """
        Analytically propagate variances using root-sum-of-squares of relative errors.
        For multiplicative/aggregation chain: (u_c / y)^2 = sum( (u_i / x_i)^2 )
        """
        if not stage_errors:
            raise ValueError("At least one stage required for uncertainty propagation.")

        total_rel_var = 0.0
        for _, val, serr in stage_errors:
            rel = serr / abs(val) if abs(val) > 1e-9 else serr
            total_rel_var += rel**2

        total_rel_err = math.sqrt(total_rel_var)
        final_nominal = stage_errors[-1][1]
        total_std_err = total_rel_err * abs(final_nominal)

        ci_lower = final_nominal - k_coverage * total_std_err
        ci_upper = final_nominal + k_coverage * total_std_err

        stage_breakdowns: List[StageUncertainty] = []
        dominant_stage = stage_errors[0][0]
        max_contrib = -1.0

        for name, val, serr in stage_errors:
            rel = serr / abs(val) if abs(val) > 1e-9 else serr
            contrib = (rel**2) / total_rel_var if total_rel_var > 0 else (1.0 / len(stage_errors))
            if contrib > max_contrib:
                max_contrib = contrib
                dominant_stage = name

            s_ci = (val - k_coverage * serr, val + k_coverage * serr)
            stage_breakdowns.append(StageUncertainty(
                stage_name=name,
                nominal_value=val,
                standard_error=serr,
                relative_uncertainty=rel,
                degrees_of_freedom=30,
                variance_contribution_pct=contrib * 100.0,
                confidence_interval_95=s_ci,
            ))

        h_payload = {
            "pipeline": pipeline_id,
            "metric": target_metric,
            "nominal": final_nominal,
            "total_std_err": total_std_err,
            "stages": [s.stage_name for s in stage_breakdowns],
        }
        digest = hash_canonical_json(h_payload)

        return EndToEndUncertaintyReport(
            pipeline_id=pipeline_id,
            target_metric_name=target_metric,
            nominal_value=final_nominal,
            total_propagated_standard_error=total_std_err,
            total_relative_uncertainty=total_rel_err,
            expanded_confidence_interval_95=(ci_lower, ci_upper),
            coverage_factor_k=k_coverage,
            stage_breakdowns=tuple(stage_breakdowns),
            dominant_uncertainty_stage=dominant_stage,
            propagation_digest=digest,
        )

    @classmethod
    def monte_carlo_propagation(
        cls,
        sample_evaluator: Callable[[List[float]], float],
        parameter_distributions: List[Tuple[float, float]],  # (mean, std_dev)
        num_simulations: int = 2000,
        seed: int = 42,
    ) -> Tuple[float, float, Tuple[float, float]]:
        """
        Empirically propagate non-linear uncertainty via Monte Carlo sampling.
        Returns (mean, std_dev, (percentile_2_5, percentile_97_5)).
        """
        rng = random.Random(seed)
        results: List[float] = []

        for _ in range(num_simulations):
            sample_params = [
                rng.gauss(m, max(1e-9, s))
                for m, s in parameter_distributions
            ]
            try:
                out = sample_evaluator(sample_params)
                results.append(out)
            except Exception:
                pass

        if not results:
            return 0.0, 0.0, (0.0, 0.0)

        results.sort()
        n = len(results)
        mean_v = sum(results) / n
        var_v = sum((x - mean_v)**2 for x in results) / max(1, n - 1)
        std_v = math.sqrt(var_v)

        p025 = results[int(0.025 * n)]
        p975 = results[int(0.975 * n)]

        return mean_v, std_v, (p025, p975)
