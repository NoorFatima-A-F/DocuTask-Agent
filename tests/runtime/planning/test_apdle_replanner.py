"""
Unit & Integration Tests for Runtime Graph Mutation, Adaptive Replanner, and Strategy Switcher.
"""

from app.runtime.planning.graph.graph_builder import ExecutionGraphBuilder
from app.runtime.planning.graph.graph_mutator import GraphMutator
from app.runtime.planning.graph.node import DAGNode
from app.runtime.planning.replanning.replanner import AdaptiveReplanner
from app.runtime.planning.replanning.strategy_switch import PlanningStrategy, StrategySwitcher


def test_graph_mutator_node_insertion():
    """Verifies in-flight insertion of a node between parent and child."""
    dag = ExecutionGraphBuilder.build_financial_invoice_audit_dag(mission_id="m-mutate")
    initial_nodes_count = len(dag.nodes)

    filter_node = DAGNode(
        node_id="node_filter_contrast",
        mission_id="m-mutate",
        name="Adaptive Contrast Filter",
        task_type="IMAGE_PROCESSING",
    )

    rec = GraphMutator.insert_node_between(
        dag=dag,
        new_node=filter_node,
        parent_node_id="node_ocr_01",
        child_node_id="node_extract_items",
        reason="Low image contrast detected",
    )

    assert rec.mutation_type == "INSERT_NODE"
    assert len(dag.nodes) == initial_nodes_count + 1
    assert "node_filter_contrast" in dag.nodes
    assert dag.has_cycle() is False


def test_adaptive_replanner_on_node_failure():
    """Verifies that AdaptiveReplanner injects dedicated recovery subgraphs upon task failure."""
    dag = ExecutionGraphBuilder.build_financial_invoice_audit_dag(mission_id="m-replan")
    replanner = AdaptiveReplanner()

    rec = replanner.handle_node_failure(
        dag=dag,
        failed_node_id="node_ocr_01",
        error_reason="Image skewed and unreadable",
    )

    assert rec.mutation_type == "INJECT_RECOVERY"
    assert rec.nodes_added_count == 2
    assert len(dag.nodes) == 7
    assert len(replanner.mutation_history) == 1
    assert dag.has_cycle() is False


def test_strategy_switcher():
    """Verifies automatic switching of planning strategies based on runtime pressure."""
    # Low budget -> COST_OPTIMIZED
    rec = StrategySwitcher.evaluate_and_switch(
        mission_id="m-strat",
        current_strategy=PlanningStrategy.PROBABILISTIC,
        budget_remaining_usd=0.001,
        latency_budget_ms=2000.0,
        current_error_rate=0.05,
    )
    assert rec.new_strategy == PlanningStrategy.COST_OPTIMIZED
    assert rec.expected_cost_delta_usd < 0

    # High error rate -> RISK_OPTIMIZED
    rec2 = StrategySwitcher.evaluate_and_switch(
        mission_id="m-strat",
        current_strategy=PlanningStrategy.GREEDY,
        budget_remaining_usd=0.50,
        latency_budget_ms=2000.0,
        current_error_rate=0.45,
    )
    assert rec2.new_strategy == PlanningStrategy.RISK_OPTIMIZED
    assert rec2.expected_utility_delta > 0
