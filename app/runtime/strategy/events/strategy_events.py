"""
Phase 13.11: Autonomous Strategic Cognition, Goal Evolution & Executive Intelligence Platform (ASC-GEEIP)
Domain Events and Enums.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class GoalPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    BACKGROUND = "BACKGROUND"


class GoalStatus(str, Enum):
    PROPOSED = "PROPOSED"
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    REFINING = "REFINING"
    COMPLETED = "COMPLETED"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


class StrategicHorizon(str, Enum):
    DAYS_30 = "DAYS_30"
    DAYS_90 = "DAYS_90"
    DAYS_180 = "DAYS_180"
    DAYS_365 = "DAYS_365"
    MULTI_YEAR = "MULTI_YEAR"


class DecisionImportance(str, Enum):
    TIER_1_EXECUTIVE = "TIER_1_EXECUTIVE"
    TIER_2_DEPARTMENTAL = "TIER_2_DEPARTMENTAL"
    TIER_3_TACTICAL = "TIER_3_TACTICAL"
    TIER_4_OPERATIONAL = "TIER_4_OPERATIONAL"


class MissionValue(str, Enum):
    TRANSFORMATIVE = "TRANSFORMATIVE"
    CORE_REVENUE = "CORE_REVENUE"
    EFFICIENCY_GAIN = "EFFICIENCY_GAIN"
    RISK_MITIGATION = "RISK_MITIGATION"
    EXPLORATORY = "EXPLORATORY"


class PortfolioStatus(str, Enum):
    BALANCED = "BALANCED"
    OVERALLOCATED = "OVERALLOCATED"
    RESOURCE_CONSTRAINED = "RESOURCE_CONSTRAINED"
    HIGH_RISK = "HIGH_RISK"
    OPTIMAL = "OPTIMAL"


class NegotiationStatus(str, Enum):
    PROPOSED = "PROPOSED"
    COUNTER_OFFERED = "COUNTER_OFFERED"
    CONVERGED = "CONVERGED"
    DEADLOCKED = "DEADLOCKED"
    SETTLED = "SETTLED"


@dataclass
class StrategicDomainEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = "STRATEGIC_EVENT"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_component: str = "executive_strategy_runtime"
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StrategicGoalCreated(StrategicDomainEvent):
    event_type: str = "StrategicGoalCreated"
    goal_id: str = ""
    title: str = ""
    priority: GoalPriority = GoalPriority.HIGH
    horizon: StrategicHorizon = StrategicHorizon.DAYS_90


@dataclass
class StrategicGoalArchived(StrategicDomainEvent):
    event_type: str = "StrategicGoalArchived"
    goal_id: str = ""
    reason: str = ""


@dataclass
class GoalPriorityChanged(StrategicDomainEvent):
    event_type: str = "GoalPriorityChanged"
    goal_id: str = ""
    previous_priority: GoalPriority = GoalPriority.MEDIUM
    new_priority: GoalPriority = GoalPriority.HIGH
    rationale: str = ""


@dataclass
class MissionPortfolioOptimized(StrategicDomainEvent):
    event_type: str = "MissionPortfolioOptimized"
    portfolio_id: str = ""
    total_missions: int = 0
    pareto_rank: int = 1
    expected_utility: float = 0.0


@dataclass
class StrategicConflictDetected(StrategicDomainEvent):
    event_type: str = "StrategicConflictDetected"
    conflict_id: str = ""
    conflicting_goal_ids: List[str] = field(default_factory=list)
    resource_type: str = ""
    severity: str = "HIGH"


@dataclass
class StrategySimulationStarted(StrategicDomainEvent):
    event_type: str = "StrategySimulationStarted"
    simulation_id: str = ""
    horizon: StrategicHorizon = StrategicHorizon.DAYS_90
    scenario_type: str = "QUARTERLY_ALIGNMENT"


@dataclass
class StrategySimulationCompleted(StrategicDomainEvent):
    event_type: str = "StrategySimulationCompleted"
    simulation_id: str = ""
    expected_roi_multiplier: float = 1.0
    risk_score: float = 0.0


@dataclass
class RoadmapGenerated(StrategicDomainEvent):
    event_type: str = "RoadmapGenerated"
    roadmap_id: str = ""
    milestone_count: int = 0
    horizon: StrategicHorizon = StrategicHorizon.DAYS_90


@dataclass
class RoadmapUpdated(StrategicDomainEvent):
    event_type: str = "RoadmapUpdated"
    roadmap_id: str = ""
    delta_summary: str = ""


@dataclass
class InvestmentRecommendationGenerated(StrategicDomainEvent):
    event_type: str = "InvestmentRecommendationGenerated"
    recommendation_id: str = ""
    target_area: str = ""
    allocated_budget_usd: float = 0.0
    expected_gain_pct: float = 0.0


@dataclass
class ExecutiveDecisionCreated(StrategicDomainEvent):
    event_type: str = "ExecutiveDecisionCreated"
    decision_id: str = ""
    title: str = ""
    importance: DecisionImportance = DecisionImportance.TIER_1_EXECUTIVE
    utility_score: float = 0.0


@dataclass
class ResourceNegotiationCompleted(StrategicDomainEvent):
    event_type: str = "ResourceNegotiationCompleted"
    negotiation_id: str = ""
    participating_swarms: List[str] = field(default_factory=list)
    converged: bool = True
    nash_product: float = 0.0


@dataclass
class LongTermObjectiveLearned(StrategicDomainEvent):
    event_type: str = "LongTermObjectiveLearned"
    objective_id: str = ""
    discovered_insight: str = ""


@dataclass
class GoalEvolutionCompleted(StrategicDomainEvent):
    event_type: str = "GoalEvolutionCompleted"
    generation: int = 1
    evolved_goals_count: int = 0


@dataclass
class StrategicRiskAccepted(StrategicDomainEvent):
    event_type: str = "StrategicRiskAccepted"
    risk_id: str = ""
    justification: str = ""


@dataclass
class StrategicRiskRejected(StrategicDomainEvent):
    event_type: str = "StrategicRiskRejected"
    risk_id: str = ""
    mitigation_mandate: str = ""


@dataclass
class StrategicPlanApproved(StrategicDomainEvent):
    event_type: str = "StrategicPlanApproved"
    plan_id: str = ""
    approver_hash: str = ""
    cryptographic_signature: str = ""


@dataclass
class StrategicPlanRejected(StrategicDomainEvent):
    event_type: str = "StrategicPlanRejected"
    plan_id: str = ""
    rejection_reasons: List[str] = field(default_factory=list)


@dataclass
class StrategicExecutionStarted(StrategicDomainEvent):
    event_type: str = "StrategicExecutionStarted"
    execution_id: str = ""
    roadmap_id: str = ""


@dataclass
class StrategicExecutionCompleted(StrategicDomainEvent):
    event_type: str = "StrategicExecutionCompleted"
    execution_id: str = ""
    status: str = "SUCCESS"
