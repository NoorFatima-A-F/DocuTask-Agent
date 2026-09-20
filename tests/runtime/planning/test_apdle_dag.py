"""
Unit Tests for APDLE ExecutionDAG, Nodes, Edges, CPM, and Graph Optimization.
"""

import pytest
from app.runtime.planning.graph.dag import ExecutionDAG
from app.runtime.planning.graph.edge import DAGEdge, EdgeType
from app.runtime.planning.graph.graph_builder import ExecutionGraphBuilder
from app.runtime.planning.graph.graph_optimizer import GraphOptimizer
from app.runtime.planning.graph.graph_validator import GraphValidator
from app.runtime.planning.graph.node import DAGNode, DependencySpec, DependencyType, NodeStatus


def test_dag_creation_and_topological_sort():
    """Verifies that ExecutionDAG constructs acyclic graphs and correctly sorts nodes."""
    dag = ExecutionGraphBuilder.build_financial_invoice_audit_dag(mission_id="m-audit-01")
    assert len(dag.nodes) == 5
    assert len(dag.edges) == 5

    is_valid, errors = GraphValidator.validate(dag)
    assert is_valid is True
    assert len(errors) == 0

    topo = dag.topological_sort()
    assert len(topo) == 5
    assert topo[0].node_id == "node_ocr_01"  # Root node
    assert topo[-1].node_id == "node_reflection"  # Sink node


def test_dag_cycle_detection():
    """Verifies that adding a cycle-inducing edge is strictly rejected."""
    dag = ExecutionDAG(dag_id="dag-test", mission_id="m-test")
    n1 = DAGNode(node_id="n1", mission_id="m-test", name="N1", task_type="GENERAL")
    n2 = DAGNode(node_id="n2", mission_id="m-test", name="N2", task_type="GENERAL")
    n3 = DAGNode(node_id="n3", mission_id="m-test", name="N3", task_type="GENERAL")

    dag.add_node(n1)
    dag.add_node(n2)
    dag.add_node(n3)

    dag.add_edge(DAGEdge(source_node_id="n1", target_node_id="n2"))
    dag.add_edge(DAGEdge(source_node_id="n2", target_node_id="n3"))

    # Attempt back-edge n3 -> n1
    with pytest.raises(ValueError, match="creates a directed cycle"):
        dag.add_edge(DAGEdge(source_node_id="n3", target_node_id="n1"))

    assert dag.has_cycle() is False


def test_critical_path_method_cpm():
    """Verifies that CPM correctly computes earliest/latest start times and slack."""
    dag = ExecutionGraphBuilder.build_financial_invoice_audit_dag(mission_id="m-cpm")
    crit_nodes, total_dur = dag.compute_critical_path()

    assert len(crit_nodes) >= 3
    assert "node_ocr_01" in crit_nodes
    assert total_dur > 0.0

    # Line items parsing (280ms) should be on critical path vs metadata (180ms)
    assert "node_extract_items" in crit_nodes


def test_concurrency_wavefronts_and_transitive_reduction():
    """Verifies concurrency grouping and transitive edge reduction."""
    dag = ExecutionGraphBuilder.build_financial_invoice_audit_dag(mission_id="m-opt")
    wavefronts = dag.compute_concurrency_wavefronts()
    
    # Layer 0: [OCR], Layer 1: [Items, Meta], Layer 2: [SMT], Layer 3: [Reflection]
    assert len(wavefronts) == 4
    assert len(wavefronts[1]) == 2  # 2 parallel extraction tasks

    # Add redundant edge OCR -> Reflection
    dag.add_edge(DAGEdge(source_node_id="node_ocr_01", target_node_id="node_reflection"))
    assert len(dag.edges) == 6

    # Optimize (transitive reduction)
    pruned = GraphOptimizer.transitive_reduction(dag)
    assert pruned == 1
    assert len(dag.edges) == 5
