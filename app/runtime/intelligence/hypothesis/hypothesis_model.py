"""
Hypothesis Model for Phase 10 (AISLCOP).

Defines structured, testable hypotheses with empirical baselines and target deltas.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class HypothesisStatus(str, Enum):
    PROPOSED = "PROPOSED"
    IN_EXPERIMENT = "IN_EXPERIMENT"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"
    DEPLOYED = "DEPLOYED"


class HypothesisCategory(str, Enum):
    LATENCY_REDUCTION = "LATENCY_REDUCTION"
    COST_OPTIMIZATION = "COST_OPTIMIZATION"
    ACCURACY_ENHANCEMENT = "ACCURACY_ENHANCEMENT"
    RETRY_MINIMIZATION = "RETRY_MINIMIZATION"
    ROUTING_EFFICIENCY = "ROUTING_EFFICIENCY"


@dataclass
class Hypothesis:
    """
    Structured scientific hypothesis proposed for runtime optimization.
    """
    hypothesis_id: str
    title: str
    category: HypothesisCategory
    premise: str
    proposed_action: str
    target_metric: str  # e.g., latency_ms, cost_usd, retries_count, confidence
    
    # Baseline vs Expected
    baseline_value: float
    expected_value: float
    expected_improvement_pct: float
    
    # Status & Lifecycle
    status: HypothesisStatus = HypothesisStatus.PROPOSED
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    
    # Associated Artifacts & Lineage
    source_domain: str = "general"
    supporting_experience_ids: List[str] = field(default_factory=list)
    experiment_id: Optional[str] = None
    validation_p_value: Optional[float] = None
    hypothesis_hash: str = ""

    def __post_init__(self):
        if not self.hypothesis_hash:
            self.hypothesis_hash = self.compute_hash()

    def compute_hash(self) -> str:
        payload = {
            "hypothesis_id": self.hypothesis_id,
            "title": self.title,
            "category": self.category.value if isinstance(self.category, Enum) else self.category,
            "premise": self.premise,
            "proposed_action": self.proposed_action,
            "target_metric": self.target_metric,
            "baseline_value": self.baseline_value,
            "expected_value": self.expected_value,
        }
        raw = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if isinstance(self.category, Enum):
            data["category"] = self.category.value
        if isinstance(self.status, Enum):
            data["status"] = self.status.value
        return data
