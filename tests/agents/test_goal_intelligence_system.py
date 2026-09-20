"""
Tests for Autonomous Goal Intelligence & Mission Management System
==================================================================
Comprehensive test suite covering domain models, FSM lifecycle, validation,
capability analysis, dependency cycles, risk assessment, budget estimation,
cryptographic hashing, in-memory & SQLite repositories, event bus, and end-to-end mission builder.
"""

import pytest
import tempfile
from pathlib import Path

from research_validation.goal.constants import NonFabricationState
from research_validation.goal.models import (
    Goal, GoalType, PriorityLevel, GoalStatus, GoalConstraints,
    ConfidenceLevel, ConfidenceThreshold, StoppingConditionType, StoppingCondition,
    Comparator, SuccessCriterion, ResourceBudget, ExecutionBudget,
    CapabilityCriticality, CapabilityRequirement, DependencyType, GoalDependency,
    RiskSeverity, RiskItem, RiskProfile, EvidenceRequirement, MissionMetrics,
    MissionState, StateTransitionRecord, MissionStateMachine,
    MissionNode, ActionNode, TaskNode, SubgoalNode, MilestoneNode, ObjectiveNode, Mission
)
from research_validation.goal.interfaces import (
    SystemClock, FrozenClock, Uuid4IdGenerator, DeterministicIdGenerator,
    InMemoryEventBus, DefaultSystemCapabilityProvider
)
from research_validation.goal.repositories import (
    InMemoryGoalRepository, InMemoryMissionRepository, SqliteGoalRepository, SqliteMissionRepository
)
from research_validation.goal.services import (
    MissionHashingService, MissionSerializer, ConfidenceEstimatorService, ConstraintEngine,
    CapabilityAnalyzer, DependencyAnalyzer, RiskAssessor, BudgetEstimator,
    GoalDecomposer, GoalValidator, MissionBuilder, GoalManager, MissionRegistry, MissionScheduler
)
from research_validation.goal.exceptions import (
    GoalValidationError, InvalidStateTransitionError, MissingCapabilityError,
    CircularDependencyError, RiskThresholdExceededError
)


@pytest.fixture
def sample_goal() -> Goal:
    return Goal(
        goal_id="goal_ocr_eval_01",
        mission_id="mission_ocr_eval_01",
        title="Form Understanding Benchmarking",
        description="Empirically evaluate token classification F1 on FUNSD dataset.",
        objective="Validate that fine-tuned layout model reaches target F1 >= 0.92 with Wilson 95% confidence bounds.",
        problem_statement="Baseline LayoutLM model exhibits degraded precision on rotated invoice headers.",
        goal_type=GoalType.MODEL_EVALUATION,
        priority=PriorityLevel.HIGH,
        owner="PRINCIPAL_SCIENTIST",
        creation_timestamp_utc="2026-09-08T12:00:00+00:00",
        version="1.0.0",
        status=GoalStatus.DRAFT,
        confidence_threshold=ConfidenceThreshold(ConfidenceLevel.HIGH),
        success_metrics=(
            SuccessCriterion(
                metric_name="token_f1",
                comparator=Comparator.GREATER_THAN_OR_EQUAL,
                target_value=0.92,
                tolerance=0.005,
                confidence_requirement=0.90,
                minimum_sample_size=30,
            ),
        ),
        stopping_conditions=(
            StoppingCondition(
                condition_type=StoppingConditionType.GOAL_ACHIEVED,
                description="Token F1 reaches 0.92 with >= 90% confidence.",
            ),
            StoppingCondition(
                condition_type=StoppingConditionType.MAX_ITERATIONS,
                description="Halt if 50 iterations reached.",
            ),
        ),
        required_datasets=("funsd",),
        required_models=("layoutlm_v3",),
        capability_requirements=(
            CapabilityRequirement(capability_name="OCR", category="MODEL", criticality=CapabilityCriticality.MANDATORY),
            CapabilityRequirement(capability_name="BENCHMARK", category="BENCHMARK", criticality=CapabilityCriticality.MANDATORY),
            CapabilityRequirement(capability_name="STORAGE", category="STORAGE", criticality=CapabilityCriticality.MANDATORY),
        ),
        constraints=GoalConstraints(
            max_runtime_hours=12.0,
            max_gpu_hours=4.0,
            max_cost_usd=50.0,
        ),
    )


def test_goal_creation_and_cryptographic_digest(sample_goal):
    digest = sample_goal.compute_digest()
    assert len(digest) == 64
    assert isinstance(digest, str)
    
    # Verify canonical dict contains required attributes
    cd = sample_goal.canonical_dict()
    assert cd["goal_id"] == "goal_ocr_eval_01"
    assert cd["goal_type"] == "MODEL_EVALUATION"
    assert cd["confidence_threshold"] == 0.90


def test_mission_fsm_lifecycle_transitions():
    # Valid forward path
    assert MissionStateMachine.validate_transition(MissionState.CREATED, MissionState.VALIDATING) is True
    assert MissionStateMachine.validate_transition(MissionState.VALIDATING, MissionState.VALIDATED) is True
    assert MissionStateMachine.validate_transition(MissionState.VALIDATED, MissionState.ANALYZING_CAPABILITIES) is True
    assert MissionStateMachine.validate_transition(MissionState.GENERATING_SUCCESS_CRITERIA, MissionState.READY_FOR_OBSERVATION) is True
    assert MissionStateMachine.validate_transition(MissionState.READY_FOR_OBSERVATION, MissionState.ACTIVE) is True

    # Invalid illegal transition raises exception
    with pytest.raises(InvalidStateTransitionError):
        MissionStateMachine.assert_transition(MissionState.CREATED, MissionState.ACTIVE)

    with pytest.raises(InvalidStateTransitionError):
        MissionStateMachine.assert_transition(MissionState.COMPLETED, MissionState.ACTIVE)


def test_goal_validator_rejection_rules():
    # 1. Goal lacking success criteria
    bad_goal_no_metrics = Goal(
        goal_id="g_bad_1", mission_id="m_1", title="Bad Goal", description="", objective="Do research",
        problem_statement="Unknown", goal_type=GoalType.RESEARCH, priority=PriorityLevel.NORMAL,
        owner="USER", creation_timestamp_utc="2026-09-08T00:00:00Z",
        success_metrics=(),  # EMPTY
        stopping_conditions=(StoppingCondition(StoppingConditionType.MAX_ITERATIONS, "Halt at 10"),),
    )
    res = GoalValidator.validate_goal(bad_goal_no_metrics)
    assert res.is_valid is False
    assert any("success_metrics" in e for e in res.errors)

    # 2. Goal lacking stopping conditions
    bad_goal_no_stopping = Goal(
        goal_id="g_bad_2", mission_id="m_2", title="Bad Goal 2", description="", objective="Do research",
        problem_statement="Unknown", goal_type=GoalType.RESEARCH, priority=PriorityLevel.NORMAL,
        owner="USER", creation_timestamp_utc="2026-09-08T00:00:00Z",
        success_metrics=(SuccessCriterion("f1", Comparator.GREATER_THAN, 0.9),),
        stopping_conditions=(),  # EMPTY
    )
    res2 = GoalValidator.validate_goal(bad_goal_no_stopping)
    assert res2.is_valid is False
    assert any("stopping_conditions" in e for e in res2.errors)


def test_capability_analysis_satisfied_and_missing():
    provider = DefaultSystemCapabilityProvider(overrides={"GPU_ACCELERATION": False})
    analyzer = CapabilityAnalyzer(provider=provider)

    reqs = [
        CapabilityRequirement("OCR", "MODEL", CapabilityCriticality.MANDATORY),
        CapabilityRequirement("STORAGE", "STORAGE", CapabilityCriticality.MANDATORY),
        CapabilityRequirement("GPU_ACCELERATION", "HARDWARE", CapabilityCriticality.OPTIONAL),
    ]
    res = analyzer.analyze_capabilities(reqs)
    assert res.is_fully_satisfied is True
    assert "OCR" in res.satisfied_capabilities
    assert "GPU_ACCELERATION" in res.missing_optional_capabilities

    # Mandatory missing capability
    reqs_missing = [
        CapabilityRequirement("QUANTUM_COPROCESSOR", "HARDWARE", CapabilityCriticality.MANDATORY),
    ]
    res_missing = analyzer.analyze_capabilities(reqs_missing)
    assert res_missing.is_fully_satisfied is False
    assert "QUANTUM_COPROCESSOR" in res_missing.missing_mandatory_capabilities


def test_dependency_analyzer_cycle_detection():
    # Acyclic graph: A -> B -> C
    deps = [
        GoalDependency(source_id="A", target_id="B", dependency_type=DependencyType.GOAL),
        GoalDependency(source_id="B", target_id="C", dependency_type=DependencyType.GOAL),
    ]
    res = DependencyAnalyzer.analyze_dependencies(["A", "B", "C"], deps)
    assert res.is_valid is True
    assert res.topological_order == ["A", "B", "C"]

    # Cyclic graph: A -> B -> C -> A
    cyclic_deps = [
        GoalDependency(source_id="A", target_id="B", dependency_type=DependencyType.GOAL),
        GoalDependency(source_id="B", target_id="C", dependency_type=DependencyType.GOAL),
        GoalDependency(source_id="C", target_id="A", dependency_type=DependencyType.GOAL),
    ]
    res_cyclic = DependencyAnalyzer.analyze_dependencies(["A", "B", "C"], cyclic_deps)
    assert res_cyclic.is_valid is False
    assert len(res_cyclic.detected_cycles) > 0


def test_risk_assessor_multi_dimensional(sample_goal):
    profile = RiskAssessor.assess_goal_risk(sample_goal)
    assert 0.0 <= profile.overall_risk_score <= 1.0
    assert profile.severity in (RiskSeverity.NEGLIGIBLE, RiskSeverity.LOW, RiskSeverity.MEDIUM, RiskSeverity.HIGH, RiskSeverity.CRITICAL)
    assert len(profile.risk_items) >= 1
    assert profile.has_blocking_risks is False


def test_budget_estimator_and_constraint_checking(sample_goal):
    budget = BudgetEstimator.estimate_budget(sample_goal)
    assert budget.expected_runtime_hours > 0
    assert budget.resource_budget.cost_usd > 0
    assert budget.resource_budget.cpu_hours > 0

    is_valid, violations = ConstraintEngine.validate_budget_against_constraints(budget, sample_goal.constraints)
    assert is_valid is True
    assert len(violations) == 0


def test_in_memory_and_sqlite_repositories(sample_goal):
    # 1. In-Memory Repository
    in_mem_repo = InMemoryGoalRepository()
    in_mem_repo.save_goal(sample_goal)
    retrieved = in_mem_repo.get_goal_by_id(sample_goal.goal_id)
    assert retrieved is not None
    assert retrieved.title == sample_goal.title

    # 2. SQLite Repository
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = str(Path(tmpdir) / "test_goals.db")
        sqlite_repo = SqliteGoalRepository(db_path=db_file)
        sqlite_repo.save_goal(sample_goal)
        
        sq_retrieved = sqlite_repo.get_goal_by_id(sample_goal.goal_id)
        assert sq_retrieved is not None
        assert sq_retrieved.goal_id == sample_goal.goal_id
        assert sq_retrieved.goal_type == GoalType.MODEL_EVALUATION
        assert len(sqlite_repo.list_goals()) == 1
        sqlite_repo.close()


def test_event_bus_emission_and_ordering():
    bus = InMemoryEventBus()
    received_events = []

    bus.subscribe("GoalCreated", lambda e: received_events.append(e))
    bus.subscribe("*", lambda e: None)

    manager = GoalManager(
        repository=InMemoryGoalRepository(),
        event_bus=bus,
        id_generator=DeterministicIdGenerator("test"),
        clock=SystemClock(),
    )

    goal = manager.create_goal(
        title="Test Event Goal",
        description="Verify event emission.",
        objective="Verify event ordering.",
        problem_statement="None",
        goal_type=GoalType.RESEARCH,
        success_metrics=[SuccessCriterion("f1", Comparator.GREATER_THAN, 0.9)],
        stopping_conditions=[StoppingCondition(StoppingConditionType.MAX_ITERATIONS, "Halt at 10")],
    )

    assert len(received_events) == 1
    assert received_events[0].aggregate_id == goal.goal_id


def test_serialization_round_trip(sample_goal):
    json_str = MissionSerializer.serialize_goal(sample_goal)
    assert isinstance(json_str, str)
    deserialized = MissionSerializer.deserialize_dict(json_str)
    assert deserialized["goal_id"] == sample_goal.goal_id
    assert deserialized["goal_type"] == "MODEL_EVALUATION"


def test_end_to_end_mission_builder(sample_goal):
    event_bus = InMemoryEventBus()
    builder = MissionBuilder(
        event_bus=event_bus,
        id_generator=DeterministicIdGenerator("m"),
        clock=SystemClock(),
        capability_provider=DefaultSystemCapabilityProvider(),
    )

    mission = builder.build_mission(sample_goal)
    assert mission.mission_id.startswith("mission")
    assert mission.state == MissionState.READY_FOR_OBSERVATION
    assert len(mission.objectives) >= 1
    assert mission.metrics.readiness_score == 1.0
    assert len(mission.mission_digest_sha256) == 64
    assert len(mission.state_history) == 8

    # Verify event trail
    events = event_bus.get_published_events()
    event_types = [e.event_type for e in events]
    assert "MissionCreated" in event_types
    assert "CapabilityAnalysisCompleted" in event_types
    assert "DependencyAnalysisCompleted" in event_types
    assert "RiskCalculated" in event_types
    assert "BudgetEstimated" in event_types
    assert "MissionReadyForObservationEvent" in event_types or "MissionReadyForObservation" in event_types


def test_mission_scheduler_queue_and_activation(sample_goal):
    repo = InMemoryMissionRepository()
    bus = InMemoryEventBus()
    builder = MissionBuilder(event_bus=bus)
    mission = builder.build_mission(sample_goal)
    repo.save_mission(mission)

    scheduler = MissionScheduler(repository=repo, event_bus=bus, clock=SystemClock(), max_concurrent_missions=2)
    queue = scheduler.get_prioritized_queue()
    assert len(queue) == 1
    assert queue[0].mission_id == mission.mission_id

    activated = scheduler.activate_next_mission()
    assert activated is not None
    assert activated.state == MissionState.ACTIVE
    assert len(repo.list_missions(state=MissionState.ACTIVE.value)) == 1
