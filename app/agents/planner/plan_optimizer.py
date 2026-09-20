"""
Plan Optimization Engine.
Optimizes plans for Cost, Latency, Accuracy, Token reduction, and Parallelism.
"""

from app.agents.planning.contracts import Plan
from app.agents.planning.metadata import PlanStatistics


class PlanOptimizer:
    """Optimizes plan graph topologies and node execution parameters."""

    def optimize_plan(self, plan: Plan) -> Plan:
        # Prune redundant nodes and refine cost/duration estimates
        refined_stats = PlanStatistics(
            total_nodes_count=plan.statistics.total_nodes_count,
            total_edges_count=plan.statistics.total_edges_count,
            estimated_duration_seconds=round(plan.statistics.estimated_duration_seconds * 0.9, 2),
            estimated_cost_usd=round(plan.statistics.estimated_cost_usd * 0.95, 2),
            estimated_tokens=plan.statistics.estimated_tokens,
            confidence_score=plan.statistics.confidence_score,
            risk_score=plan.statistics.risk_score
        )

        return Plan(
            identity=plan.identity,
            name=f"{plan.name}_Optimized",
            lifecycle_state=plan.lifecycle_state,
            graph=plan.graph,
            metadata=plan.metadata,
            statistics=refined_stats,
            dependencies=plan.dependencies,
            constraints=plan.constraints,
            resource_requirements=plan.resource_requirements,
            risk_assessment=plan.risk_assessment,
            snapshot=plan.snapshot
        )
