"""
Unit and Integration Tests for SCM & Pearl's do-Calculus (ASVSP Pillar 7).
"""

import pytest
from app.runtime.causal_analysis import (
    StructuralCausalModel,
    DoCalculusEngine,
    CausalAttributionEngine,
    CausalAnalysisEngine,
)


def test_scm_dag():
    scm = StructuralCausalModel()
    nodes = scm.list_nodes()
    assert len(nodes) >= 7

    adj = scm.get_backdoor_adjustment_set("model_choice", "accuracy")
    assert "complexity" in adj


def test_do_calculus():
    res = DoCalculusEngine.estimate_intervention(
        treatment="model_choice",
        treatment_val="gemini-1.5-pro",
        outcome="accuracy",
        baseline_val="gemini-2.5-flash",
    )
    assert res.average_treatment_effect > 0.0
    assert res.backdoor_strata_count == 3


def test_root_cause_attribution():
    items = CausalAttributionEngine.attribute_anomaly(
        target_metric="latency_ms",
        observed_value=2500.0,
        expected_baseline=480.0,
        observed_retry_count=3,
        observed_ocr_confidence=0.65,
    )
    assert len(items) >= 3
    root_cause = next(item for item in items if item.is_root_cause)
    assert root_cause.node_id == "ocr_noise"


def test_causal_engine_facade():
    engine = CausalAnalysisEngine()
    graph = engine.get_causal_graph()
    assert "nodes" in graph

    do_res = engine.simulate_do_intervention()
    assert "average_treatment_effect" in do_res
