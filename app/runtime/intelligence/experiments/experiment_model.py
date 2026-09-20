"""
Experimentation & A/B Validation Models for Phase 10 (AISLCOP).

Defines structured experimental runs, trials, and statistical comparison results.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ExperimentStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    CONCLUDED = "CONCLUDED"
    FAILED = "FAILED"


@dataclass
class TrialResult:
    trial_id: str
    variant: str  # CONTROL or CANDIDATE
    latency_ms: float
    cost_usd: float
    confidence: float
    retries_count: int
    validation_passed: bool
    evidence_hash: str


@dataclass
class StatisticalComparisonResult:
    metric_name: str
    control_mean: float
    candidate_mean: float
    delta_abs: float
    delta_pct: float
    t_statistic: float
    p_value: float
    is_significant: bool  # p_value < 0.05
    cohens_d: float
    ci_lower: float
    ci_upper: float


@dataclass
class ExperimentRun:
    """
    Formal experimental verification comparing Control vs Candidate strategies.
    """
    experiment_id: str
    title: str
    hypothesis_id: str
    control_strategy_id: str
    candidate_strategy_id: str
    sample_size_per_variant: int = 10
    status: ExperimentStatus = ExperimentStatus.PENDING
    created_at: float = field(default_factory=time.time)
    concluded_at: Optional[float] = None
    
    # Raw Trial Results
    control_trials: List[TrialResult] = field(default_factory=list)
    candidate_trials: List[TrialResult] = field(default_factory=list)
    
    # Statistical Metrics
    latency_comparison: Optional[StatisticalComparisonResult] = None
    cost_comparison: Optional[StatisticalComparisonResult] = None
    confidence_comparison: Optional[StatisticalComparisonResult] = None
    retry_comparison: Optional[StatisticalComparisonResult] = None
    
    # Overall Outcome & Promotion Justification
    promotes_candidate: bool = False
    verdict_summary: str = ""
    run_hash: str = ""

    def __post_init__(self):
        if not self.run_hash:
            self.run_hash = self.compute_hash()

    def compute_hash(self) -> str:
        payload = {
            "experiment_id": self.experiment_id,
            "hypothesis_id": self.hypothesis_id,
            "control_strategy_id": self.control_strategy_id,
            "candidate_strategy_id": self.candidate_strategy_id,
            "promotes_candidate": self.promotes_candidate,
            "created_at": self.created_at,
        }
        raw = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if isinstance(self.status, Enum):
            data["status"] = self.status.value
        return data
