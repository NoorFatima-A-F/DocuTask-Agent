"""
Planner Version Config and Version Manager for Phase 10 (AISLCOP).

Provides deterministic, versioned, and auditable parameter configurations
with 1-click rollback capabilities.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlannerVersionConfig:
    version_id: str  # e.g., v1.0.0, v1.1.0
    created_at: float = field(default_factory=time.time)
    parent_version_id: Optional[str] = None
    status: str = "ACTIVE"  # ACTIVE, CANDIDATE, ARCHIVED, ROLLED_BACK
    
    # Planner Hyperparameters & Coefficients
    exploration_weight: float = 0.20
    latency_penalty_factor: float = 0.40
    cost_penalty_factor: float = 0.30
    confidence_threshold: float = 0.90
    max_dag_depth: int = 5
    max_retries: int = 3
    parallel_fanout_limit: int = 4
    
    # Tool Selection & Routing Preferences
    default_ocr_engine: str = "tesseract_v2"
    high_precision_model: str = "gemini-1.5-pro"
    fast_tier_model: str = "gemini-1.5-flash"
    
    # Scientific Justification & Lineage
    justification: str = "Baseline production configuration"
    supporting_experiment_id: Optional[str] = None
    statistical_p_value: Optional[float] = None
    expected_improvement_pct: float = 0.0
    config_hash: str = ""

    def __post_init__(self):
        if not self.config_hash:
            self.config_hash = self.compute_hash()

    def compute_hash(self) -> str:
        payload = {
            "version_id": self.version_id,
            "exploration_weight": self.exploration_weight,
            "latency_penalty_factor": self.latency_penalty_factor,
            "cost_penalty_factor": self.cost_penalty_factor,
            "confidence_threshold": self.confidence_threshold,
            "default_ocr_engine": self.default_ocr_engine,
            "high_precision_model": self.high_precision_model,
        }
        raw = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PlannerVersionManager:
    """
    Manages historical, active, and candidate planner parameter versions.
    """

    def __init__(self):
        self._versions: Dict[str, PlannerVersionConfig] = {}
        self._active_version_id: str = "v1.0.0"
        
        # Initialize default baseline v1.0.0
        baseline = PlannerVersionConfig(
            version_id="v1.0.0",
            status="ACTIVE",
            justification="Initial baseline configuration",
        )
        self.register_version(baseline)

    def register_version(self, config: PlannerVersionConfig) -> str:
        self._versions[config.version_id] = config
        if config.status == "ACTIVE":
            # Deactivate previous
            if self._active_version_id != config.version_id and self._active_version_id in self._versions:
                self._versions[self._active_version_id].status = "ARCHIVED"
            self._active_version_id = config.version_id
        return config.version_id

    def get_active(self) -> PlannerVersionConfig:
        return self._versions[self._active_version_id]

    def get(self, version_id: str) -> Optional[PlannerVersionConfig]:
        return self._versions.get(version_id)

    def list_versions(self) -> List[PlannerVersionConfig]:
        return list(self._versions.values())

    def rollback(self, target_version_id: str) -> Optional[PlannerVersionConfig]:
        """Roll back active configuration to target historical version."""
        if target_version_id not in self._versions:
            return None
            
        current = self.get_active()
        current.status = "ROLLED_BACK"
        
        target = self._versions[target_version_id]
        target.status = "ACTIVE"
        self._active_version_id = target_version_id
        return target
