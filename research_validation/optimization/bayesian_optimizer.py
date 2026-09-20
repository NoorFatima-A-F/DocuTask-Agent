"""
Bayesian Research Optimizer (Phase 88C)
=======================================
Autonomous closed-loop hyperparameter and pipeline optimizer with
convergence detection and automatic stopping criteria.
"""

from __future__ import annotations
import math
import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Callable, Dict, List, Optional, Tuple

from research_validation.optimization.gaussian_process import GaussianProcessRegressor
from research_validation.optimization.acquisition_functions import (
    expected_improvement, upper_confidence_bound, thompson_sampling
)
from research_validation.provenance.hashing import hash_canonical_json


class AcquisitionStrategy(str, Enum):
    EXPECTED_IMPROVEMENT = "EXPECTED_IMPROVEMENT"
    UPPER_CONFIDENCE_BOUND = "UPPER_CONFIDENCE_BOUND"
    THOMPSON_SAMPLING = "THOMPSON_SAMPLING"


@dataclass(frozen=True)
class OptimizationStep:
    """A single evaluation step in the Bayesian search loop."""
    step_number: int
    candidate_x: float
    observed_y: float
    predicted_mu: float
    predicted_sigma: float
    acquisition_score: float
    current_best_y: float


@dataclass(frozen=True)
class OptimizationResult:
    """Final output of Bayesian Optimization."""
    best_x: float
    best_y: float
    total_steps: int
    converged: bool
    convergence_reason: str
    history: List[OptimizationStep]
    optimization_digest_sha256: str = field(default="")


class BayesianResearchOptimizer:
    """
    Closed-loop Bayesian Optimization engine.
    """

    def __init__(
        self,
        bounds: Tuple[float, float] = (0.0, 1.0),
        strategy: AcquisitionStrategy = AcquisitionStrategy.EXPECTED_IMPROVEMENT,
        max_iterations: int = 20,
        convergence_tolerance: float = 1e-3,
        seed: int = 42,
    ):
        self.bounds = bounds
        self.strategy = strategy
        self.max_iterations = max_iterations
        self.tol = convergence_tolerance
        self.seed = seed
        self.rng = random.Random(seed)
        self.gp = GaussianProcessRegressor()

    def optimize(
        self,
        objective_fn: Callable[[float], float],
        initial_points: Optional[List[float]] = None,
    ) -> OptimizationResult:
        """Executes the closed-loop optimization search."""
        low, high = self.bounds
        init_x = initial_points or [low + (high - low) * 0.2, low + (high - low) * 0.8]
        
        X: List[float] = []
        y: List[float] = []
        history: List[OptimizationStep] = []

        # Initial seeding
        for pt in init_x:
            val = objective_fn(pt)
            X.append(pt)
            y.append(val)

        best_y = max(y)
        best_x = X[y.index(best_y)]
        converged = False
        conv_reason = "MAX_ITERATIONS_REACHED"

        # Candidate grid for acquisition evaluation
        grid = [low + (high - low) * (i / 100.0) for i in range(101)]

        for step in range(len(init_x), self.max_iterations):
            self.gp.fit(X, y)

            # Evaluate acquisition function across grid
            best_acq = -float("inf")
            next_x = grid[0]
            pred_mu_next = 0.0
            pred_sig_next = 1.0

            for cand in grid:
                mu, var = self.gp.predict(cand)
                sig = math.sqrt(var)

                if self.strategy == AcquisitionStrategy.EXPECTED_IMPROVEMENT:
                    acq = expected_improvement(mu, sig, best_y)
                elif self.strategy == AcquisitionStrategy.UPPER_CONFIDENCE_BOUND:
                    acq = upper_confidence_bound(mu, sig)
                else:
                    acq = thompson_sampling(mu, sig, self.rng)

                if acq > best_acq:
                    best_acq = acq
                    next_x = cand
                    pred_mu_next = mu
                    pred_sig_next = sig

            # Evaluate objective at selected point
            obs_y = objective_fn(next_x)
            X.append(next_x)
            y.append(obs_y)

            if obs_y > best_y:
                improvement = obs_y - best_y
                best_y = obs_y
                best_x = next_x
            else:
                improvement = 0.0

            history.append(OptimizationStep(
                step_number=step,
                candidate_x=next_x,
                observed_y=obs_y,
                predicted_mu=pred_mu_next,
                predicted_sigma=pred_sig_next,
                acquisition_score=best_acq,
                current_best_y=best_y,
            ))

            # Check convergence
            if step >= 5 and improvement < self.tol and best_acq < self.tol:
                converged = True
                conv_reason = f"CONVERGENCE_REACHED (Acquisition {best_acq:.6f} < {self.tol})"
                break

        payload = {
            "best_x": best_x,
            "best_y": best_y,
            "steps": len(history),
            "converged": converged,
        }
        digest = hash_canonical_json(payload)

        return OptimizationResult(
            best_x=best_x,
            best_y=best_y,
            total_steps=len(history) + len(init_x),
            converged=converged,
            convergence_reason=conv_reason,
            history=history,
            optimization_digest_sha256=digest,
        )
