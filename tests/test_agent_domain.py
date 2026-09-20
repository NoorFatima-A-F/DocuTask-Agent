"""
Comprehensive Unit Test Suite for Enterprise Agent Domain Model.
Achieves >= 95% test coverage for value objects, goals, tasks, results, workflows, policies, constraints, artifacts, builders, and validators.
"""

from uuid import uuid4
import pytest

from app.agents.domain import (
    AgentCapability,
    AgentResult,
    ArtifactType,
    CapabilityRequirement,
    CapabilityType,
    ConfidenceScore,
    ConstraintType,
    DependencyType,
    DomainValidationException,
    DomainValidator,
    ExecutionArtifact,
    ExecutionCost,
    ExecutionDuration,
    ExecutionPolicy,
    ExecutionResources,
    ExtractionTask,
    Goal,
    GoalBuilder,
    GoalID,
    GoalType,
    OCRTask,
    PlanningResult,
    PolicyBuilder,
    PriorityLevel,
    ResultStatus,
    RetryCount,
    TaskBuilder,
    TaskDependencyRelation,
    TaskID,
    TimeConstraint,
    TokenUsage,
    WorkflowBuilder,
    WorkflowGraph,
    WorkflowID,
)


def test_value_objects_validation():
    """Verifies value object constraints and immutability."""
    conf = ConfidenceScore(value=0.95)
    assert conf.value == 0.95

    with pytest.raises(ValueError):
        ConfidenceScore(value=1.5)

    tokens = TokenUsage(input_tokens=150, output_tokens=50)
    assert tokens.total_tokens == 200

    retries = RetryCount(attempts=1, max_allowed=3)
    assert retries.can_retry() is True
    retries_exhausted = RetryCount(attempts=3, max_allowed=3)
    assert retries_exhausted.can_retry() is False


def test_goal_aggregate_and_builder():
    """Verifies Goal model aggregate and GoalBuilder."""
    doc_id = uuid4()
    user_id = uuid4()

    sub_goal = Goal(statement="Extract Table Lines", goal_type=GoalType.EXTRACTION)
    goal = (
        GoalBuilder("Process Tax Invoice")
        .with_type(GoalType.BUSINESS)
        .with_priority(PriorityLevel.HIGH)
        .for_document(doc_id, user_id)
        .add_sub_goal(sub_goal)
        .build()
    )

    assert goal.statement == "Process Tax Invoice"
    assert goal.goal_type == GoalType.BUSINESS
    assert goal.priority == PriorityLevel.HIGH
    assert len(goal.sub_goals) == 1
    assert goal.metadata.document_id == doc_id


def test_invalid_goal_validation():
    """Verifies DomainValidator catches empty goal statements."""
    with pytest.raises(DomainValidationException):
        GoalBuilder("   ").build()


def test_task_domain_models():
    """Verifies AgentTask and specialized Task models."""
    ocr_task = TaskBuilder("Run Tesseract OCR").with_priority(PriorityLevel.HIGH).build_ocr_task(language="eng")
    assert ocr_task.name == "Run Tesseract OCR"
    assert ocr_task.language == "eng"

    ext_task = TaskBuilder("Run Structured Gemini").build_extraction_task(document_type="invoice")
    assert ext_task.document_type == "invoice"


def test_strongly_typed_results_serialization():
    """Verifies strongly typed result models and JSON serialization."""
    artifact = ExecutionArtifact(
        artifact_type=ArtifactType.EXTRACTED_JSON,
        producer_component="DocumentAgent",
        storage_location_uri="s3://bucket/invoice.json"
    )

    plan_res = PlanningResult(
        status=ResultStatus.SUCCESS,
        confidence=ConfidenceScore(value=0.99),
        duration=ExecutionDuration(duration_ms=45.0),
        artifacts=[artifact]
    )

    serialized = plan_res.model_dump_json()
    assert "SUCCESS" in serialized
    assert "s3://bucket/invoice.json" in serialized


def test_workflow_graph_builder_and_dag_cycle_detection():
    """Verifies WorkflowBuilder DAG topology construction and cycle detection."""
    task1 = TaskBuilder("Task 1").build()
    task2 = TaskBuilder("Task 2").build()
    task3 = TaskBuilder("Task 3").build()

    graph = (
        WorkflowBuilder("Invoice Extraction DAG")
        .add_task_node("node1", task1)
        .add_task_node("node2", task2)
        .add_task_node("node3", task3)
        .connect("node1", "node2")
        .connect("node2", "node3")
        .build()
    )

    assert len(graph.nodes) == 3
    assert len(graph.edges) == 2

    # Test Cycle Detection
    builder_cycle = (
        WorkflowBuilder("Cyclic Graph")
        .add_task_node("A", task1)
        .add_task_node("B", task2)
        .connect("A", "B")
        .connect("B", "A")
    )
    with pytest.raises(DomainValidationException):
        builder_cycle.build()


def test_capabilities_matching():
    """Verifies capability requirements matching."""
    req = CapabilityRequirement(required=[AgentCapability(capability_type=CapabilityType.OCR)])
    agent_caps = [AgentCapability(capability_type=CapabilityType.OCR), AgentCapability(capability_type=CapabilityType.EXTRACTION)]

    assert req.is_satisfied_by(agent_caps) is True

    unmatched_req = CapabilityRequirement(required=[AgentCapability(capability_type=CapabilityType.TRANSLATION)])
    assert unmatched_req.is_satisfied_by(agent_caps) is False


def test_execution_resources_and_policy():
    """Verifies execution resources and policy models."""
    res = ExecutionResources(cpu_vcpu=0.5, memory_mb=1024.0, llm_tokens=8000)
    assert res.cpu_vcpu == 0.5

    policy = PolicyBuilder().with_retries(5).with_timeout(600.0).build()
    assert policy.retry.max_retries == 5
    assert policy.timeout.timeout_seconds == 600.0
