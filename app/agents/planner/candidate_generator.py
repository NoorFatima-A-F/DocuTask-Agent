"""
Candidate Plan Generator.
Generates multiple candidate plan topologies across different planning strategies.
"""

from typing import List
from uuid import uuid4
from app.agents.planner.context import PlannerRequest
from app.agents.planner.decomposer import HierarchicalTaskDecomposer
from app.agents.planner.metadata import CandidatePlan
from app.agents.planning.builders import GraphBuilder, PlanBuilder
from app.agents.planning.edges import EdgeType
from app.agents.planning.nodes import NodeType


class CandidatePlanGenerator:
    """Generates candidate plans for multi-strategy evaluation and beam-search selection."""

    def __init__(self):
        self.decomposer = HierarchicalTaskDecomposer()

    def generate_candidates(self, request: PlannerRequest) -> List[CandidatePlan]:
        tree = self.decomposer.decompose_goal(request.goal)
        tasks = tree.atomic_tasks

        # Candidate 1: Standard Hierarchical Plan
        g1 = GraphBuilder("cand1_hierarchical")
        for t in tasks:
            g1.add_node(t.task_id, t.name, NodeType.TASK, timeout_seconds=t.estimated_duration_seconds)
        g1.add_edge("t1_ocr", "t2_extract", EdgeType.SEQUENTIAL)
        g1.add_edge("t2_extract", "t3_validate", EdgeType.SEQUENTIAL)
        g1.with_entry_nodes(["t1_ocr"]).with_exit_nodes(["t3_validate"])
        graph1 = g1.build()

        p1 = (
            PlanBuilder("Candidate_Hierarchical")
            .for_goal(request.goal.goal_id)
            .with_graph(graph1)
            .with_cost(0.55)
            .with_duration(17.0)
            .build()
        )

        cand1 = CandidatePlan(
            plan=p1,
            strategy_used="HIERARCHICAL",
            rank_score=0.92,
            estimated_cost_usd=0.55,
            estimated_duration_seconds=17.0,
            confidence=0.95
        )

        # Candidate 2: Fast Parallel Plan
        g2 = GraphBuilder("cand2_fast")
        for t in tasks:
            g2.add_node(t.task_id, t.name, NodeType.TASK, timeout_seconds=t.estimated_duration_seconds)
        g2.add_edge("t1_ocr", "t2_extract", EdgeType.SEQUENTIAL)
        g2.add_edge("t1_ocr", "t3_validate", EdgeType.SEQUENTIAL)
        g2.with_entry_nodes(["t1_ocr"]).with_exit_nodes(["t2_extract", "t3_validate"])
        graph2 = g2.build()

        p2 = (
            PlanBuilder("Candidate_Fast")
            .for_goal(request.goal.goal_id)
            .with_graph(graph2)
            .with_cost(0.60)
            .with_duration(12.0)
            .build()
        )

        cand2 = CandidatePlan(
            plan=p2,
            strategy_used="LEAST_COST",
            rank_score=0.88,
            estimated_cost_usd=0.60,
            estimated_duration_seconds=12.0,
            confidence=0.90
        )

        return [cand1, cand2]
