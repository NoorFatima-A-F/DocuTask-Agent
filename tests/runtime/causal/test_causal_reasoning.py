from app.runtime.causal.structural_causal_model import StructuralCausalModel
from app.runtime.causal.do_calculus import DoCalculusEngine
from app.runtime.causal.causal_discovery import CausalDiscoveryEngine


def test_structural_causal_model():
    scm = StructuralCausalModel()
    nodes = scm.list_nodes()
    assert len(nodes) == 5
    assert scm.get_node("worker_concurrency").is_treatment is True
    assert scm.get_node("total_latency_ms").is_outcome is True


def test_do_calculus_intervention():
    engine = DoCalculusEngine()
    res = engine.evaluate_do_intervention(
        treatment_var="worker_concurrency",
        treatment_val=8.0,
        outcome_var="total_latency_ms",
    )
    assert res.treatment_variable == "worker_concurrency"
    assert res.target_outcome_variable == "total_latency_ms"
    assert "doc_complexity" in res.confounder_backdoor_set
    assert res.interventional_expectation_e_y_do_x > 0


def test_counterfactual_reasoning():
    engine = DoCalculusEngine()
    factual = {"worker_concurrency": 2.0, "total_latency_ms": 1200.0}
    action = {"worker_concurrency": 8.0}
    
    cf_res = engine.evaluate_counterfactual(factual, action)
    assert "total_latency_ms" in cf_res.counterfactual_outcomes
    assert cf_res.counterfactual_outcomes["total_latency_ms"] < 1200.0
    assert cf_res.counterfactual_delta < 0  # Latency reduced


def test_causal_discovery():
    discovery = CausalDiscoveryEngine()
    report = discovery.discover_causal_graph(execution_traces_count=1000)
    assert len(report.discovered_edges) >= 4
    assert "doc_complexity" in report.identified_confounders
