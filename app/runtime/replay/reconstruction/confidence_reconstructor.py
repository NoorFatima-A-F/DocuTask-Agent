"""
Confidence Reconstructor for Phase 13.4.
Rebuilds 13-dimension confidence scores, feature vectors, formula versions, and lineage records from events.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ReconstructedConfidenceState(BaseModel):
    current_score: float = 0.50
    calibrated_score: float = 0.50
    active_formula_version: str = "WeightedEnsemble (v1.3.0)"
    dimension_scores: Dict[str, float] = Field(default_factory=dict)
    feature_vector: Dict[str, float] = Field(default_factory=dict)
    confidence_interval_95: List[float] = Field(default_factory=lambda: [0.40, 0.60])
    aleatoric_uncertainty: float = 0.01
    epistemic_uncertainty: float = 0.05
    lineage_history: List[Dict[str, Any]] = Field(default_factory=list)


class ConfidenceReconstructor:
    """
    Reconstructs exact confidence progression and lineage chain from event store.
    """

    @classmethod
    def reconstruct_from_events(
        cls,
        events: List[Dict[str, Any]],
        target_cursor: Optional[int] = None,
    ) -> ReconstructedConfidenceState:
        state = ReconstructedConfidenceState()
        sliced = events[: (target_cursor + 1)] if target_cursor is not None else events

        for ev in sliced:
            evt_type = ev.get("event_type") or ev.get("type", "")
            payload = ev.get("payload", {})

            if "confidence.evaluated" in evt_type or "confidence.updated" in evt_type:
                state.current_score = payload.get("overall_score", state.current_score)
                state.calibrated_score = payload.get("calibrated_score", state.current_score)
                state.active_formula_version = payload.get("formula_version", state.active_formula_version)
                if "dimension_scores" in payload:
                    state.dimension_scores.update(payload["dimension_scores"])
                if "features" in payload:
                    state.feature_vector.update(payload["features"])
                if "confidence_interval_95" in payload:
                    state.confidence_interval_95 = payload["confidence_interval_95"]
                if "lineage_record" in payload:
                    state.lineage_history.append(payload["lineage_record"])
            elif "confidence.dimension" in evt_type:
                dim_name = payload.get("dimension")
                score = payload.get("score")
                if dim_name and score is not None:
                    state.dimension_scores[dim_name] = float(score)

        return state
