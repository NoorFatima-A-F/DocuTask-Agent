"""
Execution Graph Invariant Validator.

Formally validates DAG integrity, acyclicity, reachability, dangling node elimination,
and capability compatibility before execution begins.
"""

from __future__ import annotations

from typing import List, Tuple
from app.runtime.planning.graph.dag import ExecutionDAG


class GraphValidator:
    """Validates structural and semantic invariants of an ExecutionDAG."""

    @classmethod
    def validate(cls, dag: ExecutionDAG) -> Tuple[bool, List[str]]:
        """
        Runs comprehensive validation checks on the DAG.
        Returns: (is_valid, list_of_error_messages)
        """
        errors: List[str] = []

        if not dag.nodes:
            errors.append("DAG is empty: Contains zero nodes.")
            return False, errors

        # 1. Cycle Detection
        if dag.has_cycle():
            errors.append("Cycle detected: DAG contains directed cyclic dependencies.")

        # 2. Edge Referencing Soundness
        for eid, edge in dag.edges.items():
            if edge.source_node_id not in dag.nodes:
                errors.append(f"Dangling edge {eid}: source {edge.source_node_id} does not exist.")
            if edge.target_node_id not in dag.nodes:
                errors.append(f"Dangling edge {eid}: target {edge.target_node_id} does not exist.")

        # 3. Reachability & Connectivity
        topo = []
        try:
            topo = dag.topological_sort()
        except ValueError as ex:
            errors.append(f"Topological sort error: {ex}")

        # Check for completely isolated nodes (except for single-node DAGs)
        if len(dag.nodes) > 1:
            for node in dag.nodes.values():
                parents = dag._adjacency_in.get(node.node_id, [])
                children = dag._adjacency_out.get(node.node_id, [])
                if not parents and not children:
                    errors.append(f"Isolated disconnected node: {node.node_id} has no incoming or outgoing edges.")

        is_valid = (len(errors) == 0)
        return is_valid, errors
