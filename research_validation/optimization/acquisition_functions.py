"""
Bayesian Acquisition Functions (Phase 88C)
=========================================
Implements Expected Improvement (EI), Upper Confidence Bound (UCB),
and Thompson Sampling (TS) for scientific experimentation optimization.
"""

from __future__ import annotations
import math
import random


def norm_pdf(x: float) -> float:
    """Standard normal probability density function."""
    return math.exp(-0.5 * (x ** 2)) / math.sqrt(2.0 * math.pi)


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def expected_improvement(
    mu: float,
    sigma: float,
    current_best: float,
    xi: float = 0.01,
) -> float:
    """
    Analytical Expected Improvement:
    EI(x) = (mu - current_best - xi) * Phi(Z) + sigma * phi(Z)
    where Z = (mu - current_best - xi) / sigma
    """
    if sigma <= 1e-8:
        return 0.0

    diff = mu - current_best - xi
    z = diff / sigma
    ei = diff * norm_cdf(z) + sigma * norm_pdf(z)
    return max(0.0, ei)


def upper_confidence_bound(
    mu: float,
    sigma: float,
    kappa: float = 1.96,
) -> float:
    """Upper Confidence Bound / Knowledge Gradient surrogate: UCB(x) = mu + kappa * sigma."""
    return mu + kappa * sigma


def thompson_sampling(
    mu: float,
    sigma: float,
    rng: random.Random = None,
) -> float:
    """Draws a Monte Carlo posterior sample: sample ~ N(mu, sigma^2)."""
    r = rng or random
    return r.gauss(mu, sigma)
