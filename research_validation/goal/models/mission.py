"""
Immutable Mission & Mission Graph Domain Models
===============================================
Defines the Mission entity and its hierarchical Mission Graph structure:
Mission -> Objectives -> Milestones -> Subgoals -> Tasks -> Actions.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

from research_validation.goal.models.mission_state import MissionState, StateTransitionRecord
from research_validation.goal.models.goal import Goal, PriorityLevel
from research_validation.goal.models.execution_budget import ExecutionBudget
from research_validation.goal.models.risk_profile import RiskProfile
from research_validation.goal.models.mission_metrics import MissionMetrics
from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class MissionNode:
    """Base immutable node in the hierarchical mission graph."""
    node_id: str
    parent_id: Optional[str]
    title: str
    description: str
    priority: PriorityLevel
    estimated_duration_hours: float
    confidence_target: float
    required_capabilities: Tuple[str, ...]
    expected_evidence: Tuple[str, ...]
    dependencies: Tuple[str, ...] = ()
    custom_attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ActionNode(MissionNode):
    """Atomic executable action step within a task."""
    tool_or_executor: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TaskNode(MissionNode):
    """A cohesive unit of work composed of actions."""
    actions: Tuple[ActionNode, ...] = ()


@dataclass(frozen=True)
class SubgoalNode(MissionNode):
    """A sub-objective delivering specific scientific sub-outcomes."""
    tasks: Tuple[TaskNode, ...] = ()


@dataclass(frozen=True)
class MilestoneNode(MissionNode):
    """A major intermediate scientific checkpoint."""
    subgoals: Tuple[SubgoalNode, ...] = ()


@dataclass(frozen=True)
class ObjectiveNode(MissionNode):
    """A high-level strategic objective derived from the user goal."""
    milestones: Tuple[MilestoneNode, ...] = ()


@dataclass(frozen=True)
class Mission:
    """
    Authoritative immutable Mission entity representing a fully validated,
    measurable, and planned scientific research campaign.
    """
    mission_id: str
    goal_id: str
    title: str
    description: str
    version: str
    state: MissionState
    goal: Goal
    objectives: Tuple[ObjectiveNode, ...]
    execution_budget: ExecutionBudget
    risk_profile: RiskProfile
    metrics: MissionMetrics
    state_history: Tuple[StateTransitionRecord, ...]
    created_at_utc: str
    updated_at_utc: str
    author: str = "GOAL_INTELLIGENCE_ENGINE"
    previous_version_hash: str = ""
    mission_digest_sha256: str = field(default="")

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "goal_id": self.goal_id,
            "title": self.title,
            "version": self.version,
            "state": self.state.value,
            "goal_digest": self.goal.cryptographic_digest_sha256,
            "objectives_count": len(self.objectives),
            "expected_runtime_hours": self.execution_budget.expected_runtime_hours,
            "overall_risk_score": self.risk_profile.overall_risk_score,
            "created_at_utc": self.created_at_utc,
            "author": self.author,
            "previous_version_hash": self.previous_version_hash,
        }

    def compute_digest(self) -> str:
        return hash_canonical_json(self.canonical_dict())
