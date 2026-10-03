"""
Scientific Regression Package (Phase 89C)
=========================================
"""

from research_validation.regression.drift_detector import (
    DriftDimension, DriftSeverity, DimensionDriftResult, MultiDimensionalDriftDetector
)
from research_validation.regression.regression_detector import (
    ScientificRegressionReport, ScientificRegressionDetector
)

__all__ = [
    "DriftDimension",
    "DriftSeverity",
    "DimensionDriftResult",
    "MultiDimensionalDriftDetector",
    "ScientificRegressionReport",
    "ScientificRegressionDetector",
]
