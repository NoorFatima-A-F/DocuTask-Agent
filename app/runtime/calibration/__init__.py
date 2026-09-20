"""
Scientific Calibration Platform Package.
Provides reliability diagrams, ECE/MCE statistics, Platt/Isotonic calibration, and validation checks.
"""

from app.runtime.calibration.reliability_diagram import ReliabilityDiagramGenerator
from app.runtime.calibration.calibration_statistics import CalibrationStatistics
from app.runtime.calibration.calibration_validator import CalibrationValidator
from app.runtime.calibration.calibration_engine import ScientificCalibrationEngine, scientific_calibration_engine

__all__ = [
    "ReliabilityDiagramGenerator",
    "CalibrationStatistics",
    "CalibrationValidator",
    "ScientificCalibrationEngine",
    "scientific_calibration_engine",
]
