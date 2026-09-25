"""
Prediction Validation Engine Package (ASVSP).
Provides RMSE/MAE/MAPE regression metrics, residual diagnostic testing, and real-time calibration monitors.
"""

from app.runtime.predictions.prediction_error import PredictionAccuracyMetrics, PredictionErrorCalculator
from app.runtime.predictions.residual_analysis import ResidualAnalyzer
from app.runtime.predictions.calibration_monitor import CalibrationMonitor, calibration_monitor
from app.runtime.predictions.prediction_statistics import PredictionStatisticsAggregator
from app.runtime.predictions.prediction_validator import PredictionValidator

PredictionErrorEngine = PredictionErrorCalculator
CalibrationDriftMonitor = CalibrationMonitor
PredictionStatisticsTracker = PredictionStatisticsAggregator

__all__ = [
    "PredictionAccuracyMetrics",
    "PredictionErrorCalculator",
    "PredictionErrorEngine",
    "ResidualAnalyzer",
    "CalibrationMonitor",
    "CalibrationDriftMonitor",
    "calibration_monitor",
    "PredictionStatisticsAggregator",
    "PredictionStatisticsTracker",
    "PredictionValidator",
]
