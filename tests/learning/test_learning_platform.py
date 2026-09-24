"""
Comprehensive Pytest Test Suite for Phase 13.5:
Autonomous Reflection, Learning, Policy Evolution & Knowledge Intelligence Platform (ARLP-KIP).
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.runtime.learning.events.learning_events import (
    ReflectionStarted,
    ReflectionCompleted,
    PatternDetected,
    KnowledgeExtracted,
    LessonPublished,
    PolicyProposed,
    PolicyApproved,
    PolicyRejected,
    KnowledgeVersionCreated,
    KnowledgeDeprecated,
    StrategyGenerated,
    StrategyAdopted,
    LearningCompleted,
)
from app.runtime.learning.reflection.reflection_engine import ReflectionEngine
from app.runtime.learning.reflection.mission_reflector import MissionReflector
from app.runtime.learning.reflection.planner_reflector import PlannerReflector
from app.runtime.learning.reflection.worker_reflector import WorkerReflector
from app.runtime.learning.reflection.confidence_reflector import ConfidenceReflector
from app.runtime.learning.reflection.failure_reflector import FailureReflector
from app.runtime.learning.reflection.success_reflector import SuccessReflector
from app.runtime.learning.reflection.reflection_validator import ReflectionValidator

from app.runtime.learning.learning.learning_engine import LearningEngine
from app.runtime.learning.learning.pattern_miner import PatternMiner
from app.runtime.learning.learning.lesson_extractor import LessonExtractor
from app.runtime.learning.learning.strategy_builder import StrategyBuilder
from app.runtime.learning.learning.knowledge_compiler import KnowledgeCompiler
from app.runtime.learning.learning.experience_ranker import ExperienceRanker
from app.runtime.learning.learning.learning_validator import LearningValidator

from app.runtime.learning.knowledge.knowledge_registry import KnowledgeRegistry
from app.runtime.learning.knowledge.knowledge_graph import KnowledgeGraph
from app.runtime.learning.knowledge.knowledge_lineage import KnowledgeLineageTracker

from app.runtime.learning.policy.policy_engine import PolicyEngine
from app.runtime.learning.policy.policy_registry import EvolutionPolicyRegistry

from app.runtime.learning.governance.learning_governance import LearningGovernanceGatekeeper
from app.runtime.learning.governance.approval_workflow import ApprovalWorkflowManager
from app.runtime.learning.governance.promotion_pipeline import PromotionPipelineManager
from app.runtime.learning.governance.rollback_manager import rollback_manager
from app.runtime.learning.governance.policy_guardrails import PolicyGuardrailsValidator


@pytest.fixture
def client():
    return TestClient(app)


# ---------------------------------------------------------------------------
# 1. Domain Event Model Tests
# ---------------------------------------------------------------------------

def test_learning_domain_events_instantiation():
    e1 = ReflectionStarted(mission_id="mission-001")
    assert e1.event_type == "learning.reflection.started"
    assert e1.mission_id == "mission-001"

    e2 = ReflectionCompleted(mission_id="mission-001", reflection_id="ref-001", overall_efficiency=0.92)
    assert e2.event_type == "learning.reflection.completed"
    assert e2.overall_efficiency == 0.92

    e3 = PatternDetected(mission_id="mission-001", pattern_id="pat-001", pattern_type="SEQUENTIAL_BURST", frequency=4)
    assert e3.pattern_type == "SEQUENTIAL_BURST"

    e4 = KnowledgeExtracted(mission_id="mission-001", knowledge_id="kn-001", confidence=0.95)
    assert e4.confidence == 0.95

    e5 = LessonPublished(mission_id="mission-001", lesson_id="ls-001", rule_count=3)
    assert e5.rule_count == 3

    e6 = PolicyProposed(mission_id="mission-001", candidate_id="cand-001", target_component="planner")
    assert e6.target_component == "planner"

    e7 = PolicyApproved(mission_id="mission-001", candidate_id="cand-001", reviewer_id="rev-01")
    assert e7.reviewer_id == "rev-01"

    e8 = PolicyRejected(mission_id="mission-001", candidate_id="cand-001", reason="Risk too high")
    assert e8.reason == "Risk too high"

    e9 = KnowledgeVersionCreated(mission_id="mission-001", record_id="rec-001", version="1.1.0")
    assert e9.version == "1.1.0"

    e10 = KnowledgeDeprecated(mission_id="mission-001", record_id="rec-001")
    assert e10.event_type == "learning.knowledge.deprecated"

    e11 = StrategyGenerated(mission_id="mission-001", strategy_id="strat-001", goal_type="EXTRACTION")
    assert e11.goal_type == "EXTRACTION"

    e12 = StrategyAdopted(mission_id="mission-001", strategy_id="strat-001")
    assert e12.event_type == "learning.strategy.adopted"

    e13 = LearningCompleted(mission_id="mission-001", total_lessons=3, total_policies=1)
    assert e13.total_lessons == 3



# ---------------------------------------------------------------------------
# 2. Reflection Subsystem Tests
# ---------------------------------------------------------------------------

def test_reflection_engine_generate_report():
    engine = ReflectionEngine()
    report = engine.reflect_on_mission("mission-test-01")
    
    assert report.mission_id == "mission-test-01"
    assert report.macro_kpis.throughput_tasks_per_sec > 0
    assert report.macro_kpis.sla_adherence_rate >= 0.0
    assert report.planner_metrics.total_goals_planned > 0
    assert report.worker_metrics.average_tool_reliability >= 0.0
    assert report.confidence_metrics.avg_confidence >= 0.0
    assert report.validation_status in ["VERIFIED", "VALID"]
    assert len(engine.list_reports()) >= 1


def test_reflection_components():
    m_kpi = MissionReflector.reflect("mission-001")
    assert m_kpi.mission_id == "mission-001"
    assert m_kpi.execution_duration_sec > 0

    p_met = PlannerReflector.reflect("mission-001")
    assert p_met.total_goals_planned >= 1

    w_met = WorkerReflector.reflect("mission-001")
    assert w_met.worker_utilization_rate > 0

    c_met = ConfidenceReflector.reflect("mission-001")
    assert c_met.min_confidence <= c_met.max_confidence

    failures = FailureReflector.reflect("mission-001")
    assert isinstance(failures, list)

    successes = SuccessReflector.reflect("mission-001")
    assert isinstance(successes, list)
    assert len(successes) >= 1


def test_reflection_validator():
    engine = ReflectionEngine()
    report = engine.reflect_on_mission("mission-val-01")
    val_res = ReflectionValidator.validate(report)
    assert val_res.is_valid is True
    assert len(val_res.errors) == 0


# ---------------------------------------------------------------------------
# 3. Learning & Pattern Mining Subsystem Tests
# ---------------------------------------------------------------------------

def test_learning_engine_mine_lessons():
    r_engine = ReflectionEngine()
    report = r_engine.reflect_on_mission("mission-learn-01")

    l_engine = LearningEngine()
    lesson = l_engine.mine_lessons(report)

    assert lesson.mission_id == "mission-learn-01"
    assert len(lesson.mined_patterns) >= 1
    assert len(lesson.extracted_rules) >= 1
    assert lesson.compiled_strategy is not None
    assert lesson.confidence_score > 0.5
    assert len(l_engine.list_lessons()) >= 1


def test_pattern_miner_and_lesson_extractor():
    patterns = PatternMiner.mine_patterns("mission-001")
    assert len(patterns) >= 1
    assert patterns[0].pattern_type in ["PARALLEL_WAVEFRONT", "FALLBACK_CASCADE", "CONFIDENCE_DECAY_RECOVERY"]

    rules = LessonExtractor.extract_rules(patterns)
    assert len(rules) >= 1
    assert rules[0].actionable_guidance != ""

    strategy = StrategyBuilder.build_strategy(rules, goal_type="DYNAMIC_EXTRACTION")
    assert strategy.strategy_id is not None
    assert len(strategy.prescribed_tactics) >= 1

    bundle = KnowledgeCompiler.compile_bundle(lesson_id="ls-001", rules=rules, strategy=strategy)
    assert bundle.bundle_hash != ""

    ranked = ExperienceRanker.rank_experiences([
        {"id": "exp-1", "success_rate": 0.95, "confidence": 0.9},
        {"id": "exp-2", "success_rate": 0.70, "confidence": 0.6},
    ])
    assert ranked[0].experience_id == "exp-1"

    val = LearningValidator.validate_lesson(lesson_id="ls-001", rules=rules, confidence=0.88)
    assert val.is_valid is True


# ---------------------------------------------------------------------------
# 4. Knowledge Registry, Graph & Lineage Tests
# ---------------------------------------------------------------------------

def test_knowledge_registry_crud_and_search():
    reg = KnowledgeRegistry()
    record = reg.register_record(
        title="OCR Concurrency Optimization Rule",
        category="EXECUTION_RULE",
        source_mission_id="mission-001",
        confidence_score=0.94,
        content={"concurrency": 8, "batch_size": 16},
        tags=["ocr", "optimization", "performance"],
    )

    assert record.record_id.startswith("kn_")
    assert record.version == "1.0.0"
    assert record.content_hash != ""

    fetched = reg.get_record(record.record_id)
    assert fetched is not None
    assert fetched.title == "OCR Concurrency Optimization Rule"

    all_records = reg.list_records(category="EXECUTION_RULE")
    assert len(all_records) >= 1


def test_knowledge_graph_and_lineage():
    kg = KnowledgeGraph()
    kg.add_node("node-1", "Rule A", "RULE", {"confidence": 0.9})
    kg.add_node("node-2", "Strategy B", "STRATEGY", {"confidence": 0.85})
    kg.add_edge("node-1", "node-2", "ENABLES", weight=0.8)

    graph_dict = kg.to_dict()
    assert len(graph_dict["nodes"]) >= 2
    assert len(graph_dict["edges"]) >= 1

    # Lineage
    lineage = KnowledgeLineageTracker()
    r1 = lineage.record_origin("rec-100", "1.0.0", "mission-001", "hash_v1")
    assert r1.parent_hash is None
    assert lineage.verify_chain_integrity("rec-100") is True

    r2 = lineage.record_evolution("rec-100", "1.1.0", "mission-002", "hash_v2", "Updated parameters")
    assert r2.parent_hash == r1.lineage_hash
    assert lineage.verify_chain_integrity("rec-100") is True


# ---------------------------------------------------------------------------
# 5. Policy Engine, Simulation & Evolution Tests
# ---------------------------------------------------------------------------

def test_policy_engine_proposal_and_evaluation():
    p_engine = PolicyEngine()
    candidate = p_engine.propose_candidate(
        target_component="planner",
        policy_name="Dynamic Replanning Policy",
        parameters={"max_retries": 3, "concurrency_limit": 8, "confidence_threshold": 0.85},
        evidence_lessons=["ls-001"],
    )

    assert candidate.candidate_id.startswith("cand_")
    assert candidate.status == "PROPOSED"


    evaluation = p_engine.evaluate_candidate(candidate.candidate_id)
    assert evaluation.simulation_id is not None
    assert evaluation.projected_throughput_gain_pct >= 0.0
    assert candidate.status in ["EVALUATED", "PROPOSED"]


def test_policy_registry_and_versioning():
    reg = EvolutionPolicyRegistry()
    active = reg.list_active_policies()
    assert len(active) >= 1

    p = active[0]
    entry = reg.get_active_policy(p.policy_id)
    assert entry is not None


# ---------------------------------------------------------------------------
# 6. Governance, Guardrails & Rollback Tests
# ---------------------------------------------------------------------------

def test_governance_gatekeeper_and_approval():
    gatekeeper = LearningGovernanceGatekeeper()
    evaluation = gatekeeper.evaluate_candidate_for_promotion(
        candidate_id="cand-001",
        projected_gain=12.5,
        risk_score=0.15,
        confidence=0.91,
    )
    assert evaluation.decision in ["APPROVED", "REJECTED", "MANUAL_REVIEW_REQUIRED"]

    approval_mgr = ApprovalWorkflowManager()
    review = approval_mgr.record_review("cand-001", reviewer_id="gov-admin", decision="APPROVED", comments="LGTM")
    assert review.decision == "APPROVED"

    promotion_mgr = PromotionPipelineManager()
    prom_res = promotion_mgr.promote("cand-001", promoter_id="ci-deployer")
    assert prom_res.status in ["PROMOTED", "REJECTED"]


def test_rollback_and_guardrails():
    guardrails_spec = PolicyGuardrailsValidator.get_guardrail_spec()
    assert "max_retries" in guardrails_spec
    assert "confidence_threshold" in guardrails_spec

    is_safe = PolicyGuardrailsValidator.validate_parameters({
        "max_retries": 3,
        "concurrency_limit": 10,
        "confidence_threshold": 0.85,
    })
    assert is_safe.is_compliant is True

    unsafe = PolicyGuardrailsValidator.validate_parameters({
        "max_retries": 100,  # Exceeds max 10
        "confidence_threshold": 0.10,  # Below min 0.50
    })
    assert unsafe.is_compliant is False

    rb_res = rollback_manager.rollback("pol-baseline-planner", operator_id="admin-01", reason="Testing rollback mechanism")
    assert rb_res.status == "ROLLED_BACK"


# ---------------------------------------------------------------------------
# 7. FastAPI Endpoints Integration Tests
# ---------------------------------------------------------------------------

def test_api_reflection_endpoints(client: TestClient):
    resp = client.get("/api/v1/learning/reflection/mission/mission-001")
    assert resp.status_code == 200
    data = resp.json()
    assert data["mission_id"] == "mission-001"
    assert "macro_kpis" in data

    resp_hist = client.get("/api/v1/learning/reflection/history")
    assert resp_hist.status_code == 200
    assert isinstance(resp_hist.json(), list)


def test_api_learning_and_knowledge_endpoints(client: TestClient):
    resp_mine = client.post("/api/v1/learning/learning/mine", json={"mission_id": "mission-001"})
    assert resp_mine.status_code == 200
    data = resp_mine.json()
    assert "mined_patterns" in data

    resp_patterns = client.get("/api/v1/learning/learning/patterns")
    assert resp_patterns.status_code == 200
    assert isinstance(resp_patterns.json(), list)

    resp_lessons = client.get("/api/v1/learning/learning/lessons")
    assert resp_lessons.status_code == 200
    assert isinstance(resp_lessons.json(), list)

    resp_strategies = client.get("/api/v1/learning/learning/strategies")
    assert resp_strategies.status_code == 200
    assert isinstance(resp_strategies.json(), list)

    resp_ingest = client.post("/api/v1/learning/knowledge/records", json={
        "title": "Adaptive Resiliency Buffer",
        "category": "RESILIENCE_STRATEGY",
        "source_mission_id": "mission-001",
        "confidence_score": 0.92,
        "content": {"buffer_size": 64},
        "tags": ["resilience", "buffer"],
    })
    assert resp_ingest.status_code == 201
    rec_data = resp_ingest.json()
    assert rec_data["title"] == "Adaptive Resiliency Buffer"

    resp_records = client.get("/api/v1/learning/knowledge/records")
    assert resp_records.status_code == 200
    assert len(resp_records.json()) >= 1

    resp_graph = client.get("/api/v1/learning/knowledge/graph")
    assert resp_graph.status_code == 200
    assert "nodes" in resp_graph.json()

    resp_search = client.get("/api/v1/learning/knowledge/search?q=resilience")
    assert resp_search.status_code == 200
    assert isinstance(resp_search.json(), list)


def test_api_policy_and_governance_endpoints(client: TestClient):
    resp_prop = client.post("/api/v1/learning/policy/propose", json={
        "target_component": "planner",
        "policy_name": "API Proposed Policy",
        "parameters": {"max_retries": 4, "concurrency_limit": 6, "confidence_threshold": 0.85},
        "evidence_lessons": ["ls-001"],
    })
    assert resp_prop.status_code == 200
    candidate = resp_prop.json()
    cand_id = candidate["candidate_id"]

    resp_eval = client.post("/api/v1/learning/policy/evaluate", json={"candidate_id": cand_id})
    assert resp_eval.status_code == 200

    resp_active = client.get("/api/v1/learning/policy/active")
    assert resp_active.status_code == 200
    assert len(resp_active.json()) >= 1

    resp_rev = client.post("/api/v1/learning/governance/review", json={
        "candidate_id": cand_id,
        "reviewer_id": "admin-reviewer",
        "decision": "APPROVED",
        "comments": "Meets performance requirements.",
    })
    assert resp_rev.status_code == 200

    resp_prom = client.post("/api/v1/learning/governance/promote", json={"candidate_id": cand_id, "promoter_id": "api-deployer"})
    assert resp_prom.status_code == 200

    resp_guard = client.get("/api/v1/learning/governance/guardrails")
    assert resp_guard.status_code == 200

    resp_analytics = client.get("/api/v1/learning/analytics/summary")
    assert resp_analytics.status_code == 200
    summary = resp_analytics.json()
    assert "total_reflections" in summary
    assert "avg_confidence_score" in summary
