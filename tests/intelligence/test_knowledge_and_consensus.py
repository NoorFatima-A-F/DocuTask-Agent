"""
Tests for Knowledge Graph, Consensus, Routing, Prediction, Org Learning & Continuous Improvement (Pillars 6-11).
"""

from app.runtime.intelligence.consensus.consensus_engine import (
    AgentContribution,
    ConsensusEngine,
)
from app.runtime.intelligence.continuous.continuous_improvement import (
    ContinuousImprovementEngine,
    ImprovementStage,
)
from app.runtime.intelligence.experience import (
    ExperienceExtractor,
    ExperienceStore,
)
from app.runtime.intelligence.knowledge.graph_query import GraphQueryEngine
from app.runtime.intelligence.knowledge.knowledge_graph import (
    AdaptiveKnowledgeGraph,
    GraphEdge,
    GraphNode,
)
from app.runtime.intelligence.organizational.org_learning import OrgLearningEngine
from app.runtime.intelligence.predictive.predictive_mission import (
    PredictiveMissionEngine,
)
from app.runtime.intelligence.routing.adaptive_routing import (
    AdaptiveResourceOptimizer,
)


def test_knowledge_graph_and_queries():
    kg = AdaptiveKnowledgeGraph()
    kg.add_node(GraphNode(node_id="doc_inv", node_type="ENTITY", label="Invoice"))
    kg.add_node(GraphNode(node_id="strat_1", node_type="STRATEGY", label="Invoice Fast Route"))
    kg.add_edge(GraphEdge(edge_id="e1", source_id="doc_inv", target_id="strat_1", relationship="APPLIES_STRATEGY", evidence_hash="0x123"))

    query = GraphQueryEngine(kg)
    strats = query.find_strategies_for_domain("Invoice")
    assert len(strats) == 1
    assert strats[0]["strategy_id"] == "strat_1"
    assert strats[0]["evidence_hash"] == "0x123"


def test_consensus_engine_weighted_evidence():
    engine = ConsensusEngine()
    contribs = [
        AgentContribution(
            agent_id="Agent1",
            department="Ops",
            confidence=0.98,
            recommendation="APPROVE",
            risk_score=0.02,
            supporting_evidence_hashes=["0xabc", "0xdef"],
        ),
        AgentContribution(
            agent_id="Agent2",
            department="QA",
            confidence=0.92,
            recommendation="APPROVE",
            risk_score=0.05,
            supporting_evidence_hashes=["0xabc"],
        ),
        AgentContribution(
            agent_id="Agent3",
            department="Risk",
            confidence=0.70,
            recommendation="REJECT",
            risk_score=0.30,
        ),
    ]

    res = engine.evaluate_consensus(contribs)
    assert res.winning_recommendation == "APPROVE"
    assert res.agreement_score > 0.70
    assert res.dominant_evidence_hash == "0xabc"


def test_predictive_mission_and_routing():
    pred_engine = PredictiveMissionEngine()
    routing = AdaptiveResourceOptimizer()

    pred = pred_engine.forecast_mission("msn_test", "invoice", "extraction")
    assert pred.predicted_latency_ms > 0
    assert pred.predicted_cost_usd > 0

    evaluated = pred_engine.evaluate_actuals(
        pred.prediction_id,
        {"total_latency_ms": pred.predicted_latency_ms * 1.05, "total_cost_usd": pred.predicted_cost_usd},
    )
    assert evaluated is not None
    assert evaluated.prediction_accuracy_score > 0.85

    prof = routing.get_profile("invoice")
    assert prof.document_domain == "invoice"


def test_org_learning_and_continuous_improvement():
    store = ExperienceStore()
    extractor = ExperienceExtractor(store)

    exps = []
    for i in range(5):
        e = extractor.extract_from_mission(
            mission_id=f"msn_ci_{i}",
            document_type="invoice",
            task_type="extraction",
            telemetry={"total_latency_ms": 1100.0, "total_cost_usd": 0.012, "final_confidence": 0.96},
        )
        exps.append(e)

    org = OrgLearningEngine()
    org.record_mission_outcome("Financial Operations", exps[0])
    dept = org.get_department("fin_ops")
    assert dept is not None
    assert dept.total_missions_executed > 0

    ci = ContinuousImprovementEngine()
    pipe = ci.initiate_cycle("invoice", exps, auto_deploy=True)
    assert pipe.stage == ImprovementStage.DEPLOYED
    assert pipe.deployed_version_id is not None
    assert pipe.p_value is not None

    # Rollback
    rolled = ci.rollback_pipeline(pipe.pipeline_id)
    assert rolled is True
    assert pipe.stage == ImprovementStage.ROLLED_BACK
