"""
Feedback Generator.
Synthesizes strongly typed feedback bundles for Planner, Execution, Memory, and Tool Registry.
"""

from typing import Any, Dict, List, Optional
from uuid import uuid4
from pydantic import BaseModel, Field
from app.agents.reflection.evaluation import EvaluationReport
from app.agents.reflection.execution_feedback import ExecutionCritiqueItem, ExecutionFeedback
from app.agents.reflection.interfaces import IFeedbackGenerator
from app.agents.reflection.learning_artifact import LearningArtifact
from app.agents.reflection.memory_feedback import MemoryFeedback, MemoryUpdateRequest
from app.agents.reflection.planner_feedback import PlannerCritiqueItem, PlannerFeedback
from app.agents.reflection.recommendation_engine import Recommendation, SubsystemTarget
from app.agents.reflection.self_critique import SelfCritique
from app.agents.reflection.tool_feedback import ToolFeedback, ToolPerformanceFeedback


class SubsystemFeedbackBundle(BaseModel):
    """Aggregate bundle containing typed feedback for all downstream platform subsystems."""
    planner_feedback: PlannerFeedback
    execution_feedback: ExecutionFeedback
    memory_feedback: MemoryFeedback
    tool_feedback: ToolFeedback

    model_config = {"frozen": True}


class FeedbackGenerator(IFeedbackGenerator):
    """Generates structured subsystem feedback payloads from reflection critique and recommendations."""

    def generate_feedback(
        self,
        critique: SelfCritique,
        recommendations: List[Recommendation]
    ) -> SubsystemFeedbackBundle:
        """Constructs typed feedback models for each platform layer."""
        exec_id = critique.execution_id

        # 1. Planner Feedback
        planner_critiques: List[PlannerCritiqueItem] = []
        for f in critique.findings:
            if f.category in ("UNCHECKED_ASSUMPTION", "CIRCULAR_REASONING", "HALLUCINATION", "SUBOPTIMAL_PLAN"):
                planner_critiques.append(PlannerCritiqueItem(
                    code=f.category,
                    description=f.description,
                    suggested_action=f.suggested_correction or "Verify preconditions.",
                    confidence=f.confidence
                ))

        planner_feedback = PlannerFeedback(
            feedback_id=uuid4(),
            execution_id=exec_id,
            critique_items=planner_critiques,
            recommended_heuristics=[r.title for r in recommendations if r.target_subsystem == SubsystemTarget.PLANNER],
            decomposition_score=critique.overall_critique_score
        )

        # 2. Execution Feedback
        exec_critiques: List[ExecutionCritiqueItem] = []
        for w in critique.weaknesses:
            if "latency" in w.lower() or "retry" in w.lower() or "duration" in w.lower():
                exec_critiques.append(ExecutionCritiqueItem(
                    code="RUNTIME_BOTTLENECK",
                    description=w,
                    suggested_runtime_action="Adjust concurrency or timeouts.",
                    impact_level="MEDIUM"
                ))

        execution_feedback = ExecutionFeedback(
            feedback_id=uuid4(),
            execution_id=exec_id,
            critique_items=exec_critiques,
            recommended_worker_concurrency=4,
            runtime_score=critique.overall_critique_score
        )

        # 3. Memory Feedback
        memory_feedback = MemoryFeedback(
            feedback_id=uuid4(),
            execution_id=exec_id,
            update_requests=[],
            items_to_prune=[],
            context_efficiency_score=0.9
        )

        # 4. Tool Feedback
        tool_feedback = ToolFeedback(
            feedback_id=uuid4(),
            execution_id=exec_id,
            tool_evaluations=[],
            overall_tooling_score=1.0
        )

        return SubsystemFeedbackBundle(
            planner_feedback=planner_feedback,
            execution_feedback=execution_feedback,
            memory_feedback=memory_feedback,
            tool_feedback=tool_feedback
        )
