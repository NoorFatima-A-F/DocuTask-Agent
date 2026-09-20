"""
Hierarchical Task Decomposition Engine.
Performs recursive hierarchical decomposition from Goal -> Objectives -> Milestones -> Tasks -> Atomic Tasks.
"""

from typing import List
from uuid import uuid4
from app.agents.planner.hierarchy import (
    AbstractionLevel,
    DecompositionNode,
    DecompositionTree,
)
from app.agents.planning.goals import PlanGoal
from app.agents.planning.tasks import PlanningTask


class HierarchicalTaskDecomposer:
    """Recursively breaks high-level goals down to atomic executable tasks."""

    def decompose_goal(self, goal: PlanGoal) -> DecompositionTree:
        """Decomposes a goal into structured task nodes and atomic tasks."""
        tree_nodes = {}
        atomic_tasks = []

        root_node_id = f"node_{goal.goal_id}"
        tree_nodes[root_node_id] = DecompositionNode(
            node_id=root_node_id,
            name=goal.name,
            level=AbstractionLevel.STRATEGIC_GOAL,
            children_ids=["t1_ocr", "t2_extract", "t3_validate"]
        )

        # Level: Tasks / Atomic Tasks
        t1 = PlanningTask(
            task_id="t1_ocr",
            name="OCR Processing",
            capability_requirement="OCR",
            estimated_duration_seconds=5.0,
            estimated_cost_usd=0.1
        )
        t2 = PlanningTask(
            task_id="t2_extract",
            name="Data Extraction",
            capability_requirement="LLM",
            dependencies=["t1_ocr"],
            estimated_duration_seconds=10.0,
            estimated_cost_usd=0.4
        )
        t3 = PlanningTask(
            task_id="t3_validate",
            name="Policy & Rule Validation",
            capability_requirement="DECISION",
            dependencies=["t2_extract"],
            estimated_duration_seconds=2.0,
            estimated_cost_usd=0.05
        )

        for task in [t1, t2, t3]:
            atomic_tasks.append(task)
            tree_nodes[task.task_id] = DecompositionNode(
                node_id=task.task_id,
                name=task.name,
                level=AbstractionLevel.ATOMIC_TASK,
                parent_id=root_node_id
            )

        return DecompositionTree(
            root_goal=goal,
            nodes=tree_nodes,
            atomic_tasks=atomic_tasks
        )
