"""Test Lineage Graph Engine and Transformation Tracker."""

from app.data_governance.lineage.nodes import LineageNode, LineageNodeType
from app.data_governance.lineage.edges import LineageEdge, LineageEdgeType
from app.data_governance.lineage.graph import LineageGraphEngine
from app.data_governance.lineage.tracker import LineageTracker


def test_lineage_graph_traversal():
    """Verify directed lineage DAG and recursive upstream/downstream search."""
    graph = LineageGraphEngine()
    org_id = "org_lineage_test"

    # Nodes: Doc -> Task -> JSON -> Model -> Summary
    graph.add_node(LineageNode(node_id="node_doc", node_type=LineageNodeType.DOCUMENT, label="Invoice.pdf", organization_id=org_id))
    graph.add_node(LineageNode(node_id="node_ocr", node_type=LineageNodeType.TASK, label="OCR Pipeline", organization_id=org_id))
    graph.add_node(LineageNode(node_id="node_json", node_type=LineageNodeType.DATASET, label="Extracted.json", organization_id=org_id))
    graph.add_node(LineageNode(node_id="node_ai", node_type=LineageNodeType.MODEL, label="Gemini LLM", organization_id=org_id))
    graph.add_node(LineageNode(node_id="node_summary", node_type=LineageNodeType.DOCUMENT, label="Summary.txt", organization_id=org_id))

    # Edges
    graph.add_edge(LineageEdge(edge_id="e1", source_node_id="node_doc", target_node_id="node_ocr", edge_type=LineageEdgeType.READ, organization_id=org_id))
    graph.add_edge(LineageEdge(edge_id="e2", source_node_id="node_ocr", target_node_id="node_json", edge_type=LineageEdgeType.GENERATED_BY, organization_id=org_id))
    graph.add_edge(LineageEdge(edge_id="e3", source_node_id="node_json", target_node_id="node_ai", edge_type=LineageEdgeType.READ, organization_id=org_id))
    graph.add_edge(LineageEdge(edge_id="e4", source_node_id="node_ai", target_node_id="node_summary", edge_type=LineageEdgeType.GENERATED_BY, organization_id=org_id))

    # Upstream from Summary
    upstream = graph.get_upstream_lineage("node_summary")
    upstream_ids = [n.node_id for n in upstream]
    assert "node_ai" in upstream_ids
    assert "node_json" in upstream_ids
    assert "node_ocr" in upstream_ids
    assert "node_doc" in upstream_ids

    # Downstream from Doc
    downstream = graph.get_downstream_lineage("node_doc")
    downstream_ids = [n.node_id for n in downstream]
    assert "node_ocr" in downstream_ids
    assert "node_summary" in downstream_ids


def test_lineage_tracker_context_manager():
    """Verify LineageTracker automatically registers nodes and edges within context."""
    tracker = LineageTracker()
    org_id = "org_track_test"

    tracker.register_node("raw_file_1", LineageNodeType.DOCUMENT, "Contract.pdf", org_id)
    tracker.register_node("parsed_chunk_1", LineageNodeType.DATASET, "Contract Chunk 1", org_id)

    with tracker.track("contract_chunking", ["raw_file_1"], ["parsed_chunk_1"], organization_id=org_id):
        pass  # Simulated chunking logic

    downstream = tracker.graph.get_downstream_lineage("raw_file_1")
    downstream_labels = [n.label for n in downstream]
    assert "contract_chunking" in downstream_labels
    assert "Contract Chunk 1" in downstream_labels
