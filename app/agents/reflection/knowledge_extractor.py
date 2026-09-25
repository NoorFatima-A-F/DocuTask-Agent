"""
Knowledge Extractor.
Distills general heuristics, decomposition rules, and execution strategies from traces and critiques.
Never directly updates Memory; outputs immutable LearningArtifacts.
"""

from typing import List
from uuid import uuid4
from app.agents.reflection.interfaces import IKnowledgeExtractor
from app.agents.reflection.learning_artifact import LearningArtifact, LearningArtifactType
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope
from app.agents.reflection.self_critique import SelfCritique


class KnowledgeExtractor(IKnowledgeExtractor):
    """Extracts immutable LearningArtifact entities from execution analysis and self-critiques."""

    def extract_artifacts(
        self,
        trace: ExecutionTraceEnvelope,
        critique: SelfCritique
    ) -> List[LearningArtifact]:
        """Synthesizes reusable, immutable learning artifacts."""
        artifacts: List[LearningArtifact] = []

        # 1. Success pattern extraction
        if trace.final_state == "COMPLETED" and not trace.errors:
            artifacts.append(LearningArtifact(
                artifact_id=uuid4(),
                artifact_type=LearningArtifactType.DECOMPOSITION_STRATEGY,
                title=f"Optimal Decomposition for Goal '{trace.goal[:40]}'",
                description=f"Flawless execution with {len(trace.tasks)} tasks.",
                heuristic_content={
                    "task_sequence": [t.task_name for t in trace.tasks],
                    "total_duration_ms": trace.total_duration_ms
                },
                conditions=[f"goal_contains:{trace.goal[:20]}"],
                confidence_score=0.95,
                source_execution_id=trace.execution_id
            ))

        # 2. Failure avoidance rule from critique
        for finding in critique.findings:
            if finding.category in ("HALLUCINATION", "CIRCULAR_REASONING"):
                artifacts.append(LearningArtifact(
                    artifact_id=uuid4(),
                    artifact_type=LearningArtifactType.FAILURE_AVOIDANCE_RULE,
                    title=f"Avoid {finding.category} in Reasoning",
                    description=finding.description,
                    heuristic_content={"avoid_category": finding.category, "correction": finding.suggested_correction},
                    conditions=["reasoning_phase"],
                    confidence_score=finding.confidence,
                    source_execution_id=trace.execution_id
                ))

        # 3. Tool selection optimization
        if trace.tool_calls:
            reliable_tools = [t.tool_name for t in trace.tool_calls if t.success]
            if reliable_tools:
                artifacts.append(LearningArtifact(
                    artifact_id=uuid4(),
                    artifact_type=LearningArtifactType.TOOL_SELECTION,
                    title="Validated Reliable Tools Heuristic",
                    description=f"Verified reliability for {set(reliable_tools)}.",
                    heuristic_content={"reliable_tools": list(set(reliable_tools))},
                    conditions=["tool_selection_phase"],
                    confidence_score=0.90,
                    source_execution_id=trace.execution_id
                ))

        # 4. Retry policy heuristic if high retries
        high_retries = [t for t in trace.tasks if t.retry_count > 1]
        if high_retries:
            artifacts.append(LearningArtifact(
                artifact_id=uuid4(),
                artifact_type=LearningArtifactType.RETRY_POLICY,
                title="Adaptive Backoff Heuristic for Flaky Tasks",
                description="Elevated retry count observed; recommend exponential backoff with jitter.",
                heuristic_content={"tasks": [t.task_name for t in high_retries], "recommended_backoff": "EXPONENTIAL_JITTER"},
                conditions=["retry_phase"],
                confidence_score=0.85,
                source_execution_id=trace.execution_id
            ))

        return artifacts
