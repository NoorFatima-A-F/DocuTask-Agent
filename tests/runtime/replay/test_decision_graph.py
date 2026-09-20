"""
Unit Tests for Decision DAG Graph Construction.
"""

import pytest
from app.runtime.decision.provenance_engine import DecisionProvenanceEngine
from app.runtime.decision.decision_graph import DecisionGraphBuilder


def test_decision_graph_causal_edges():
    d1 = DecisionProvenanceEngine.create_decision(
        decision_id="d_goal",
        mission_id="mission_dag_01",
        goal="Parse Invoice Structure",
        selected_plan="Multi-Table Layout Strategy",
        why_chosen="Invoice contains complex line item matrices",
    )
    d2 = DecisionProvenanceEngine.create_decision(
        decision_id="d_worker",
        mission_id="mission_dag_01",
        goal="Assign OCR Engine",
        selected_plan="Vision GPU Worker",
        why_chosen="Hardware acceleration enabled",
        parent_decision_id="d_goal",
    )
    d3 = DecisionProvenanceEngine.create_decision(
        decision_id="d_val",
        mission_id="mission_dag_01",
        goal="Validate Calculations",
        selected_plan="Z3 SMT Invariant Solver",
        why_chosen="Formal verification requirement",
        parent_decision_id="d_worker",
    )

    graph = DecisionGraphBuilder.build_graph("mission_dag_01", [d1, d2, d3])

    assert graph.total_decisions == 3
    assert len(graph.nodes) == 3
    assert len(graph.edges) == 2
    assert graph.edges[0].source == "d_goal"
    assert graph.edges[0].target == "d_worker"
    assert graph.edges[1].source == "d_worker"
    assert graph.edges[1].target == "d_val"
