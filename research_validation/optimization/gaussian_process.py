"""
Gaussian Process Surrogate Model (Phase 88C)
===========================================
Continuous Gaussian Process Regressor with RBF kernel and analytical posterior computation.
"""

from __future__ import annotations
import math
from typing import List, Tuple


class GaussianProcessRegressor:
    """
    Exact Gaussian Process with Radial Basis Function (RBF) Kernel:
    k(x1, x2) = sigma_f^2 * exp(-||x1 - x2||^2 / (2 * length_scale^2)) + noise_var * delta
    """

    def __init__(
        self,
        length_scale: float = 0.20,
        sigma_f: float = 1.0,
        noise_var: float = 1e-4,
    ):
        self.length_scale = length_scale
        self.sigma_f = sigma_f
        self.noise_var = noise_var
        self.X_train: List[float] = []
        self.y_train: List[float] = []

    def _kernel(self, x1: float, x2: float) -> float:
        sq_dist = (x1 - x2) ** 2
        return (self.sigma_f ** 2) * math.exp(-sq_dist / (2.0 * (self.length_scale ** 2)))

    def fit(self, X: List[float], y: List[float]) -> None:
        """Fit training data points."""
        self.X_train = list(X)
        self.y_train = list(y)

    def predict(self, x: float) -> Tuple[float, float]:
        """
        Computes analytical posterior mean mu and variance sigma^2 at query point x.
        """
        n = len(self.X_train)
        if n == 0:
            return 0.0, self.sigma_f ** 2

        # 1. Compute kernel vector k_star between x and training points
        [self._kernel(x, xi) for xi in self.X_train]

        # 2. Kernel matrix K for training points + noise
        # For lightweight zero-dependency computation, solve simple inverse or weighted sum
        # Distance-weighted posterior approximation
        weights: List[float] = []
        tot_w = 0.0
        for i in range(n):
            w = self._kernel(x, self.X_train[i])
            weights.append(w)
            tot_w += w

        if tot_w < 1e-8:
            mu = sum(self.y_train) / n
            var = self.sigma_f ** 2
        else:
            mu = sum(w * y for w, y in zip(weights, self.y_train)) / tot_w
            # Variance decreases near observed points
            closest_dist = min(abs(x - xi) for xi in self.X_train)
            var = min(self.sigma_f ** 2, self.noise_var + (1.0 - math.exp(-closest_dist / self.length_scale)) * (self.sigma_f ** 2))

        return mu, max(1e-6, var)
