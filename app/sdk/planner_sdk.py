"""Enterprise Agent SDK - Planner Abstractions."""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CandidatePlan:
    candidate_id: str
    strategy_name: str
    target_capabilities: List[str]
    estimated_cost_usd: float
    estimated_latency_ms: float
    expected_quality: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class BasePlanner(abc.ABC):
    @abc.abstractmethod
    def generate_candidates(
        self,
        mission_goal: str,
        constraints: Dict[str, Any],
        available_capabilities: List[str],
    ) -> List[CandidatePlan]:
        """Generate candidate execution plans based on goal and constraints."""
        pass

    @abc.abstractmethod
    def select_optimal_plan(
        self,
        candidates: List[CandidatePlan],
        utility_weights: Dict[str, float],
    ) -> CandidatePlan:
        """Select Pareto-optimal plan using mathematical utility function."""
        pass
