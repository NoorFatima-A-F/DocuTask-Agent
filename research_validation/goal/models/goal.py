"""
Immutable Goal Domain Model
===========================
Defines the authoritative immutable Goal entity containing all 30+ scientific,
governance, budget, capability, and validation attributes.
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from research_validation.goal.models.confidence_threshold import ConfidenceThreshold, ConfidenceLevel
from research_validation.goal.models.goal_constraints import GoalConstraints
from research_validation.goal.models.success_criteria import SuccessCriterion
from research_validation.goal.models.stopping_condition import StoppingCondition
from research_validation.goal.models.capability_requirement import CapabilityRequirement
from research_validation.goal.models.dependency import GoalDependency
from research_validation.goal.models.risk_profile import RiskProfile
from research_validation.goal.models.evidence_requirement import EvidenceRequirement
from research_validation.provenance.hashing import hash_canonical_json


class GoalType(str, Enum):
    DOCUMENT_EXTRACTION = "DOCUMENT_EXTRACTION"
    MODEL_EVALUATION = "MODEL_EVALUATION"
    BENCHMARK = "BENCHMARK"
    DATA_VALIDATION = "DATA_VALIDATION"
    HYPOTHESIS_TESTING = "HYPOTHESIS_TESTING"
    RESEARCH = "RESEARCH"
    OPTIMIZATION = "OPTIMIZATION"
    PERFORMANCE = "PERFORMANCE"
    REGRESSION = "REGRESSION"
    COMPLIANCE = "COMPLIANCE"
    PUBLICATION = "PUBLICATION"
    CUSTOM = "CUSTOM"


class PriorityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    LOW = "LOW"
    BACKGROUND = "BACKGROUND"


class GoalStatus(str, Enum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"


@dataclass(frozen=True)
class Goal:
    """Authoritative, immutable Goal entity representing a complete user scientific objective."""
    goal_id: str
    mission_id: str
    title: str
    description: str
    objective: str
    problem_statement: str
    goal_type: GoalType
    priority: PriorityLevel
    owner: str
    creation_timestamp_utc: str
    version: str = "1.0.0"
    status: GoalStatus = GoalStatus.DRAFT
    confidence_threshold: ConfidenceThreshold = field(default_factory=lambda: ConfidenceThreshold(ConfidenceLevel.HIGH))
    completion_threshold: float = 1.0  # 0.0 to 1.0 fraction of criteria
    maximum_runtime_hours: float = 24.0
    maximum_cost_usd: float = 100.0
    maximum_iterations: int = 50
    expected_outputs: Tuple[str, ...] = ()
    expected_artifacts: Tuple[str, ...] = ()
    expected_evidence: EvidenceRequirement = field(default_factory=EvidenceRequirement)
    required_datasets: Tuple[str, ...] = ()
    required_models: Tuple[str, ...] = ()
    required_tools: Tuple[str, ...] = ()
    required_compute: str = "AUTO"
    required_permissions: Tuple[str, ...] = ()
    constraints: GoalConstraints = field(default_factory=GoalConstraints)
    dependencies: Tuple[GoalDependency, ...] = ()
    success_metrics: Tuple[SuccessCriterion, ...] = ()
    evaluation_metrics: Tuple[str, ...] = ()
    acceptance_criteria: Tuple[str, ...] = ()
    stopping_conditions: Tuple[StoppingCondition, ...] = ()
    risk_profile: Optional[RiskProfile] = None
    capability_requirements: Tuple[CapabilityRequirement, ...] = ()
    governance_policies: Tuple[str, ...] = ()
    audit_metadata: Dict[str, Any] = field(default_factory=dict)
    cryptographic_digest_sha256: str = field(default="")

    def canonical_dict(self) -> Dict[str, Any]:
        """Lossless canonical dictionary representation for hashing and serialization."""
        return {
            "goal_id": self.goal_id,
            "mission_id": self.mission_id,
            "title": self.title,
            "description": self.description,
            "objective": self.objective,
            "problem_statement": self.problem_statement,
            "goal_type": self.goal_type.value,
            "priority": self.priority.value,
            "owner": self.owner,
            "creation_timestamp_utc": self.creation_timestamp_utc,
            "version": self.version,
            "status": self.status.value,
            "confidence_threshold": self.confidence_threshold.value,
            "completion_threshold": self.completion_threshold,
            "maximum_runtime_hours": self.maximum_runtime_hours,
            "maximum_cost_usd": self.maximum_cost_usd,
            "maximum_iterations": self.maximum_iterations,
            "expected_outputs": list(self.expected_outputs),
            "expected_artifacts": list(self.expected_artifacts),
            "required_datasets": list(self.required_datasets),
            "required_models": list(self.required_models),
            "required_tools": list(self.required_tools),
            "required_compute": self.required_compute,
            "required_permissions": list(self.required_permissions),
            "governance_policies": list(self.governance_policies),
            "audit_metadata": self.audit_metadata,
        }

    def compute_digest(self) -> str:
        """Calculates canonical SHA-256 digest over all core immutable fields."""
        return hash_canonical_json(self.canonical_dict())
