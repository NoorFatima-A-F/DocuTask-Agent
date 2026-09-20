"""
Bayesian Optimization Package (Phase 88C)
=========================================
"""

from research_validation.optimization.gaussian_process import GaussianProcessRegressor
from research_validation.optimization.acquisition_functions import (
    norm_pdf, norm_cdf, expected_improvement, upper_confidence_bound, thompson_sampling
)
from research_validation.optimization.bayesian_optimizer import (
    AcquisitionStrategy, OptimizationStep, OptimizationResult, BayesianResearchOptimizer
)

__all__ = [
    "GaussianProcessRegressor",
    "norm_pdf",
    "norm_cdf",
    "expected_improvement",
    "upper_confidence_bound",
    "thompson_sampling",
    "AcquisitionStrategy",
    "OptimizationStep",
    "OptimizationResult",
    "BayesianResearchOptimizer",
]
