"""
Goal Decomposer Service
=======================
Decomposes high-level Goals into structured hierarchical Mission Graphs:
Objective -> Milestone -> Subgoal -> Task -> Action.
"""

from typing import Tuple
from research_validation.goal.models.goal import Goal
from research_validation.goal.models.mission import (
    ObjectiveNode, MilestoneNode, SubgoalNode, TaskNode, ActionNode
)


class GoalDecomposer:
    """
    Translates a verified scientific Goal into a hierarchical execution graph.
    """

    @classmethod
    def decompose_goal(cls, goal: Goal) -> Tuple[ObjectiveNode, ...]:
        """Builds Objective, Milestone, Subgoal, Task, and Action hierarchy."""
        obj_id = f"obj_{goal.goal_id}_primary"
        ms_id = f"ms_{goal.goal_id}_data_prep"
        ms2_id = f"ms_{goal.goal_id}_eval"
        sg_id = f"sg_{goal.goal_id}_ingest"
        sg2_id = f"sg_{goal.goal_id}_benchmark"
        task_id = f"task_{goal.goal_id}_run_eval"
        act_id = f"act_{goal.goal_id}_exec"

        action = ActionNode(
            node_id=act_id,
            parent_id=task_id,
            title="Execute Model Evaluation Harness",
            description=f"Run benchmark across datasets: {', '.join(goal.required_datasets)}",
            priority=goal.priority,
            estimated_duration_hours=0.5,
            confidence_target=goal.confidence_threshold.value,
            required_capabilities=tuple(r.capability_name for r in goal.capability_requirements),
            expected_evidence=("EXECUTION_TRACE", "RAW_OUTPUT_DIGEST"),
            dependencies=(),
            tool_or_executor="ScientificExperimentRunner",
            parameters={"target_metrics": list(goal.evaluation_metrics)},
        )

        task = TaskNode(
            node_id=task_id,
            parent_id=sg2_id,
            title="Run Evaluation Pipeline",
            description="Execute automated benchmark harness and extract metrics.",
            priority=goal.priority,
            estimated_duration_hours=1.0,
            confidence_target=goal.confidence_threshold.value,
            required_capabilities=tuple(r.capability_name for r in goal.capability_requirements),
            expected_evidence=("METRIC_LOG", "MERKLE_ROOT"),
            dependencies=(),
            actions=(action,),
        )

        subgoal1 = SubgoalNode(
            node_id=sg_id,
            parent_id=ms_id,
            title="Ingest and Validate Datasets",
            description="Verify SHA-256 dataset integrity.",
            priority=goal.priority,
            estimated_duration_hours=0.2,
            confidence_target=1.0,
            required_capabilities=("STORAGE",),
            expected_evidence=("DATASET_CHECKSUM",),
            dependencies=(),
            tasks=(),
        )

        subgoal2 = SubgoalNode(
            node_id=sg2_id,
            parent_id=ms2_id,
            title="Compute Empirical Metrics",
            description="Evaluate metrics and calculate confidence intervals.",
            priority=goal.priority,
            estimated_duration_hours=1.0,
            confidence_target=goal.confidence_threshold.value,
            required_capabilities=tuple(r.capability_name for r in goal.capability_requirements),
            expected_evidence=("METRIC_REPORT", "CONFIDENCE_BOUNDS"),
            dependencies=(sg_id,),
            tasks=(task,),
        )

        milestone1 = MilestoneNode(
            node_id=ms_id,
            parent_id=obj_id,
            title="Dataset Verification Milestone",
            description="All public and private datasets verified on disk.",
            priority=goal.priority,
            estimated_duration_hours=0.5,
            confidence_target=1.0,
            required_capabilities=("STORAGE",),
            expected_evidence=("DATASET_VALIDATION_CERT",),
            dependencies=(),
            subgoals=(subgoal1,),
        )

        milestone2 = MilestoneNode(
            node_id=ms2_id,
            parent_id=obj_id,
            title="Empirical Evaluation Milestone",
            description="All required statistical criteria evaluated.",
            priority=goal.priority,
            estimated_duration_hours=2.0,
            confidence_target=goal.confidence_threshold.value,
            required_capabilities=tuple(r.capability_name for r in goal.capability_requirements),
            expected_evidence=("EVALUATION_REPORT",),
            dependencies=(ms_id,),
            subgoals=(subgoal2,),
        )

        objective = ObjectiveNode(
            node_id=obj_id,
            parent_id=None,
            title=f"Objective: {goal.title}",
            description=goal.objective,
            priority=goal.priority,
            estimated_duration_hours=2.5,
            confidence_target=goal.confidence_threshold.value,
            required_capabilities=tuple(r.capability_name for r in goal.capability_requirements),
            expected_evidence=("PUBLICATION_DRAFT", "GOVERNANCE_AUDIT"),
            dependencies=(),
            milestones=(milestone1, milestone2),
        )

        return (objective,)
