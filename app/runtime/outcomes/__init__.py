"""
Outcome Verification Engine Package (ASVSP).
Provides pairing of predicted vs observed metrics, verification, and ground-truth telemetry reconstruction.
"""

from app.runtime.outcomes.outcome_collector import DimensionPair, MissionOutcomeRecord, OutcomeCollector
from app.runtime.outcomes.outcome_validator import OutcomeValidator, OutcomeValidationError
from app.runtime.outcomes.outcome_reconstructor import OutcomeReconstructor
from app.runtime.outcomes.outcome_statistics import OutcomeStatisticsTracker, outcome_statistics_tracker
from app.runtime.outcomes.outcome_serializer import OutcomeSerializer

__all__ = [
    "DimensionPair",
    "MissionOutcomeRecord",
    "OutcomeCollector",
    "OutcomeValidator",
    "OutcomeValidationError",
    "OutcomeReconstructor",
    "OutcomeStatisticsTracker",
    "outcome_statistics_tracker",
    "OutcomeSerializer",
]
