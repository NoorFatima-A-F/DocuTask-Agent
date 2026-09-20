"""
Goal Manager Service
====================
Primary application service providing CRUD, validation, revisioning, and lifecycle management for Goals.
"""

from typing import Any, Dict, List, Optional, Tuple
from research_validation.goal.models.goal import (
    Goal, GoalType, PriorityLevel, GoalStatus
)
from research_validation.goal.models.confidence_threshold import ConfidenceThreshold, ConfidenceLevel
from research_validation.goal.models.goal_constraints import GoalConstraints
from research_validation.goal.models.success_criteria import SuccessCriterion
from research_validation.goal.models.stopping_condition import StoppingCondition
from research_validation.goal.models.capability_requirement import CapabilityRequirement
from research_validation.goal.models.dependency import GoalDependency
from research_validation.goal.models.evidence_requirement import EvidenceRequirement
from research_validation.goal.interfaces.repository import IGoalRepository
from research_validation.goal.interfaces.event_bus import IEventBus
from research_validation.goal.interfaces.id_generator import IIdGenerator
from research_validation.goal.interfaces.clock import IClock
from research_validation.goal.services.goal_validator import GoalValidator
from research_validation.goal.events.goal_events import (
    GoalCreatedEvent, GoalValidatedEvent, GoalRejectedEvent, GoalUpdatedEvent
)
from research_validation.goal.exceptions import GoalValidationError, EntityNotFoundError


class GoalManager:
    """
    Manages the creation, validation, storage, and version evolution of Goals.
    """

    def __init__(
        self,
        repository: IGoalRepository,
        event_bus: IEventBus,
        id_generator: IIdGenerator,
        clock: IClock,
    ):
        self.repo = repository
        self.event_bus = event_bus
        self.id_gen = id_generator
        self.clock = clock

    def create_goal(
        self,
        title: str,
        description: str,
        objective: str,
        problem_statement: str,
        goal_type: GoalType,
        priority: PriorityLevel = PriorityLevel.NORMAL,
        owner: str = "RESEARCHER",
        confidence_threshold: Optional[ConfidenceThreshold] = None,
        success_metrics: Optional[List[SuccessCriterion]] = None,
        stopping_conditions: Optional[List[StoppingCondition]] = None,
        required_datasets: Optional[List[str]] = None,
        required_models: Optional[List[str]] = None,
        required_tools: Optional[List[str]] = None,
        capability_requirements: Optional[List[CapabilityRequirement]] = None,
        constraints: Optional[GoalConstraints] = None,
        dependencies: Optional[List[GoalDependency]] = None,
        governance_policies: Optional[List[str]] = None,
        mission_id: Optional[str] = None,
    ) -> Goal:
        """Instantiates, seals, and persists a new Goal."""
        goal_id = self.id_gen.generate_id(prefix="goal")
        m_id = mission_id or self.id_gen.generate_id(prefix="mission")
        now_str = self.clock.now_utc_iso()

        goal = Goal(
            goal_id=goal_id,
            mission_id=m_id,
            title=title,
            description=description,
            objective=objective,
            problem_statement=problem_statement,
            goal_type=goal_type,
            priority=priority,
            owner=owner,
            creation_timestamp_utc=now_str,
            version="1.0.0",
            status=GoalStatus.DRAFT,
            confidence_threshold=confidence_threshold or ConfidenceThreshold(ConfidenceLevel.HIGH),
            success_metrics=tuple(success_metrics or []),
            stopping_conditions=tuple(stopping_conditions or []),
            required_datasets=tuple(required_datasets or []),
            required_models=tuple(required_models or []),
            required_tools=tuple(required_tools or []),
            capability_requirements=tuple(capability_requirements or []),
            constraints=constraints or GoalConstraints(),
            dependencies=tuple(dependencies or []),
            governance_policies=tuple(governance_policies or []),
        )

        digest = goal.compute_digest()
        sealed_goal = Goal(
            goal_id=goal.goal_id,
            mission_id=goal.mission_id,
            title=goal.title,
            description=goal.description,
            objective=goal.objective,
            problem_statement=goal.problem_statement,
            goal_type=goal.goal_type,
            priority=goal.priority,
            owner=goal.owner,
            creation_timestamp_utc=goal.creation_timestamp_utc,
            version=goal.version,
            status=goal.status,
            confidence_threshold=goal.confidence_threshold,
            success_metrics=goal.success_metrics,
            stopping_conditions=goal.stopping_conditions,
            required_datasets=goal.required_datasets,
            required_models=goal.required_models,
            required_tools=goal.required_tools,
            capability_requirements=goal.capability_requirements,
            constraints=goal.constraints,
            dependencies=goal.dependencies,
            governance_policies=goal.governance_policies,
            cryptographic_digest_sha256=digest,
        )

        self.repo.save_goal(sealed_goal)
        self.event_bus.publish(GoalCreatedEvent(
            event_id=self.id_gen.generate_id("evt"),
            event_type="GoalCreated",
            aggregate_id=goal_id,
            timestamp_utc=now_str,
            payload={"goal_id": goal_id, "title": title, "digest": digest},
        ))

        return sealed_goal

    def validate_and_approve(self, goal_id: str) -> Goal:
        """Validates an existing draft goal and advances its status to VALIDATED."""
        goal = self.repo.get_goal_by_id(goal_id)
        if not goal:
            raise EntityNotFoundError("Goal", goal_id)

        val_res = GoalValidator.validate_goal(goal)
        now_str = self.clock.now_utc_iso()

        if not val_res.is_valid:
            self.event_bus.publish(GoalRejectedEvent(
                event_id=self.id_gen.generate_id("evt"),
                event_type="GoalRejected",
                aggregate_id=goal_id,
                timestamp_utc=now_str,
                payload={"goal_id": goal_id, "errors": val_res.errors},
            ))
            raise GoalValidationError(f"Goal {goal_id} failed validation.", validation_errors=val_res.errors)

        updated_goal = Goal(
            goal_id=goal.goal_id,
            mission_id=goal.mission_id,
            title=goal.title,
            description=goal.description,
            objective=goal.objective,
            problem_statement=goal.problem_statement,
            goal_type=goal.goal_type,
            priority=goal.priority,
            owner=goal.owner,
            creation_timestamp_utc=goal.creation_timestamp_utc,
            version=goal.version,
            status=GoalStatus.VALIDATED,
            confidence_threshold=goal.confidence_threshold,
            success_metrics=goal.success_metrics,
            stopping_conditions=goal.stopping_conditions,
            required_datasets=goal.required_datasets,
            required_models=goal.required_models,
            required_tools=goal.required_tools,
            capability_requirements=goal.capability_requirements,
            constraints=goal.constraints,
            dependencies=goal.dependencies,
            governance_policies=goal.governance_policies,
            cryptographic_digest_sha256=goal.cryptographic_digest_sha256,
        )

        self.repo.save_goal(updated_goal)
        self.event_bus.publish(GoalValidatedEvent(
            event_id=self.id_gen.generate_id("evt"),
            event_type="GoalValidated",
            aggregate_id=goal_id,
            timestamp_utc=now_str,
            payload={"goal_id": goal_id, "status": updated_goal.status.value},
        ))

        return updated_goal

    def get_goal(self, goal_id: str) -> Optional[Goal]:
        return self.repo.get_goal_by_id(goal_id)
