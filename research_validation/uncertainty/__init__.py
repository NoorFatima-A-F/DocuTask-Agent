"""Uncertainty quantification & propagation module."""

from research_validation.uncertainty.uncertainty_quant import (
    UncertaintyQuantificationLab, UncertaintyDecomposition,
    ConformalPredictionInterval, UncertaintyAuditReport
)
from research_validation.uncertainty.advanced_uncertainty import (
    AdvancedUncertaintyQuantificationLab, TriComponentUncertainty,
    ConformalPredictionSet, AdvancedUncertaintyReport
)
from research_validation.uncertainty.uncertainty_propagation import (
    UncertaintyPropagationEngine, EndToEndUncertaintyReport, StageUncertainty
)
from research_validation.uncertainty.confidence_budget import (
    ConfidenceBudgetManager, ConfidenceBudgetReport, BudgetStatus, StageBudgetConsumption
)
from research_validation.uncertainty.evidence_weighting import (
    DynamicEvidenceWeightEngine, CalibratedWeightScheme, WeightSensitivityReport
)
from research_validation.uncertainty.calibration import (
    EmpiricalCalibrationEngine, CalibrationAuditReport, CalibrationBin
)
