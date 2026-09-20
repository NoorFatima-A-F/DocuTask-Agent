"""
Strategy Model for Phase 10 (AISLCOP).

Defines structured execution strategies mined from operational experience.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class MetricDistribution:
    mean: float
    std_dev: float
    min_val: float
    max_val: float
    p50: float
    p95: float


@dataclass
class ExecutionStrategy:
    """
    Reusable execution strategy mined from validated experience records.
    """
    strategy_id: str
    name: str
    document_domain: str
    target_task: str
    version: str = "1.0.0"
    is_promoted: bool = False
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    
    # Requirements & Capabilities
    required_capabilities: List[str] = field(default_factory=list)
    recommended_tools: List[str] = field(default_factory=list)
    preferred_models: List[str] = field(default_factory=lambda: ["gemini-1.5-pro", "gemini-1.5-flash"])
    dag_template_nodes: List[str] = field(default_factory=list)
    
    # Statistical Performance Profiles
    sample_size: int = 1
    observed_success_rate: float = 0.98
    latency_profile: MetricDistribution = field(
        default_factory=lambda: MetricDistribution(mean=1200.0, std_dev=150.0, min_val=900.0, max_val=1600.0, p50=1180.0, p95=1450.0)
    )
    cost_profile: MetricDistribution = field(
        default_factory=lambda: MetricDistribution(mean=0.012, std_dev=0.003, min_val=0.008, max_val=0.020, p50=0.011, p95=0.018)
    )
    confidence_profile: MetricDistribution = field(
        default_factory=lambda: MetricDistribution(mean=0.95, std_dev=0.03, min_val=0.88, max_val=0.99, p50=0.96, p95=0.98)
    )
    retry_frequency: float = 0.05
    
    # Failure Modes & Prerequisites
    known_failure_modes: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    
    # Evidence & Lineage
    supporting_experience_ids: List[str] = field(default_factory=list)
    supporting_evidence_hashes: List[str] = field(default_factory=list)
    strategy_hash: str = ""

    def __post_init__(self):
        if not self.strategy_hash:
            self.strategy_hash = self.compute_hash()

    def compute_hash(self) -> str:
        payload = {
            "strategy_id": self.strategy_id,
            "name": self.name,
            "document_domain": self.document_domain,
            "version": self.version,
            "required_capabilities": sorted(self.required_capabilities),
            "observed_success_rate": self.observed_success_rate,
            "supporting_experience_ids": sorted(self.supporting_experience_ids),
        }
        raw = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
