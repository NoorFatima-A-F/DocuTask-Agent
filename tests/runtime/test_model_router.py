"""
Unit & Optimization Tests for Model Router (QDIOP / SDIOP).
"""

import pytest
from app.runtime.routing import (
    ScientificModelRouter,
    RoutingOptimizer,
    AVAILABLE_MODELS,
    routing_history,
)


def test_routing_optimizer_evaluates_all_registered_models():
    evaluated = RoutingOptimizer.evaluate_models(
        document_complexity=0.4,
        token_estimate=2000,
    )
    assert len(evaluated) == len(AVAILABLE_MODELS)
    assert all("expected_utility" in m for m in evaluated)
    assert evaluated[0]["expected_utility"] >= evaluated[-1]["expected_utility"]


def test_scientific_model_router_selection_and_provenance():
    res = ScientificModelRouter.route_task(
        task_id="task_doc_99",
        document_complexity=0.3,
        token_estimate=1500,
    )
    assert res["selected_model"] != ""
    assert res["expected_utility"] > 0.0
    assert res["is_valid"]
    assert len(routing_history.list_recent()) > 0
