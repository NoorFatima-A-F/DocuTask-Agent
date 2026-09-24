"""Tests for Runtime Provenance DAG and Traversal Engine."""

from app.runtime.provenance_dag.provenance_dag_builder import (
    ProvenanceDAGBuilder,
    TraversalEngine,
)


def test_provenance_dag_and_traversal():
    dag = ProvenanceDAGBuilder()
    dag.add_node("node-in", "INPUT", "Raw Document", "hash-doc-raw")
    dag.add_node("node-plan", "PLAN", "Planner Decision", "hash-plan", parent_ids=["node-in"])
    dag.add_node("node-tool", "TOOL", "OCR Tool Execution", "hash-tool", parent_ids=["node-plan"])
    dag.add_node("node-out", "OUTPUT", "Extracted JSON", "hash-out", parent_ids=["node-tool"])

    assert dag.count() == 4

    # Backward lineage from output should contain tool, plan, in
    backward = TraversalEngine.trace_backward_lineage(dag, "node-out")
    ancestor_ids = [n.node_id for n in backward]
    assert "node-out" in ancestor_ids
    assert "node-tool" in ancestor_ids
    assert "node-plan" in ancestor_ids
    assert "node-in" in ancestor_ids

    # Forward impact from input should reach all downstream nodes
    forward = TraversalEngine.trace_forward_impact(dag, "node-in")
    descendant_ids = [n.node_id for n in forward]
    assert "node-in" in descendant_ids
    assert "node-out" in descendant_ids
