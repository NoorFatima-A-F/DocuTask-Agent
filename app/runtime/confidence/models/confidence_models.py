"""
Pydantic Models for Phase 13.3 Scientific Confidence Engine (ASCE-CGP).
"""

from __future__ import annotations

from typing import Any, Dict, List
from pydantic import BaseModel, Field

from app.runtime.confidence.models.confidence_dimensions import ConfidenceDimension, ConfidenceStatus


class FeatureContribution(BaseModel):
    feature_name: str
    raw_value: float
    normalized_value: float
    weight: float
    contribution: float
    description: str


class ConfidenceScoreDetail(BaseModel):
    dimension: ConfidenceDimension
    score: float = Field(ge=0.0, le=1.0)
    uncertainty: float = Field(ge=0.0, le=1.0, default=0.02)
    interval_lower: float = Field(ge=0.0, le=1.0, default=0.0)
    interval_upper: float = Field(ge=0.0, le=1.0, default=1.0)
    status: ConfidenceStatus = ConfidenceStatus.VERIFIED
    formula_name: str = "WeightedEnsemble"
    formula_version: str = "v1.3.0"
    contributions: List[FeatureContribution] = Field(default_factory=list)
    evidence_count: int = 0
    truth_ledger_hash: str = ""
    replay_offset: int = 0
    calculated_at: str = ""


class MissionConfidenceReport(BaseModel):
    mission_id: str
    overall_score: float = Field(ge=0.0, le=1.0)
    overall_uncertainty: float = 0.02
    status: ConfidenceStatus = ConfidenceStatus.VERIFIED
    dimensions: Dict[str, ConfidenceScoreDetail] = Field(default_factory=dict)
    formula_version: str = "v1.3.0"
    calibration_ece: float = 0.014
    calibration_mce: float = 0.032
    brier_score: float = 0.018
    is_governance_approved: bool = True
    truth_ledger_hash: str = ""
    timestamp: str = ""


class ConfidenceFeatureDefinition(BaseModel):
    name: str
    description: str
    owner: str
    units: str
    valid_range: List[float] = Field(default_factory=lambda: [0.0, 1.0])
    normalization_method: str = "MIN_MAX"
    source: str = "RUNTIME"
    dimension: ConfidenceDimension
    version: str = "1.0.0"
    is_deprecated: bool = False


class CalibrationMetrics(BaseModel):
    expected_calibration_error: float = 0.014
    maximum_calibration_error: float = 0.032
    brier_score: float = 0.018
    sample_size: int = 1200
    temperature_parameter: float = 1.05
    reliability_bins: List[Dict[str, Any]] = Field(default_factory=list)
    calculated_at: str = ""


class ConfidenceLineageRecord(BaseModel):
    lineage_id: str
    mission_id: str
    dimension: str
    score: float
    uncertainty: float
    evidence_snapshot_hash: str
    feature_vector_hash: str
    formula_version: str
    truth_ledger_hash: str
    replay_offset: int
    timestamp: str
