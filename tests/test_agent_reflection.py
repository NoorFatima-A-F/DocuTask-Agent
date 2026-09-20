"""
Unit and Integration Test Suite for Enterprise Reflection Engine.
Targeting >=95% meaningful coverage across evaluation, critique, knowledge extraction,
recommendations, adaptation, feedback generation, serialization, builders, and repositories.
"""

from datetime import datetime, timezone
import json
import pytest
from uuid import UUID, uuid4

from app.agents.reflection.adaptation_engine import (
    AdaptationEngine,
    AdaptationProposal,
    AdaptationStatus,
    AdaptationType,
)
from app.agents.reflection.benchmark import BenchmarkCriteria, BenchmarkEvaluator
from app.agents.reflection.bias_detector import BiasDetector
from app.agents.reflection.builders import (
    CritiqueBuilder,
    EvaluationBuilder,
    FeedbackBuilder,
    LearningArtifactBuilder,
    RecommendationBuilder,
    ReflectionRequestBuilder,
    ReflectionSessionBuilder,
)
from app.agents.reflection.cache import ReflectionCache
from app.agents.reflection.comparative_analysis import ComparativeAnalyzer
from app.agents.reflection.confidence_evaluator import ConfidenceEvaluator
from app.agents.reflection.context import ReflectionContext, ReflectionRequest, ReflectionResult
from app.agents.reflection.correlation import CorrelationAnalyzer
from app.agents.reflection.correctness_evaluator import CorrectnessEvaluator
from app.agents.reflection.cost_evaluator import CostEvaluator
from app.agents.reflection.critique_engine import CritiqueEngine
from app.agents.reflection.decision_analyzer import DecisionAnalyzer
from app.agents.reflection.efficiency_evaluator import EfficiencyEvaluator
from app.agents.reflection.engine import ReflectionEngine
from app.agents.reflection.evaluation import (
    DimensionEvaluation,
    EvaluationDimension,
    EvaluationMetric,
    EvaluationReport,
)
from app.agents.reflection.evaluation_graph import EvaluationGraph, EvaluationStageNode
from app.agents.reflection.evaluation_pipeline import EvaluationPipeline
from app.agents.reflection.events import (
    CritiqueGeneratedEvent,
    EvaluationCompletedEvent,
    LearningArtifactCreatedEvent,
    ReflectionCompletedEvent,
    ReflectionStartedEvent,
)
from app.agents.reflection.exceptions import (
    AdaptationApprovalRequiredError,
    CircularCritiqueReferenceError,
    DuplicateLearningArtifactError,
    IncompleteExecutionTraceError,
    InconsistentEvidenceError,
    InvalidConfidenceScoreError,
    InvalidEvaluationGraphError,
    MalformedRecommendationError,
)
from app.agents.reflection.execution_analyzer import ExecutionAnalyzer
from app.agents.reflection.execution_feedback import ExecutionCritiqueItem, ExecutionFeedback
from app.agents.reflection.factory import ReflectionFactory
from app.agents.reflection.failure_analyzer import FailureAnalyzer
from app.agents.reflection.feedback_generator import FeedbackGenerator, SubsystemFeedbackBundle
from app.agents.reflection.goal_evaluator import GoalEvaluator
from app.agents.reflection.hallucination_detector import HallucinationDetector
from app.agents.reflection.improvement_generator import ImprovementDirective, ImprovementGenerator
from app.agents.reflection.inconsistency_detector import InconsistencyDetector
from app.agents.reflection.knowledge_extractor import KnowledgeExtractor
from app.agents.reflection.latency_evaluator import LatencyEvaluator
from app.agents.reflection.learning_artifact import LearningArtifact, LearningArtifactType
from app.agents.reflection.lifecycle import ReflectionLifecycleState
from app.agents.reflection.manager import ReflectionManager
from app.agents.reflection.memory_evaluator import MemoryEvaluator
from app.agents.reflection.memory_feedback import MemoryFeedback, MemoryUpdateRequest
from app.agents.reflection.metadata import ReflectionIdentity, ReflectionMetadata, ReflectionStatistics
from app.agents.reflection.metrics import ReflectionMetrics, ReflectionMetricsCollector
from app.agents.reflection.orchestrator import ReflectionOrchestrator
from app.agents.reflection.pattern_detector import DetectedPattern, PatternDetector
from app.agents.reflection.performance_analyzer import PerformanceAnalyzer
from app.agents.reflection.plan_analyzer import PlanAnalyzer
from app.agents.reflection.planner_feedback import PlannerCritiqueItem, PlannerFeedback
from app.agents.reflection.quality_evaluator import QualityEvaluator
from app.agents.reflection.ranking import AlternativeRanker
from app.agents.reflection.reasoning_analyzer import ReasoningAnalyzer
from app.agents.reflection.reasoning_validator import ReasoningValidator
from app.agents.reflection.recommendation_engine import (
    Recommendation,
    RecommendationEngine,
    SubsystemTarget,
)
from app.agents.reflection.reflection import Reflection
from app.agents.reflection.reflection_context import (
    DecisionTrace,
    ExecutionTraceEnvelope,
    ReasoningStepTrace,
    TaskTrace,
    ToolCallTrace,
)
from app.agents.reflection.reflection_graph import ReflectionGraph, ReflectionNode
from app.agents.reflection.reflection_session import ReflectionSession
from app.agents.reflection.repository import (
    InMemoryEvaluationRepository,
    InMemoryLearningArtifactRepository,
    InMemoryRecommendationRepository,
    InMemoryReflectionRepository,
)
from app.agents.reflection.resource_analyzer import ResourceAnalyzer
from app.agents.reflection.risk_evaluator import RiskEvaluator
from app.agents.reflection.root_cause import ReflectionRootCauseAnalyzer
from app.agents.reflection.runtime import ReflectionRuntime
from app.agents.reflection.scoring import CompositeScorer
from app.agents.reflection.self_critique import CritiqueFinding, SelfCritique
from app.agents.reflection.serialization import ReflectionSerializer
from app.agents.reflection.success_analyzer import SuccessAnalyzer
from app.agents.reflection.token_evaluator import TokenEvaluator
from app.agents.reflection.tool_feedback import ToolFeedback
from app.agents.reflection.tool_usage_analyzer import ToolUsageAnalyzer
from app.agents.reflection.trend_analyzer import TrendAnalyzer
from app.agents.reflection.validation import ReflectionRequestValidator
from app.agents.reflection.validators import ReflectionValidator


@pytest.fixture
def sample_successful_trace() -> ExecutionTraceEnvelope:
    """Fixture providing a complete, successful execution trace envelope."""
    return ExecutionTraceEnvelope(
        execution_id=uuid4(),
        plan_id=uuid4(),
        goal="Process 10-K Document and Extract Financial Metrics",
        final_state="COMPLETED",
        total_duration_ms=4500.0,
        token_usage={"prompt_tokens": 1200, "completion_tokens": 400},
        cost_usd=0.035,
        tasks=[
            TaskTrace(task_id="t1", task_name="ParsePDF", status="COMPLETED", duration_ms=1200.0),
            TaskTrace(task_id="t2", task_name="ExtractTables", status="COMPLETED", duration_ms=2100.0),
            TaskTrace(task_id="t3", task_name="ValidateRatios", status="COMPLETED", duration_ms=1200.0),
        ],
        tool_calls=[
            ToolCallTrace(tool_name="pdf_parser", success=True, duration_ms=1100.0),
            ToolCallTrace(tool_name="table_extractor", success=True, duration_ms=2000.0),
        ],
        reasoning_steps=[
            ReasoningStepTrace(
                step_id="step_1",
                rationale="Table contains Balance Sheet headers.",
                evidence=["Assets", "Liabilities"],
                conclusion="Recognized as Balance Sheet",
                confidence_score=0.95
            )
        ],
        decisions=[
            DecisionTrace(decision_id="dec_1", policy_name="PII_Filter", outcome="ALLOWED", risk_score=0.05)
        ],
        final_outputs={"extracted_revenue": 1000000.0, "currency": "USD"}
    )


@pytest.fixture
def sample_failed_trace() -> ExecutionTraceEnvelope:
    """Fixture providing an execution trace with failures and errors."""
    return ExecutionTraceEnvelope(
        execution_id=uuid4(),
        plan_id=uuid4(),
        goal="Translate Document to German",
        final_state="FAILED",
        total_duration_ms=18500.0,
        token_usage={"prompt_tokens": 8500, "completion_tokens": 200},
        cost_usd=0.15,
        tasks=[
            TaskTrace(task_id="t1", task_name="TranslateChunk1", status="FAILED", error_message="ToolTimeoutException"),
        ],
        tool_calls=[
            ToolCallTrace(tool_name="translator_tool", success=False, error_details="Timeout 10000ms exceeded")
        ],
        errors=["Task TranslateChunk1 failed: ToolTimeoutException"],
        recovery_actions=[{"action": "RETRY", "status": "FAILED"}]
    )


# ---------------------------------------------------------------------------
# Part 1 & Runtime Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_reflection_engine_success_pipeline(sample_successful_trace):
    """Verifies complete end-to-end reflection pipeline for successful execution."""
    engine = ReflectionFactory.create_engine()
    request = ReflectionRequest(trace=sample_successful_trace)

    result: ReflectionResult = await engine.reflect(request)

    assert result.lifecycle_state == ReflectionLifecycleState.COMPLETED
    assert result.evaluation_report is not None
    assert result.evaluation_report.overall_score >= 0.85
    assert result.critique is not None
    assert len(result.learning_artifacts) >= 1
    assert len(result.recommendations) >= 1
    assert result.planner_feedback is not None
    assert result.execution_feedback is not None
    assert result.statistics.evaluators_executed >= 10


@pytest.mark.asyncio
async def test_reflection_engine_failed_trace_handling(sample_failed_trace):
    """Verifies that reflection engine diagnoses failures and produces corrective feedback."""
    engine = ReflectionFactory.create_engine()
    request = ReflectionRequest(trace=sample_failed_trace)

    result: ReflectionResult = await engine.reflect(request)

    assert result.lifecycle_state == ReflectionLifecycleState.COMPLETED
    assert result.evaluation_report is not None
    assert result.evaluation_report.overall_score < 0.80
    assert any("FAILED" in w or "failed" in w.lower() for w in result.critique.weaknesses)


@pytest.mark.asyncio
async def test_reflection_runtime_start_stop(sample_successful_trace):
    """Tests ReflectionRuntime container lifecycle and execution dispatch."""
    runtime = ReflectionFactory.create_runtime()
    await runtime.start()
    assert runtime.is_running is True

    req = ReflectionRequest(trace=sample_successful_trace)
    res = await runtime.process_completed_execution(req)
    assert res.lifecycle_state == ReflectionLifecycleState.COMPLETED

    await runtime.stop()
    assert runtime.is_running is False


# ---------------------------------------------------------------------------
# Part 2: Analyzers Tests
# ---------------------------------------------------------------------------

def test_analyzers_diagnostics(sample_successful_trace, sample_failed_trace):
    """Tests execution, plan, reasoning, decision, tool, and resource analyzers."""
    # Execution Analyzer
    exec_analyzer = ExecutionAnalyzer()
    res_exec = exec_analyzer.analyze_execution(sample_successful_trace)
    assert res_exec["total_tasks"] == 3
    assert res_exec["success_rate"] == 1.0

    # Plan Analyzer
    plan_analyzer = PlanAnalyzer()
    res_plan = plan_analyzer.analyze_plan(None, sample_successful_trace)
    assert res_plan["duplicated_task_count"] == 0
    assert res_plan["decomposition_efficiency_score"] == 1.0

    # Reasoning Analyzer
    reasoning_analyzer = ReasoningAnalyzer()
    res_reas = reasoning_analyzer.analyze_reasoning([
        {"confidence_score": 0.9, "evidence": ["E1"], "assumptions": []}
    ])
    assert res_reas["total_reasoning_steps"] == 1
    assert res_reas["reasoning_rigor_score"] == 0.9

    # Decision Analyzer
    dec_analyzer = DecisionAnalyzer()
    res_dec = dec_analyzer.analyze_decisions(sample_successful_trace.decisions)
    assert res_dec["policy_compliance_rate"] == 1.0

    # Tool Usage Analyzer
    tool_analyzer = ToolUsageAnalyzer()
    res_tool = tool_analyzer.analyze_tool_usage([
        {"tool_name": "t1", "success": True, "duration_ms": 100.0},
        {"tool_name": "t2", "success": False, "duration_ms": 500.0}
    ])
    assert res_tool["total_tool_calls"] == 2
    assert res_tool["reliability_rate"] == 0.5
    assert res_tool["slowest_tool"] == "t2"

    # Resource Analyzer
    resource_analyzer = ResourceAnalyzer()
    res_res = resource_analyzer.analyze_resources(sample_successful_trace)
    assert res_res["total_tokens"] == 1600
    assert res_res["cost_usd"] == 0.035

    # Performance Analyzer
    perf_analyzer = PerformanceAnalyzer()
    res_perf = perf_analyzer.analyze_performance(sample_successful_trace)
    assert res_perf["total_duration_ms"] == 4500.0

    # Failure Analyzer
    failure_analyzer = FailureAnalyzer()
    res_fail = failure_analyzer.analyze_failures(sample_failed_trace)
    assert res_fail["has_failures"] is True
    assert res_fail["failed_task_count"] == 1

    # Success Analyzer
    success_analyzer = SuccessAnalyzer()
    res_succ = success_analyzer.analyze_success(sample_successful_trace)
    assert res_succ["is_success"] is True
    assert res_succ["flawless_execution"] is True


# ---------------------------------------------------------------------------
# Part 3: Evaluators Tests
# ---------------------------------------------------------------------------

def test_all_dimensional_evaluators(sample_successful_trace):
    """Tests all 10 quantitative dimensional evaluators."""
    assert GoalEvaluator().evaluate(sample_successful_trace).score >= 0.8
    assert QualityEvaluator().evaluate(sample_successful_trace).score >= 0.8
    assert ConfidenceEvaluator().evaluate(sample_successful_trace).score >= 0.8
    assert CorrectnessEvaluator().evaluate(sample_successful_trace).score == 1.0
    assert EfficiencyEvaluator().evaluate(sample_successful_trace).score >= 0.8
    assert CostEvaluator().evaluate(sample_successful_trace).score >= 0.8
    assert LatencyEvaluator().evaluate(sample_successful_trace).score >= 0.8
    assert TokenEvaluator().evaluate(sample_successful_trace).score >= 0.8
    assert MemoryEvaluator().evaluate(sample_successful_trace).score >= 0.8
    assert RiskEvaluator().evaluate(sample_successful_trace).score >= 0.8


# ---------------------------------------------------------------------------
# Part 4 & 5: Critique & Detectors Tests
# ---------------------------------------------------------------------------

def test_hallucination_and_inconsistency_detection():
    """Tests detection of hallucinations, circular logic, and contradictions."""
    hallucination_trace = ExecutionTraceEnvelope(
        execution_id=uuid4(),
        final_state="COMPLETED",
        reasoning_steps=[
            ReasoningStepTrace(
                step_id="s1",
                rationale="Derived from nothing",
                evidence=["phantom_fact_99"],
                conclusion="Phantom claim asserted"
            )
        ]
    )

    detector = HallucinationDetector()
    findings = detector.detect_hallucinations(hallucination_trace)
    assert len(findings) == 1
    assert findings[0].category == "HALLUCINATION"

    # Inconsistency Detection
    contradiction_trace = ExecutionTraceEnvelope(
        execution_id=uuid4(),
        final_state="COMPLETED",
        reasoning_steps=[
            ReasoningStepTrace(step_id="s1", rationale="r1", conclusion="tax rate is high"),
            ReasoningStepTrace(step_id="s2", rationale="r2", conclusion="not tax rate is high"),
        ]
    )
    inconsistency_detector = InconsistencyDetector()
    incon_findings = inconsistency_detector.detect_inconsistencies(contradiction_trace)
    assert len(incon_findings) >= 1
    assert incon_findings[0].category == "INCONSISTENCY"


def test_bias_detector():
    """Tests bias detector identifying tool over-utilization skew."""
    skewed_trace = ExecutionTraceEnvelope(
        execution_id=uuid4(),
        final_state="COMPLETED",
        tool_calls=[
            ToolCallTrace(tool_name="heavy_tool") for _ in range(15)
        ] + [ToolCallTrace(tool_name="light_tool")]
    )
    bias_detector = BiasDetector()
    findings = bias_detector.detect_bias(skewed_trace)
    assert len(findings) == 1
    assert findings[0].category == "BIAS"


# ---------------------------------------------------------------------------
# Part 6: Learning Artifacts & Immutability Tests
# ---------------------------------------------------------------------------

def test_learning_artifacts_immutability(sample_successful_trace):
    """Verifies learning artifact generation and frozen immutability."""
    critique = CritiqueEngine().generate_critique(
        sample_successful_trace,
        EvaluationPipeline().run_pipeline(sample_successful_trace)
    )
    extractor = KnowledgeExtractor()
    artifacts = extractor.extract_artifacts(sample_successful_trace, critique)

    assert len(artifacts) >= 1
    art = artifacts[0]
    assert isinstance(art, LearningArtifact)

    # Verify immutability (frozen Pydantic model)
    with pytest.raises(Exception):
        art.title = "Modified Title"


# ---------------------------------------------------------------------------
# Part 7: Recommendations, Adaptation Proposals & Approvals
# ---------------------------------------------------------------------------

def test_recommendation_and_adaptation_lifecycle(sample_successful_trace):
    """Tests recommendation generation and formal adaptation proposal approval gate."""
    critique = CritiqueEngine().generate_critique(
        sample_successful_trace,
        EvaluationPipeline().run_pipeline(sample_successful_trace)
    )
    artifacts = KnowledgeExtractor().extract_artifacts(sample_successful_trace, critique)

    rec_engine = RecommendationEngine()
    recs = rec_engine.generate_recommendations(critique, artifacts)
    assert len(recs) >= 1

    adapt_engine = AdaptationEngine()
    proposals = adapt_engine.generate_proposals(recs)

    if proposals:
        prop = proposals[0]
        assert prop.status == AdaptationStatus.PROPOSED

        # Cannot activate without approval
        with pytest.raises(AdaptationApprovalRequiredError):
            prop.activate()

        # Approve and then activate
        approved_prop = prop.approve(approver_id="security_admin_1")
        assert approved_prop.status == AdaptationStatus.APPROVED
        assert approved_prop.approved_by == "security_admin_1"

        activated_prop = approved_prop.activate()
        assert activated_prop.status == AdaptationStatus.ACTIVATED


# ---------------------------------------------------------------------------
# Part 8: Subsystem Feedback Generation
# ---------------------------------------------------------------------------

def test_feedback_generation(sample_successful_trace):
    """Verifies typed feedback generation for Planner, Execution, Memory, and Tools."""
    critique = CritiqueEngine().generate_critique(
        sample_successful_trace,
        EvaluationPipeline().run_pipeline(sample_successful_trace)
    )
    recs = RecommendationEngine().generate_recommendations(critique, [])

    gen = FeedbackGenerator()
    bundle: SubsystemFeedbackBundle = gen.generate_feedback(critique, recs)

    assert isinstance(bundle.planner_feedback, PlannerFeedback)
    assert isinstance(bundle.execution_feedback, ExecutionFeedback)
    assert isinstance(bundle.memory_feedback, MemoryFeedback)
    assert isinstance(bundle.tool_feedback, ToolFeedback)
    assert bundle.planner_feedback.execution_id == sample_successful_trace.execution_id


# ---------------------------------------------------------------------------
# Part 9: Pattern Detection, Trends & Root Cause
# ---------------------------------------------------------------------------

def test_patterns_trends_and_root_cause(sample_successful_trace, sample_failed_trace):
    """Tests cross-run pattern detection, trend analysis, and root cause discovery."""
    pattern_detector = PatternDetector()
    patterns = pattern_detector.detect_patterns(sample_failed_trace, [sample_failed_trace])
    assert len(patterns) >= 1
    assert patterns[0].pattern_type in ("RECURRING_FAILURE", "TOOL_DEGRADATION")

    trend_analyzer = TrendAnalyzer()
    trends = trend_analyzer.analyze_trends(sample_successful_trace, [sample_successful_trace])
    assert trends.sample_size == 2
    assert trends.latency_trend in ("STABLE", "INCREASING", "DECREASING")

    rc_analyzer = ReflectionRootCauseAnalyzer()
    root_cause = rc_analyzer.analyze_root_cause(sample_failed_trace)
    assert root_cause is not None
    assert root_cause.primary_fault_domain == "TOOL"


def test_comparative_benchmark_and_scoring(sample_successful_trace):
    """Tests comparison against baseline, benchmark thresholds, and composite scoring."""
    comp_analyzer = ComparativeAnalyzer()
    comp_result = comp_analyzer.compare_traces(sample_successful_trace, sample_successful_trace)
    assert comp_result.is_improvement is True

    benchmarker = BenchmarkEvaluator(BenchmarkCriteria(max_duration_ms=10000.0, max_cost_usd=0.10))
    bench_report = benchmarker.evaluate_benchmark(sample_successful_trace)
    assert bench_report.passed_all is True

    scorer = CompositeScorer()
    eval_report = EvaluationPipeline().run_pipeline(sample_successful_trace)
    comp_score = scorer.compute_composite_score(eval_report)
    assert 0.0 <= comp_score <= 1.0


# ---------------------------------------------------------------------------
# Part 10: Serialization & Versioning
# ---------------------------------------------------------------------------

def test_serialization_round_trip(sample_successful_trace):
    """Tests Pydantic v2 JSON serialization and Cloud Tasks/PubSub encoding."""
    req = ReflectionRequest(trace=sample_successful_trace)
    json_str = ReflectionSerializer.serialize_to_json(req)
    assert "schema_version" in json_str
    assert "20.0" in json_str

    deserialized: ReflectionRequest = ReflectionSerializer.deserialize_from_json(
        json_str, ReflectionRequest
    )
    assert deserialized.trace.execution_id == sample_successful_trace.execution_id

    pubsub_msg = ReflectionSerializer.to_pubsub_message(req)
    assert "data" in pubsub_msg
    assert pubsub_msg["attributes"]["schema_version"] == "20.0"


# ---------------------------------------------------------------------------
# Part 11: Fail-Fast Validators Tests
# ---------------------------------------------------------------------------

def test_validators_fail_fast():
    """Tests validation errors on invalid inputs, malformed recommendations, and out-of-bound scores."""
    with pytest.raises(InvalidConfidenceScoreError):
        ReflectionValidator.validate_confidence_score(1.5)

    with pytest.raises(InvalidConfidenceScoreError):
        ReflectionValidator.validate_confidence_score(-0.2)

    with pytest.raises(MalformedRecommendationError):
        ReflectionValidator.validate_recommendation(
            Recommendation(
                target_subsystem=SubsystemTarget.PLANNER,
                title="",
                rationale="valid",
                expected_impact="gain"
            )
        )

    # Evaluation DAG cycle detection
    graph = EvaluationGraph()
    graph.add_stage(EvaluationStageNode(stage_id="s1", evaluator_name="e1", dimension="d1", dependencies=["s2"]))
    graph.add_stage(EvaluationStageNode(stage_id="s2", evaluator_name="e2", dimension="d2", dependencies=["s1"]))
    with pytest.raises(InvalidEvaluationGraphError):
        graph.get_execution_order()


# ---------------------------------------------------------------------------
# Part 12: Fluent Builders Tests
# ---------------------------------------------------------------------------

def test_builders_suite():
    """Verifies fluent builders for request, artifact, recommendation, critique, evaluation, and feedback."""
    exec_id = uuid4()

    # Request Builder
    req = (
        ReflectionRequestBuilder(execution_id=exec_id)
        .with_goal("Test Goal")
        .with_duration(1500.0)
        .with_cost(0.01)
        .with_tokens(100, 50)
        .with_outputs({"status": "ok"})
        .build()
    )
    assert req.trace.execution_id == exec_id
    assert req.trace.goal == "Test Goal"

    # Artifact Builder
    art = (
        LearningArtifactBuilder(source_execution_id=exec_id)
        .with_type(LearningArtifactType.PLANNER_HEURISTIC)
        .with_title("Planner Heuristic")
        .with_confidence(0.92)
        .build()
    )
    assert art.title == "Planner Heuristic"

    # Recommendation Builder
    rec = (
        RecommendationBuilder(target_subsystem=SubsystemTarget.PLANNER)
        .with_title("Test Rec")
        .with_rationale("Rationale")
        .with_expected_impact("Impact")
        .build()
    )
    assert rec.target_subsystem == SubsystemTarget.PLANNER

    # Critique Builder
    critique = (
        CritiqueBuilder(execution_id=exec_id)
        .add_strength("High performance")
        .add_opportunity("Refactor subtasks")
        .build()
    )
    assert len(critique.strengths) == 1

    # Feedback Builder
    bundle = FeedbackBuilder(execution_id=exec_id).build()
    assert bundle.planner_feedback.execution_id == exec_id


# ---------------------------------------------------------------------------
# Part 13: Repositories & Cache Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_repositories_and_cache(sample_successful_trace):
    """Tests in-memory repositories and LRU/TTL cache operations."""
    repo = InMemoryReflectionRepository()
    ref = Reflection(
        identity=ReflectionIdentity(execution_id=sample_successful_trace.execution_id)
    )
    await repo.save(ref)
    retrieved = await repo.get_by_id(ref.identity.reflection_id)
    assert retrieved is not None
    assert retrieved.identity.execution_id == sample_successful_trace.execution_id

    # Cache test
    cache = ReflectionCache(capacity=2, ttl_seconds=300.0)
    cache.put("key1", "val1")
    cache.put("key2", "val2")
    assert cache.get("key1") == "val1"

    # Eviction test
    cache.put("key3", "val3")
    assert cache.size() == 2
    assert cache.get("key2") is None  # key2 was LRU when key1 was accessed
    assert cache.get("key1") == "val1"
    assert cache.get("key3") == "val3"


# ---------------------------------------------------------------------------
# Part 14: Metrics Collector Tests
# ---------------------------------------------------------------------------

def test_metrics_collector():
    """Tests metric recording and Cloud Monitoring export format."""
    collector = ReflectionMetricsCollector()
    collector.record_reflection_started()
    collector.record_reflection_completed(250.0)
    collector.record_evaluation(10)
    collector.record_artifacts(3)
    collector.record_recommendations(2)

    snap = collector.get_metrics_snapshot()
    assert snap.total_reflections_completed == 1
    assert snap.average_reflection_duration_ms == 250.0
    assert snap.total_evaluations_executed == 10

    exported = collector.export_cloud_monitoring_format()
    assert "custom.googleapis.com/agent/reflection/completed_count" in exported
    assert exported["custom.googleapis.com/agent/reflection/completed_count"] == 1
