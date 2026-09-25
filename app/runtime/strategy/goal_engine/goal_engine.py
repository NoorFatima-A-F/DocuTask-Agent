"""
Goal Evolution Engine for Phase 13.11 (ASC-GEEIP).
Hierarchical Task Network (HTN) and GOAP Goal Decomposition and Evolution.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.strategy.events.strategy_events import (
    GoalPriority,
    GoalStatus,
    StrategicHorizon,
    MissionValue,
    StrategicGoalCreated,
    StrategicGoalArchived,
    GoalPriorityChanged,
    StrategicConflictDetected,
    GoalEvolutionCompleted,
)


@dataclass
class GoalDependency:
    source_goal_id: str
    target_goal_id: str
    dependency_type: str = "BLOCKING"  # "BLOCKING" | "ENABLING" | "SYNERGISTIC"
    criticality: float = 0.85


@dataclass
class StrategicGoal:
    goal_id: str = field(default_factory=lambda: f"goal-{uuid.uuid4().hex[:8]}")
    title: str = ""
    description: str = ""
    parent_goal_id: Optional[str] = None
    priority: GoalPriority = GoalPriority.HIGH
    status: GoalStatus = GoalStatus.ACTIVE
    horizon: StrategicHorizon = StrategicHorizon.DAYS_90
    value_type: MissionValue = MissionValue.EFFICIENCY_GAIN
    utility_score: float = 0.85
    confidence: float = 0.95
    age_days: int = 0
    estimated_cost_usd: float = 500.0
    expected_latency_reduction_pct: float = 15.0
    decomposed_subgoal_ids: List[str] = field(default_factory=list)
    dependencies: List[GoalDependency] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal_id": self.goal_id,
            "title": self.title,
            "description": self.description,
            "parent_goal_id": self.parent_goal_id,
            "priority": self.priority.value if hasattr(self.priority, "value") else str(self.priority),
            "status": self.status.value if hasattr(self.status, "value") else str(self.status),
            "horizon": self.horizon.value if hasattr(self.horizon, "value") else str(self.horizon),
            "value_type": self.value_type.value if hasattr(self.value_type, "value") else str(self.value_type),
            "utility_score": round(self.utility_score, 4),
            "confidence": round(self.confidence, 4),
            "age_days": self.age_days,
            "estimated_cost_usd": self.estimated_cost_usd,
            "expected_latency_reduction_pct": self.expected_latency_reduction_pct,
            "decomposed_subgoal_ids": self.decomposed_subgoal_ids,
            "dependencies": [
                {
                    "source": d.source_goal_id,
                    "target": d.target_goal_id,
                    "type": d.dependency_type,
                    "criticality": d.criticality,
                }
                for d in self.dependencies
            ],
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class GoalTree:
    root_goals: List[StrategicGoal] = field(default_factory=list)
    all_goals: Dict[str, StrategicGoal] = field(default_factory=dict)

    def add_goal(self, goal: StrategicGoal) -> None:
        self.all_goals[goal.goal_id] = goal
        if not goal.parent_goal_id or goal.parent_goal_id not in self.all_goals:
            if goal not in self.root_goals:
                self.root_goals.append(goal)
        else:
            parent = self.all_goals[goal.parent_goal_id]
            if goal.goal_id not in parent.decomposed_subgoal_ids:
                parent.decomposed_subgoal_ids.append(goal.goal_id)

    def get_goal(self, goal_id: str) -> Optional[StrategicGoal]:
        return self.all_goals.get(goal_id)


class GoalEvolutionEngine:
    """
    Manages dynamic hierarchical goal decomposition, reprioritization,
    aging degradation, and utility-driven evolution.
    """

    def __init__(self) -> None:
        self.tree: GoalTree = GoalTree()
        self.event_log: List[Any] = []
        self._initialize_bootstrap_goals()

    def _initialize_bootstrap_goals(self) -> None:
        # 1. Root: Autonomous Processing Scale-Out
        root1 = StrategicGoal(
            goal_id="goal-root-scale-100k",
            title="Scale Multi-Swarm Processing to 100k Daily Documents",
            description="Expand agentic extraction capacity with sub-250ms SLA and zero accuracy degradation.",
            parent_goal_id=None,
            priority=GoalPriority.CRITICAL,
            status=GoalStatus.ACTIVE,
            horizon=StrategicHorizon.DAYS_90,
            value_type=MissionValue.TRANSFORMATIVE,
            utility_score=0.965,
            confidence=0.982,
            age_days=12,
            estimated_cost_usd=2400.0,
            expected_latency_reduction_pct=35.0,
            tags=["scalability", "swarm", "throughput"],
        )
        self.tree.add_goal(root1)

        # 1a. Subgoal: Caching optimization
        sub1 = StrategicGoal(
            goal_id="goal-sub-cache-warm",
            title="Deploy Speculative Zero-Copy Embedding Cache",
            description="Pre-compute document layout representations across recurrent corporate invoice templates.",
            parent_goal_id="goal-root-scale-100k",
            priority=GoalPriority.HIGH,
            status=GoalStatus.ACTIVE,
            horizon=StrategicHorizon.DAYS_30,
            value_type=MissionValue.EFFICIENCY_GAIN,
            utility_score=0.920,
            confidence=0.990,
            age_days=5,
            estimated_cost_usd=450.0,
            expected_latency_reduction_pct=22.0,
            tags=["caching", "latency", "gpu"],
        )
        self.tree.add_goal(sub1)

        # 1b. Subgoal: Specialist strike team coalition
        sub2 = StrategicGoal(
            goal_id="goal-sub-strike-teams",
            title="Form Triadic Specialist Swarm Strike Teams",
            description="Pre-cluster extraction workers by document taxonomy to reduce inter-agent bidding friction.",
            parent_goal_id="goal-root-scale-100k",
            priority=GoalPriority.HIGH,
            status=GoalStatus.ACTIVE,
            horizon=StrategicHorizon.DAYS_30,
            value_type=MissionValue.CORE_REVENUE,
            utility_score=0.895,
            confidence=0.975,
            age_days=7,
            estimated_cost_usd=600.0,
            expected_latency_reduction_pct=18.0,
            tags=["swarm", "coalition", "specialist"],
        )
        sub2.dependencies.append(
            GoalDependency(
                source_goal_id=sub2.goal_id,
                target_goal_id=sub1.goal_id,
                dependency_type="ENABLING",
                criticality=0.8,
            )
        )
        self.tree.add_goal(sub2)

        # 2. Root: Autonomous Self-Governance & Truth Integrity
        root2 = StrategicGoal(
            goal_id="goal-root-gov-integrity",
            title="Attain Continuous 100% Cryptographic Auditability",
            description="Ensure all autonomous interventions have SHA-256 state proofs and instant rollback points.",
            parent_goal_id=None,
            priority=GoalPriority.CRITICAL,
            status=GoalStatus.ACTIVE,
            horizon=StrategicHorizon.DAYS_180,
            value_type=MissionValue.RISK_MITIGATION,
            utility_score=0.980,
            confidence=0.995,
            age_days=25,
            estimated_cost_usd=1200.0,
            expected_latency_reduction_pct=0.0,
            tags=["governance", "cryptography", "safety"],
        )
        self.tree.add_goal(root2)

    def create_goal(
        self,
        title: str,
        description: str,
        parent_goal_id: Optional[str] = None,
        priority: GoalPriority = GoalPriority.HIGH,
        horizon: StrategicHorizon = StrategicHorizon.DAYS_90,
        value_type: MissionValue = MissionValue.EFFICIENCY_GAIN,
        estimated_cost_usd: float = 500.0,
        expected_latency_reduction_pct: float = 10.0,
        tags: Optional[List[str]] = None,
    ) -> StrategicGoal:
        goal = StrategicGoal(
            title=title,
            description=description,
            parent_goal_id=parent_goal_id,
            priority=priority,
            horizon=horizon,
            value_type=value_type,
            estimated_cost_usd=estimated_cost_usd,
            expected_latency_reduction_pct=expected_latency_reduction_pct,
            tags=tags or [],
        )
        self.tree.add_goal(goal)
        event = StrategicGoalCreated(
            goal_id=goal.goal_id,
            title=goal.title,
            priority=goal.priority,
            horizon=goal.horizon,
            payload=goal.to_dict(),
        )
        self.event_log.append(event)
        return goal

    def decompose_goal(self, goal_id: str, subtasks: List[Dict[str, Any]]) -> List[StrategicGoal]:
        """
        Hierarchical Task Network (HTN) decomposition of a complex goal into executable subgoals.
        """
        parent = self.tree.get_goal(goal_id)
        if not parent:
            raise ValueError(f"Goal {goal_id} not found.")

        created_subgoals: List[StrategicGoal] = []
        for task in subtasks:
            sub = StrategicGoal(
                title=task.get("title", "Decomposed Action Task"),
                description=task.get("description", ""),
                parent_goal_id=parent.goal_id,
                priority=parent.priority,
                horizon=task.get("horizon", parent.horizon),
                value_type=task.get("value_type", parent.value_type),
                estimated_cost_usd=task.get("estimated_cost_usd", parent.estimated_cost_usd / max(len(subtasks), 1)),
                expected_latency_reduction_pct=task.get("expected_latency_reduction_pct", 5.0),
                tags=task.get("tags", parent.tags.copy()),
            )
            self.tree.add_goal(sub)
            created_subgoals.append(sub)

        parent.status = GoalStatus.REFINING
        parent.updated_at = datetime.now(timezone.utc).isoformat()
        return created_subgoals

    def calculate_utility(self, goal: StrategicGoal) -> float:
        """
        MCDA Multi-attribute utility:
        U = 0.40 * ValueWeight + 0.30 * Confidence - 0.15 * (Cost / 5000) - 0.15 * (Age / 100)
        """
        val_map = {
            MissionValue.TRANSFORMATIVE: 1.0,
            MissionValue.CORE_REVENUE: 0.85,
            MissionValue.EFFICIENCY_GAIN: 0.70,
            MissionValue.RISK_MITIGATION: 0.90,
            MissionValue.EXPLORATORY: 0.50,
        }
        val_score = val_map.get(goal.value_type, 0.7)
        cost_norm = min(goal.estimated_cost_usd / 5000.0, 1.0)
        age_norm = min(goal.age_days / 100.0, 1.0)

        utility = (0.40 * val_score) + (0.30 * goal.confidence) - (0.15 * cost_norm) - (0.15 * age_norm)
        return max(0.05, min(1.0, utility))

    def reprioritize_goals(self) -> List[StrategicGoal]:
        """
        Evaluates utility across all active goals and adjusts priority dynamically.
        """
        reprioritized: List[StrategicGoal] = []
        for goal in self.tree.all_goals.values():
            if goal.status in (GoalStatus.ARCHIVED, GoalStatus.DEPRECATED, GoalStatus.COMPLETED):
                continue

            goal.utility_score = self.calculate_utility(goal)
            old_priority = goal.priority

            if goal.utility_score >= 0.88:
                new_priority = GoalPriority.CRITICAL
            elif goal.utility_score >= 0.75:
                new_priority = GoalPriority.HIGH
            elif goal.utility_score >= 0.55:
                new_priority = GoalPriority.MEDIUM
            elif goal.utility_score >= 0.30:
                new_priority = GoalPriority.LOW
            else:
                new_priority = GoalPriority.BACKGROUND

            if new_priority != old_priority:
                goal.priority = new_priority
                goal.updated_at = datetime.now(timezone.utc).isoformat()
                event = GoalPriorityChanged(
                    goal_id=goal.goal_id,
                    previous_priority=old_priority,
                    new_priority=new_priority,
                    rationale=f"Updated based on utility score {goal.utility_score:.3f} and age {goal.age_days}d",
                )
                self.event_log.append(event)
                reprioritized.append(goal)

        return reprioritized

    def archive_goal(self, goal_id: str, reason: str = "Retired via strategic mandate") -> StrategicGoal:
        goal = self.tree.get_goal(goal_id)
        if not goal:
            raise ValueError(f"Goal {goal_id} not found.")
        goal.status = GoalStatus.ARCHIVED
        goal.updated_at = datetime.now(timezone.utc).isoformat()
        event = StrategicGoalArchived(goal_id=goal.goal_id, reason=reason)
        self.event_log.append(event)
        return goal

    def detect_conflicts(self) -> List[Dict[str, Any]]:
        """
        Checks for cyclic or contradictory dependencies.
        """
        conflicts = []
        visited = set()

        for goal in self.tree.all_goals.values():
            for dep in goal.dependencies:
                target = self.tree.get_goal(dep.target_goal_id)
                if not target:
                    continue
                # Check for reciprocal blocking
                for target_dep in target.dependencies:
                    if target_dep.target_goal_id == goal.goal_id and dep.dependency_type == "BLOCKING" and target_dep.dependency_type == "BLOCKING":
                        conflict_id = f"conflict-{goal.goal_id}-{target.goal_id}"
                        if conflict_id not in visited:
                            visited.add(conflict_id)
                            conflicts.append({
                                "conflict_id": conflict_id,
                                "goals": [goal.goal_id, target.goal_id],
                                "reason": "Mutual deadlocking dependency detected",
                                "severity": "CRITICAL",
                            })
                            self.event_log.append(
                                StrategicConflictDetected(
                                    conflict_id=conflict_id,
                                    conflicting_goal_ids=[goal.goal_id, target.goal_id],
                                    severity="CRITICAL",
                                )
                            )
        return conflicts

    def evolve_generation(self) -> Dict[str, Any]:
        """
        Runs one cycle of goal aging, reprioritization, and conflict detection.
        """
        for goal in self.tree.all_goals.values():
            if goal.status == GoalStatus.ACTIVE:
                goal.age_days += 1

        reprioritized = self.reprioritize_goals()
        conflicts = self.detect_conflicts()

        event = GoalEvolutionCompleted(
            generation=len(self.event_log) + 1,
            evolved_goals_count=len(reprioritized),
        )
        self.event_log.append(event)

        return {
            "total_goals": len(self.tree.all_goals),
            "reprioritized_count": len(reprioritized),
            "conflicts_detected": len(conflicts),
            "active_goals": [g.to_dict() for g in self.tree.all_goals.values() if g.status == GoalStatus.ACTIVE],
        }

    def list_goals(self, status: Optional[GoalStatus] = None) -> List[Dict[str, Any]]:
        goals = list(self.tree.all_goals.values())
        if status:
            goals = [g for g in goals if g.status == status]
        return [g.to_dict() for g in goals]
