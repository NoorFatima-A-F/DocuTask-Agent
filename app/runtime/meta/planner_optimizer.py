"""Planner Optimizer for DocuTask ADIP Meta-Reasoning Layer.

Dynamically tunes search parameters (beam width, candidate count, simulation iterations,
planning time budget) based on document complexity and metacognitive feedback.
"""

from __future__ import annotations

from pydantic import BaseModel


class PlannerHyperparameters(BaseModel):
    """Dynamic operational parameters governing the autonomous planner."""
    beam_width: int = 4
    candidate_strategy_count: int = 4
    simulation_iterations: int = 300
    planning_timeout_ms: float = 3000.0
    search_depth_limit: int = 4
    utility_w_accuracy: float = 0.40
    utility_w_latency: float = 0.20
    utility_w_cost: float = 0.20
    utility_w_risk: float = 0.10


class PlannerOptimizer:
    """Tunes planning hyperparameters to optimize search quality vs compute overhead."""

    def optimize_parameters(
        self,
        document_complexity: float = 1.0,
        critique_score: float = 0.90,
        sla_urgency: str = "NORMAL",
    ) -> PlannerHyperparameters:
        # Default baseline
        beam = 4
        candidates = 4
        sims = 300
        depth = 4

        # Scale based on document complexity
        if document_complexity > 2.0:
            beam = 6
            sims = 500
            depth = 5

        # Scale based on critique feedback (if previous critique score was low, increase search depth)
        if critique_score < 0.75:
            beam = max(beam, 8)
            candidates = 6
            sims = 600

        # Adjust for SLA urgency
        if sla_urgency == "URGENT":
            sims = 150
            beam = 3

        return PlannerHyperparameters(
            beam_width=beam,
            candidate_strategy_count=candidates,
            simulation_iterations=sims,
            search_depth_limit=depth,
        )
