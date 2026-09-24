"""
Plan Repair Engine.
Performs incremental graph repair, constraint adjustment, and dependency relinking.
"""

from app.agents.planner.reflection import ReflectionCritique
from app.agents.planning.contracts import Plan
from app.agents.planning.edges import EdgeType, PlanEdge


class PlanRepairEngine:
    """Repairs flawed plans incrementally without requiring complete replanning."""

    def repair_plan(self, plan: Plan, critique: ReflectionCritique) -> Plan:
        if not critique.has_flaws:
            return plan

        # If isolated nodes, connect sequentially
        if "LINK_SEQUENTIAL_EDGES" in critique.suggested_repairs:
            node_ids = list(plan.graph.nodes.keys())
            new_edges = []
            for i in range(len(node_ids) - 1):
                new_edges.append(
                    PlanEdge(
                        edge_id=f"repair_{node_ids[i]}->{node_ids[i+1]}",
                        source_node_id=node_ids[i],
                        target_node_id=node_ids[i+1],
                        edge_type=EdgeType.SEQUENTIAL
                    )
                )

            repaired_graph = plan.graph.model_copy(update={"edges": new_edges})
            return plan.model_copy(update={"graph": repaired_graph, "name": f"{plan.name}_Repaired"})

        return plan
