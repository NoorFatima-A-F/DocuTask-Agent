"""
Mission Builder Service
=======================
Orchestrates the complete 8-stage transformation from a raw Goal to a validated
Mission in READY_FOR_OBSERVATION state, advancing through the FSM deterministically.
"""

from typing import List, Optional

from research_validation.goal.models.goal import Goal
from research_validation.goal.models.mission import Mission
from research_validation.goal.models.mission_state import (
    MissionState, StateTransitionRecord, MissionStateMachine
)
from research_validation.goal.models.mission_metrics import MissionMetrics
from research_validation.goal.services.goal_validator import GoalValidator
from research_validation.goal.services.capability_analyzer import CapabilityAnalyzer
from research_validation.goal.services.dependency_analyzer import DependencyAnalyzer
from research_validation.goal.services.risk_assessor import RiskAssessor
from research_validation.goal.services.budget_estimator import BudgetEstimator
from research_validation.goal.services.goal_decomposer import GoalDecomposer
from research_validation.goal.interfaces.event_bus import IEventBus, InMemoryEventBus
from research_validation.goal.interfaces.id_generator import IIdGenerator, Uuid4IdGenerator
from research_validation.goal.interfaces.clock import IClock, SystemClock
from research_validation.goal.interfaces.capability_provider import ICapabilityProvider
from research_validation.goal.events.mission_events import (
    MissionCreatedEvent, CapabilityAnalysisCompletedEvent,
    DependencyAnalysisCompletedEvent, RiskCalculatedEvent, BudgetEstimatedEvent,
    MissionReadyForObservationEvent
)
from research_validation.goal.exceptions import (
    GoalValidationError, MissingCapabilityError, RiskThresholdExceededError
)


class MissionBuilder:
    """
    Builds and transitions an autonomous mission through all preparatory lifecycle stages.
    """

    def __init__(
        self,
        event_bus: Optional[IEventBus] = None,
        id_generator: Optional[IIdGenerator] = None,
        clock: Optional[IClock] = None,
        capability_provider: Optional[ICapabilityProvider] = None,
    ):
        self.event_bus = event_bus or InMemoryEventBus()
        self.id_gen = id_generator or Uuid4IdGenerator()
        self.clock = clock or SystemClock()
        self.capability_analyzer = CapabilityAnalyzer(provider=capability_provider)

    def build_mission(self, goal: Goal) -> Mission:
        """Executes the full pipeline to transform a Goal into a READY_FOR_OBSERVATION Mission."""
        mission_id = goal.mission_id or self.id_gen.generate_id(prefix="mission")
        now_str = self.clock.now_utc_iso()
        transitions: List[StateTransitionRecord] = []

        # Stage 1: CREATED
        curr_state = MissionState.CREATED
        self.event_bus.publish(MissionCreatedEvent(
            event_id=self.id_gen.generate_id("evt"),
            event_type="MissionCreated",
            aggregate_id=mission_id,
            timestamp_utc=now_str,
            payload={"goal_id": goal.goal_id, "title": goal.title},
        ))

        # Stage 2: VALIDATING -> VALIDATED
        MissionStateMachine.assert_transition(curr_state, MissionState.VALIDATING)
        curr_state = MissionState.VALIDATING
        transitions.append(StateTransitionRecord(from_state=MissionState.CREATED, to_state=curr_state, timestamp_utc=now_str))

        val_res = GoalValidator.validate_goal(goal)
        if not val_res.is_valid:
            raise GoalValidationError(f"Goal validation failed: {val_res.errors}", validation_errors=val_res.errors)

        MissionStateMachine.assert_transition(curr_state, MissionState.VALIDATED)
        curr_state = MissionState.VALIDATED
        transitions.append(StateTransitionRecord(from_state=MissionState.VALIDATING, to_state=curr_state, timestamp_utc=now_str))

        # Stage 3: ANALYZING_CAPABILITIES
        MissionStateMachine.assert_transition(curr_state, MissionState.ANALYZING_CAPABILITIES)
        curr_state = MissionState.ANALYZING_CAPABILITIES
        transitions.append(StateTransitionRecord(from_state=MissionState.VALIDATED, to_state=curr_state, timestamp_utc=now_str))

        cap_res = self.capability_analyzer.analyze_capabilities(list(goal.capability_requirements))
        self.event_bus.publish(CapabilityAnalysisCompletedEvent(
            event_id=self.id_gen.generate_id("evt"),
            event_type="CapabilityAnalysisCompleted",
            aggregate_id=mission_id,
            timestamp_utc=now_str,
            payload={"satisfied": cap_res.satisfied_capabilities, "missing": cap_res.missing_mandatory_capabilities},
        ))
        if not cap_res.is_fully_satisfied:
            raise MissingCapabilityError(missing_capabilities=cap_res.missing_mandatory_capabilities)

        # Stage 4: ANALYZING_DEPENDENCIES
        MissionStateMachine.assert_transition(curr_state, MissionState.ANALYZING_DEPENDENCIES)
        curr_state = MissionState.ANALYZING_DEPENDENCIES
        transitions.append(StateTransitionRecord(from_state=MissionState.ANALYZING_CAPABILITIES, to_state=curr_state, timestamp_utc=now_str))

        nodes = list(set([d.source_id for d in goal.dependencies] + [d.target_id for d in goal.dependencies]))
        dep_res = DependencyAnalyzer.analyze_dependencies(nodes, list(goal.dependencies))
        self.event_bus.publish(DependencyAnalysisCompletedEvent(
            event_id=self.id_gen.generate_id("evt"),
            event_type="DependencyAnalysisCompleted",
            aggregate_id=mission_id,
            timestamp_utc=now_str,
            payload={"is_valid": dep_res.is_valid, "total_dependencies": dep_res.total_dependencies_count},
        ))

        # Stage 5: ANALYZING_RISK
        MissionStateMachine.assert_transition(curr_state, MissionState.ANALYZING_RISK)
        curr_state = MissionState.ANALYZING_RISK
        transitions.append(StateTransitionRecord(from_state=MissionState.ANALYZING_DEPENDENCIES, to_state=curr_state, timestamp_utc=now_str))

        risk_profile = RiskAssessor.assess_goal_risk(goal, missing_capabilities_count=len(cap_res.missing_mandatory_capabilities))
        self.event_bus.publish(RiskCalculatedEvent(
            event_id=self.id_gen.generate_id("evt"),
            event_type="RiskCalculated",
            aggregate_id=mission_id,
            timestamp_utc=now_str,
            payload={"risk_score": risk_profile.overall_risk_score, "severity": risk_profile.severity.value},
        ))
        if risk_profile.has_blocking_risks:
            blocking = [r.description for r in risk_profile.risk_items if r.is_blocking]
            raise RiskThresholdExceededError(risk_score=risk_profile.overall_risk_score, max_acceptable=0.70, blocking_risks=blocking)

        # Stage 6: ESTIMATING_BUDGET
        MissionStateMachine.assert_transition(curr_state, MissionState.ESTIMATING_BUDGET)
        curr_state = MissionState.ESTIMATING_BUDGET
        transitions.append(StateTransitionRecord(from_state=MissionState.ANALYZING_RISK, to_state=curr_state, timestamp_utc=now_str))

        budget = BudgetEstimator.estimate_budget(goal)
        self.event_bus.publish(BudgetEstimatedEvent(
            event_id=self.id_gen.generate_id("evt"),
            event_type="BudgetEstimated",
            aggregate_id=mission_id,
            timestamp_utc=now_str,
            payload={"expected_runtime": budget.expected_runtime_hours, "cost_usd": budget.resource_budget.cost_usd},
        ))

        # Stage 7: GENERATING_SUCCESS_CRITERIA & MISSION GRAPH
        MissionStateMachine.assert_transition(curr_state, MissionState.GENERATING_SUCCESS_CRITERIA)
        curr_state = MissionState.GENERATING_SUCCESS_CRITERIA
        transitions.append(StateTransitionRecord(from_state=MissionState.ESTIMATING_BUDGET, to_state=curr_state, timestamp_utc=now_str))

        objectives = GoalDecomposer.decompose_goal(goal)

        # Stage 8: READY_FOR_OBSERVATION
        MissionStateMachine.assert_transition(curr_state, MissionState.READY_FOR_OBSERVATION)
        curr_state = MissionState.READY_FOR_OBSERVATION
        transitions.append(StateTransitionRecord(from_state=MissionState.GENERATING_SUCCESS_CRITERIA, to_state=curr_state, timestamp_utc=now_str))

        metrics = MissionMetrics(
            total_objectives_count=len(objectives),
            total_milestones_count=sum(len(o.milestones) for o in objectives),
            total_tasks_count=sum(len(sg.tasks) for o in objectives for ms in o.milestones for sg in ms.subgoals),
            total_actions_count=sum(len(t.actions) for o in objectives for ms in o.milestones for sg in ms.subgoals for t in sg.tasks),
            graph_depth=5,
            estimated_complexity_score=0.45,
            feasibility_score=1.0 - risk_profile.overall_risk_score,
            readiness_score=1.0,
        )

        mission = Mission(
            mission_id=mission_id,
            goal_id=goal.goal_id,
            title=f"Mission: {goal.title}",
            description=goal.description,
            version="1.0.0",
            state=MissionState.READY_FOR_OBSERVATION,
            goal=goal,
            objectives=objectives,
            execution_budget=budget,
            risk_profile=risk_profile,
            metrics=metrics,
            state_history=tuple(transitions),
            created_at_utc=now_str,
            updated_at_utc=now_str,
            previous_version_hash="",
        )

        digest = mission.compute_digest()
        mission = Mission(
            mission_id=mission.mission_id,
            goal_id=mission.goal_id,
            title=mission.title,
            description=mission.description,
            version=mission.version,
            state=mission.state,
            goal=mission.goal,
            objectives=mission.objectives,
            execution_budget=mission.execution_budget,
            risk_profile=mission.risk_profile,
            metrics=mission.metrics,
            state_history=mission.state_history,
            created_at_utc=mission.created_at_utc,
            updated_at_utc=mission.updated_at_utc,
            author=mission.author,
            previous_version_hash=mission.previous_version_hash,
            mission_digest_sha256=digest,
        )

        self.event_bus.publish(MissionReadyForObservationEvent(
            event_id=self.id_gen.generate_id("evt"),
            event_type="MissionReadyForObservation",
            aggregate_id=mission_id,
            timestamp_utc=now_str,
            payload={"mission_digest": digest, "state": mission.state.value},
        ))

        return mission
