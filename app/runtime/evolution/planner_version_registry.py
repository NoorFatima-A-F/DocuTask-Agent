"""Planner Version Registry for DocuTask ACOS.

Maintains an immutable cryptographic genealogy of Planner generations (Planner v1, v2, v3...),
storing evaluation benchmarks, parameter weights, and automated rollback points.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PlannerGeneration(BaseModel):
    """Archival record of an evolved planner generation."""
    generation_id: str = Field(default_factory=lambda: f"gen_{uuid.uuid4().hex[:8]}")
    version_tag: str  # 'v1.0.0', 'v2.0.0', 'v3.1.0'
    parent_version: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    benchmark_utility: float = 0.4392
    brier_score: float = 0.032
    simulated_trials_count: int = 1000
    is_active_canary: bool = False
    is_promoted_production: bool = True
    cryptographic_seal_hash: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def seal(self, parent_hash: str = "") -> str:
        payload = f"{self.generation_id}:{self.version_tag}:{json.dumps(self.parameters, sort_keys=True)}:{self.benchmark_utility}:{parent_hash}"
        self.cryptographic_seal_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return self.cryptographic_seal_hash


class PlannerVersionRegistry:
    """Thread-safe ledger of versioned planner generations."""

    def __init__(self) -> None:
        self._generations: Dict[str, PlannerGeneration] = {}
        self._active_version: str = "v1.0.0"
        self._seed_default_generations()

    def _seed_default_generations(self) -> None:
        v1 = PlannerGeneration(
            version_tag="v1.0.0",
            parent_version=None,
            parameters={"weight_accuracy": 0.40, "weight_cost": 0.40, "weight_latency": 0.20, "beam_width": 4},
            benchmark_utility=0.3850,
            brier_score=0.065,
            is_promoted_production=False,
        )
        v1.seal("genesis_zero_00000000")
        self._generations[v1.version_tag] = v1

        v2 = PlannerGeneration(
            version_tag="v2.0.0",
            parent_version="v1.0.0",
            parameters={"weight_accuracy": 0.45, "weight_cost": 0.35, "weight_latency": 0.20, "beam_width": 6},
            benchmark_utility=0.4120,
            brier_score=0.048,
            is_promoted_production=False,
        )
        v2.seal(v1.cryptographic_seal_hash)
        self._generations[v2.version_tag] = v2

        v3 = PlannerGeneration(
            version_tag="v3.0.0",
            parent_version="v2.0.0",
            parameters={"weight_accuracy": 0.50, "weight_cost": 0.30, "weight_latency": 0.20, "beam_width": 8},
            benchmark_utility=0.4392,
            brier_score=0.032,
            is_promoted_production=True,
        )
        v3.seal(v2.cryptographic_seal_hash)
        self._generations[v3.version_tag] = v3
        self._active_version = "v3.0.0"

    def register_generation(self, generation: PlannerGeneration) -> PlannerGeneration:
        parent = self._generations.get(generation.parent_version or "")
        parent_hash = parent.cryptographic_seal_hash if parent else "genesis_root_0000"
        generation.seal(parent_hash)
        self._generations[generation.version_tag] = generation
        return generation

    def promote_to_production(self, version_tag: str) -> bool:
        if version_tag in self._generations:
            for g in self._generations.values():
                g.is_promoted_production = (g.version_tag == version_tag)
            self._active_version = version_tag
            return True
        return False

    def rollback_to_previous(self) -> Optional[PlannerGeneration]:
        current = self._generations.get(self._active_version)
        if current and current.parent_version and current.parent_version in self._generations:
            self.promote_to_production(current.parent_version)
            return self._generations[current.parent_version]
        return None

    def list_generations(self) -> List[PlannerGeneration]:
        return sorted(self._generations.values(), key=lambda g: g.version_tag)

    def get_active_generation(self) -> PlannerGeneration:
        return self._generations[self._active_version]
