"""
DAG Graph Serializer & Visual Export Engine.

Exports ExecutionDAG to JSON dictionaries, Mermaid flowchart syntax, and Graphviz DOT formats.
"""

from __future__ import annotations

from typing import Any, Dict
from app.runtime.planning.graph.dag import ExecutionDAG


class GraphSerializer:
    """Serializes ExecutionDAG into standard interchange and visualization formats."""

    @classmethod
    def to_dict(cls, dag: ExecutionDAG) -> Dict[str, Any]:
        """Converts DAG to structured dictionary for REST API and frontend."""
        crit_nodes, crit_dur = dag.compute_critical_path()
        return {
            "dag_id": dag.dag_id,
            "mission_id": dag.mission_id,
            "generation": dag.generation,
            "summary": dag.get_summary(),
            "nodes": {nid: node.model_dump() for nid, node in dag.nodes.items()},
            "edges": {eid: edge.model_dump() for eid, edge in dag.edges.items()},
            "critical_path_node_ids": crit_nodes,
        }

    @classmethod
    def to_mermaid(cls, dag: ExecutionDAG) -> str:
        """Renders DAG as Mermaid graph definition."""
        lines = ["graph TD"]
        
        # Nodes
        for nid, node in dag.nodes.items():
            status_style = f"[{node.name}<br/>({node.status.value})]"
            lines.append(f"    {nid}{status_style}")

        # Edges
        for edge in dag.edges.values():
            if edge.edge_type.value == "CONDITIONAL_BRANCH":
                lines.append(f"    {edge.source_node_id} -.->|{edge.condition_expression or 'cond'}| {edge.target_node_id}")
            else:
                lines.append(f"    {edge.source_node_id} --> {edge.target_node_id}")

        return "\n".join(lines)
