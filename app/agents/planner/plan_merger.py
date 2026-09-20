"""
Plan Merger Engine.
Merges multiple subplans or parallel branches into a unified PlanGraph.
"""

from typing import List
from uuid import uuid4
from app.agents.planning.contracts import Plan
from app.agents.planning.graph import PlanGraph


class PlanMerger:
    """Merges multiple plans into a combined composite plan."""

    def merge_plans(self, plans: List[Plan]) -> Plan:
        if not plans:
            raise ValueError("Cannot merge empty plan list.")
        if len(plans) == 1:
            return plans[0]

        base = plans[0]
        combined_nodes = dict(base.graph.nodes)
        combined_edges = list(base.graph.edges)

        for p in plans[1:]:
            combined_nodes.update(p.graph.nodes)
            combined_edges.extend(p.graph.edges)

        merged_graph = PlanGraph(
            graph_id=f"merged_{uuid4().hex[:8]}",
            nodes=combined_nodes,
            edges=combined_edges,
            entry_node_ids=base.graph.entry_node_ids,
            exit_node_ids=plans[-1].graph.exit_node_ids
        )

        return Plan(
            identity=base.identity,
            name="MergedPlan",
            graph=merged_graph,
            metadata=base.metadata,
            statistics=base.statistics
        )
