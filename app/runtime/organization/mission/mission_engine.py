"""
Phase 13.14 - Autonomous Mission Understanding Engine
Converts human / enterprise strategic goals into machine-executable missions with KPIs, constraints, and dependencies.
"""

from __future__ import annotations
import time
import uuid
import re
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from app.runtime.organization.events.organization_events import (
    MissionPriority,
    OrganizationState,
    AgentRole,
    DecisionConfidence,
    MissionCreated,
    MissionValidated,
    org_event_bus,
)


class MissionMetric(BaseModel):
    metric_id: str = Field(default_factory=lambda: f"met_{uuid.uuid4().hex[:8]}")
    name: str
    baseline_value: float
    current_value: float
    target_value: float
    unit: str
    direction: str = "HIGHER_IS_BETTER"  # HIGHER_IS_BETTER or LOWER_IS_BETTER


class MissionConstraint(BaseModel):
    constraint_id: str = Field(default_factory=lambda: f"con_{uuid.uuid4().hex[:8]}")
    description: str
    constraint_type: str  # SLA, ACCURACY, BUDGET, COMPLIANCE, TIME
    threshold_value: float
    unit: str
    is_strict: bool = True


class MissionObjective(BaseModel):
    objective_id: str = Field(default_factory=lambda: f"obj_{uuid.uuid4().hex[:8]}")
    title: str
    description: str
    target_metric: str
    target_value: float
    current_value: float = 0.0
    weight: float = 1.0
    status: str = "PENDING"  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    progress_percent: float = 0.0


class Mission(BaseModel):
    mission_id: str = Field(default_factory=lambda: f"msn_{uuid.uuid4().hex[:8]}")
    title: str
    raw_goal: str
    priority: MissionPriority = MissionPriority.HIGH
    state: OrganizationState = OrganizationState.CREATED
    timeline_days: int = 90
    required_capabilities: List[str] = Field(default_factory=list)
    assigned_roles: List[AgentRole] = Field(default_factory=list)
    objectives: List[MissionObjective] = Field(default_factory=list)
    constraints: List[MissionConstraint] = Field(default_factory=list)
    metrics: List[MissionMetric] = Field(default_factory=list)
    strategic_alignment_score: float = 0.95
    confidence: DecisionConfidence = DecisionConfidence.HIGH
    created_at: float = Field(default_factory=time.time)
    validated_at: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MissionEngine:
    """Decomposes enterprise goals into formal mission architectures."""

    def __init__(self) -> None:
        self._missions: Dict[str, Mission] = {}
        self._initialize_canonical_missions()

    def _initialize_canonical_missions(self) -> None:
        canonical = Mission(
            mission_id="msn_reduce_cost_40pct",
            title="Reduce Enterprise Document Processing Cost by 40%",
            raw_goal="Reduce document processing cost by 40% while maintaining >=98% accuracy within 90 days",
            priority=MissionPriority.CRITICAL,
            state=OrganizationState.PLANNING,
            timeline_days=90,
            required_capabilities=[
                "cost_optimization",
                "token_distillation",
                "ocr_batching",
                "smart_caching",
                "accuracy_verification"
            ],
            assigned_roles=[
                AgentRole.CEO_AGENT,
                AgentRole.CTO_AGENT,
                AgentRole.FINANCE_AGENT,
                AgentRole.ENGINEERING_AGENT,
                AgentRole.ANALYST_AGENT
            ],
            objectives=[
                MissionObjective(
                    title="Optimize GPU/Token Spend",
                    description="Implement dynamic model routing and context pruning to cut unit token cost by 45%",
                    target_metric="cost_per_1k_docs",
                    target_value=3.20,
                    current_value=5.40,
                    weight=0.4,
                    status="IN_PROGRESS",
                    progress_percent=35.0,
                ),
                MissionObjective(
                    title="Automate Extraction Pipeline Throughput",
                    description="Increase document throughput to 1,200 docs/min via parallelized swarm batching",
                    target_metric="throughput_dpm",
                    target_value=1200.0,
                    current_value=850.0,
                    weight=0.3,
                    status="IN_PROGRESS",
                    progress_percent=45.0,
                ),
                MissionObjective(
                    title="Maintain Extraction Accuracy Ceiling",
                    description="Enforce verification guards so accuracy never dips below 98.5%",
                    target_metric="f1_accuracy",
                    target_value=98.5,
                    current_value=98.8,
                    weight=0.3,
                    status="COMPLETED",
                    progress_percent=100.0,
                ),
            ],
            constraints=[
                MissionConstraint(
                    description="Accuracy must not drop below 98.0%",
                    constraint_type="ACCURACY",
                    threshold_value=98.0,
                    unit="percent",
                    is_strict=True,
                ),
                MissionConstraint(
                    description="Maximum execution budget $15,000",
                    constraint_type="BUDGET",
                    threshold_value=15000.0,
                    unit="usd",
                    is_strict=True,
                ),
                MissionConstraint(
                    description="Latency p95 under 450ms",
                    constraint_type="SLA",
                    threshold_value=450.0,
                    unit="ms",
                    is_strict=False,
                ),
            ],
            metrics=[
                MissionMetric(
                    name="Cost per 1k Documents",
                    baseline_value=5.80,
                    current_value=4.10,
                    target_value=3.20,
                    unit="USD",
                    direction="LOWER_IS_BETTER",
                ),
                MissionMetric(
                    name="Extraction F1 Score",
                    baseline_value=98.2,
                    current_value=98.8,
                    target_value=98.5,
                    unit="%",
                    direction="HIGHER_IS_BETTER",
                ),
                MissionMetric(
                    name="System Throughput",
                    baseline_value=600.0,
                    current_value=850.0,
                    target_value=1200.0,
                    unit="docs/min",
                    direction="HIGHER_IS_BETTER",
                ),
            ],
            strategic_alignment_score=0.96,
            confidence=DecisionConfidence.VERY_HIGH,
        )
        self._missions[canonical.mission_id] = canonical

    def decompose_goal(
        self,
        goal: str,
        priority: MissionPriority = MissionPriority.HIGH,
        timeline_days: int = 90,
        custom_constraints: Optional[List[str]] = None,
    ) -> Mission:
        """Parse raw goal string and construct structured mission."""
        title = goal[:80] + ("..." if len(goal) > 80 else "")

        # Extract percentages or numerical targets with bounded input and safe quantifiers (ReDoS prevention)
        bounded_goal = (goal or "")[:500]
        cost_match = re.search(r"(\d{1,3}(?:\.\d{1,2})?)%\s*(?:cost|spend|expense)", bounded_goal, re.IGNORECASE)
        acc_match = re.search(r"(\d{1,3}(?:\.\d{1,2})?)%\s*accuracy", bounded_goal, re.IGNORECASE)

        target_reduction = float(cost_match.group(1)) if cost_match else 25.0
        target_acc = float(acc_match.group(1)) if acc_match else 98.0

        objectives = [
            MissionObjective(
                title="Primary Operational Target",
                description=f"Execute core objective from goal: {goal}",
                target_metric="primary_kpi_index",
                target_value=100.0,
                current_value=10.0,
                weight=0.5,
                status="PENDING",
                progress_percent=10.0,
            ),
            MissionObjective(
                title="Resource & Cost Optimization",
                description=f"Reduce resource overhead by {target_reduction}%",
                target_metric="cost_reduction_percent",
                target_value=target_reduction,
                current_value=5.0,
                weight=0.3,
                status="PENDING",
                progress_percent=15.0,
            ),
            MissionObjective(
                title="Quality & Precision Assurance",
                description=f"Preserve output quality at or above {target_acc}%",
                target_metric="quality_score",
                target_value=target_acc,
                current_value=target_acc,
                weight=0.2,
                status="IN_PROGRESS",
                progress_percent=50.0,
            ),
        ]

        constraints = [
            MissionConstraint(
                description=f"Quality floor {target_acc}%",
                constraint_type="ACCURACY",
                threshold_value=target_acc,
                unit="percent",
                is_strict=True,
            ),
            MissionConstraint(
                description=f"Execution timeline <= {timeline_days} days",
                constraint_type="TIME",
                threshold_value=float(timeline_days),
                unit="days",
                is_strict=True,
            ),
        ]

        if custom_constraints:
            for c_str in custom_constraints:
                constraints.append(
                    MissionConstraint(
                        description=c_str,
                        constraint_type="CUSTOM",
                        threshold_value=1.0,
                        unit="flag",
                        is_strict=False,
                    )
                )

        metrics = [
            MissionMetric(
                name="Goal Achievement Ratio",
                baseline_value=0.0,
                current_value=15.0,
                target_value=100.0,
                unit="%",
                direction="HIGHER_IS_BETTER",
            ),
            MissionMetric(
                name="Cost Efficiency Gain",
                baseline_value=0.0,
                current_value=5.0,
                target_value=target_reduction,
                unit="%",
                direction="HIGHER_IS_BETTER",
            ),
        ]

        mission = Mission(
            title=title,
            raw_goal=goal,
            priority=priority,
            state=OrganizationState.PLANNING,
            timeline_days=timeline_days,
            required_capabilities=["strategy_planning", "multi_agent_execution", "performance_monitoring"],
            assigned_roles=[AgentRole.CEO_AGENT, AgentRole.CTO_AGENT, AgentRole.OPERATIONS_AGENT],
            objectives=objectives,
            constraints=constraints,
            metrics=metrics,
            strategic_alignment_score=0.92,
            confidence=DecisionConfidence.HIGH,
        )

        self._missions[mission.mission_id] = mission

        org_event_bus.publish(
            MissionCreated(
                actor_agent_role=AgentRole.CEO_AGENT,
                payload={"mission_id": mission.mission_id, "title": mission.title, "priority": mission.priority},
            )
        )

        return mission

    def validate_mission(self, mission_id: str) -> Dict[str, Any]:
        """Validate feasibility, constraints, and strategic alignment of a mission."""
        mission = self._missions.get(mission_id)
        if not mission:
            return {"valid": False, "error": f"Mission '{mission_id}' not found"}

        validation_checks = {
            "strategic_alignment": mission.strategic_alignment_score >= 0.80,
            "has_executable_objectives": len(mission.objectives) > 0,
            "has_bounded_constraints": len(mission.constraints) > 0,
            "timeline_feasible": mission.timeline_days > 0,
            "capabilities_mapped": len(mission.required_capabilities) > 0,
        }

        all_valid = all(validation_checks.values())
        if all_valid:
            mission.state = OrganizationState.PLANNING
            mission.validated_at = time.time()

            org_event_bus.publish(
                MissionValidated(
                    actor_agent_role=AgentRole.CTO_AGENT,
                    payload={"mission_id": mission_id, "checks": validation_checks, "status": "APPROVED"},
                )
            )

        return {
            "valid": all_valid,
            "mission_id": mission_id,
            "checks": validation_checks,
            "confidence_score": 0.94 if all_valid else 0.40,
            "alignment_score": mission.strategic_alignment_score,
            "validated_at": mission.validated_at,
        }

    def list_missions(self) -> List[Mission]:
        return list(self._missions.values())

    def get_mission(self, mission_id: str) -> Optional[Mission]:
        return self._missions.get(mission_id)


# Global Singleton
mission_engine = MissionEngine()
