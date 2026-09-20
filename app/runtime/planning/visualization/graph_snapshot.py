"""
Visual Graph Snapshot Generator.

Generates UI-ready graphical representations of ExecutionDAG instances, computing
hierarchical layout coordinates, execution status colors, and critical path highlights.
"""

from __future__ import annotations

from typing import Any, Dict, List
from app.runtime.planning.graph.dag import ExecutionDAG


class VisualGraphSnapshot:
    """Generates structured DAG visualization models for React flow & SVG renderers."""

    @classmethod
    def generate_snapshot(cls, dag: ExecutionDAG) -> Dict[str, Any]:
        """Produces layout coordinates and node metadata for visual rendering."""
        crit_nodes, crit_dur = dag.compute_critical_path()
        wavefronts = dag.compute_concurrency_wavefronts()

        visual_nodes = []
        # Assign X/Y coordinates based on wavefront layer
        for layer_idx, wave in enumerate(wavefronts):
            x_pos = 100 + (layer_idx * 220)
            layer_size = len(wave)
            for item_idx, node in enumerate(wave):
                y_pos = 100 + (item_idx * 140) - ((layer_size - 1) * 70)
                visual_nodes.append({
                    "id": node.node_id,
                    "label": node.name,
                    "task_type": node.task_type,
                    "status": node.status.value,
                    "priority": node.priority,
                    "estimated_cost_usd": node.estimated_cost_usd,
                    "estimated_runtime_ms": node.estimated_runtime_ms,
                    "actual_runtime_ms": node.actual_runtime_ms,
                    "assigned_worker": node.assigned_worker,
                    "is_critical_path": node.is_critical_path,
                    "total_slack_ms": node.total_slack_ms,
                    "position": {"x": x_pos, "y": y_pos},
                })

        visual_edges = []
        for eid, edge in dag.edges.items():
            is_crit_edge = (edge.source_node_id in crit_nodes and edge.target_node_id in crit_nodes)
            visual_edges.append({
                "id": eid,
                "source": edge.source_node_id,
                "target": edge.target_node_id,
                "edge_type": edge.edge_type.value,
                "condition": edge.condition_expression,
                "is_critical_path": is_crit_edge,
            })

        return {
            "dag_id": dag.dag_id,
            "mission_id": dag.mission_id,
            "generation": dag.generation,
            "critical_path_duration_ms": crit_dur,
            "critical_nodes_count": len(crit_nodes),
            "structural_depth": len(wavefronts),
            "nodes": visual_nodes,
            "edges": visual_edges,
        }
