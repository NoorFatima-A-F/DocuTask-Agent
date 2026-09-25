"""
Fallback Plan Generator.
Generates safe, low-complexity fallback plans when main planning fails.
"""

from app.agents.planner.context import PlannerRequest
from app.agents.planning.builders import GraphBuilder, PlanBuilder
from app.agents.planning.contracts import Plan
from app.agents.planning.nodes import NodeType


class FallbackPlanGenerator:
    """Generates baseline sequential fallback plans."""

    def generate_fallback_plan(self, request: PlannerRequest) -> Plan:
        graph = (
            GraphBuilder("fallback_graph")
            .add_node("fallback_task", f"Fallback task for {request.goal.name}", NodeType.TASK)
            .with_entry_nodes(["fallback_task"])
            .with_exit_nodes(["fallback_task"])
            .build()
        )

        return (
            PlanBuilder("FallbackPlan")
            .for_goal(request.goal.goal_id)
            .with_graph(graph)
            .with_cost(0.1)
            .with_duration(5.0)
            .build()
        )
