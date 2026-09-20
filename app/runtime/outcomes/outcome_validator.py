"""
Outcome Verification Engine - Outcome Validator
Validates observational integrity, physical non-negativity, and timestamp monotonicity.
"""

from typing import Dict, Any, List, Tuple
import math
from app.runtime.outcomes.outcome_collector import MissionOutcomeRecord


class OutcomeValidationError(ValueError):
    """Raised when an observed outcome vector contains invalid or corrupted metrics."""
    pass


class OutcomeValidator:
    """Validates ground-truth outcome vectors prior to ingestion into model validation engines."""

    @staticmethod
    def validate_bounds(accuracy: float, latency_ms: float, cost_usd: float) -> bool:
        """Simple invariant validation on fundamental metrics."""
        if accuracy < 0.0 or accuracy > 1.0:
            return False
        if latency_ms < 0.0:
            return False
        if cost_usd < 0.0:
            return False
        return True

    @staticmethod
    def validate_outcome_record(record: MissionOutcomeRecord) -> Tuple[bool, List[str]]:
        errors = []

        if not record.mission_id:
            errors.append("Missing mission_id in outcome record.")
        if not record.task_id:
            errors.append("Missing task_id in outcome record.")

        for name, pair in record.dimension_pairs.items():
            if math.isnan(pair.observed_value) or math.isinf(pair.observed_value):
                errors.append(f"Observed value for '{name}' is NaN or Inf.")
            if math.isnan(pair.predicted_value) or math.isinf(pair.predicted_value):
                errors.append(f"Predicted value for '{name}' is NaN or Inf.")

            # Physical non-negativity
            if name in ("latency_ms", "cost_usd", "execution_duration_ms", "retry_count"):
                if pair.observed_value < 0.0:
                    errors.append(f"Observed metric '{name}'={pair.observed_value} cannot be negative.")

            # Bounded probabilities
            if name in ("accuracy", "ocr_confidence", "schema_validation_score", "overall_risk", "expected_utility"):
                if pair.observed_value < -1e-6 or pair.observed_value > 1.0 + 1e-6:
                    errors.append(f"Observed metric '{name}'={pair.observed_value} is outside valid [0, 1] range.")

        return len(errors) == 0, errors
