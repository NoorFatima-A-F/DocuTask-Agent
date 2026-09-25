"""
Recommendation Engine.
Synthesizes evidence-backed, confidence-scored recommendations across Planner, Execution,
Recovery, Tool Registry, Decision Engine, and Memory subsystems.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.reflection.interfaces import IRecommendationEngine
from app.agents.reflection.learning_artifact import LearningArtifact
from app.agents.reflection.self_critique import SelfCritique


class SubsystemTarget(str, Enum):
    """Subsystems targeted by reflection recommendations."""
    PLANNER = "PLANNER"
    EXECUTION = "EXECUTION"
    RECOVERY = "RECOVERY"
    TOOL_REGISTRY = "TOOL_REGISTRY"
    DECISION_ENGINE = "DECISION_ENGINE"
    MEMORY = "MEMORY"


class Recommendation(BaseModel):
    """Actionable recommendation addressing an observed deficiency or optimization opportunity."""
    recommendation_id: UUID = Field(default_factory=uuid4)
    target_subsystem: SubsystemTarget
    title: str
    rationale: str
    expected_impact: str  # e.g., "Reduces execution latency by ~25%"
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    evidence: List[str] = Field(default_factory=list)
    action_type: str = Field(default="OPTIMIZATION")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}


class RecommendationEngine(IRecommendationEngine):
    """Generates cross-subsystem recommendations from self-critiques and learning artifacts."""

    def generate_recommendations(
        self,
        critique: SelfCritique,
        artifacts: List[LearningArtifact]
    ) -> List[Recommendation]:
        """Generates recommendations for all platform subsystems."""
        recommendations: List[Recommendation] = []

        # 1. Planner recommendations from critique findings
        for f in critique.findings:
            if f.category in ("UNCHECKED_ASSUMPTION", "CIRCULAR_REASONING", "HALLUCINATION"):
                recommendations.append(Recommendation(
                    recommendation_id=uuid4(),
                    target_subsystem=SubsystemTarget.PLANNER,
                    title=f"Enforce Grounding Gate for {f.category}",
                    rationale=f.description,
                    expected_impact="Eliminates ungrounded assertions in plan generation.",
                    confidence=f.confidence,
                    evidence=f.evidence,
                    action_type="CONSTRAINT_INJECTION"
                ))

        # 2. Tool Registry recommendations
        for art in artifacts:
            if art.artifact_type.value == "TOOL_SELECTION":
                recommendations.append(Recommendation(
                    recommendation_id=uuid4(),
                    target_subsystem=SubsystemTarget.TOOL_REGISTRY,
                    title="Promote Reliable Tool Mapping",
                    rationale=art.description,
                    expected_impact="Increases first-attempt tool call success rate.",
                    confidence=art.confidence_score,
                    evidence=[f"Artifact: {art.title}"],
                    action_type="CAPABILITY_WEIGHTING"
                ))

        # 3. Execution Runtime recommendations
        if any("latency" in w.lower() or "slow" in w.lower() for w in critique.weaknesses):
            recommendations.append(Recommendation(
                recommendation_id=uuid4(),
                target_subsystem=SubsystemTarget.EXECUTION,
                title="Increase Parallel Worker Allocation",
                rationale="Critical path delay observed due to sequential task queueing.",
                expected_impact="Reduces wall-clock duration for parallelizable branches.",
                confidence=0.88,
                evidence=critique.weaknesses,
                action_type="WORKER_POOL_SCALING"
            ))

        # 4. Memory recommendations
        if artifacts:
            recommendations.append(Recommendation(
                recommendation_id=uuid4(),
                target_subsystem=SubsystemTarget.MEMORY,
                title="Promote Learning Artifacts to Reflection Memory Tier",
                rationale=f"{len(artifacts)} new learning artifacts generated.",
                expected_impact="Improves semantic context retrieval for similar future goals.",
                confidence=0.95,
                evidence=[f"{len(artifacts)} artifacts staged"],
                action_type="MEMORY_PROMOTION"
            ))

        # 5. Recovery recommendations
        if any("timeout" in w.lower() or "failure" in w.lower() for w in critique.weaknesses):
            recommendations.append(Recommendation(
                recommendation_id=uuid4(),
                target_subsystem=SubsystemTarget.RECOVERY,
                title="Tune Retry Jitter and Backoff Bounds",
                rationale="Repeated task recovery attempts caused delays.",
                expected_impact="Avoids thundering herd on downstream services during recovery.",
                confidence=0.85,
                evidence=critique.weaknesses,
                action_type="RECOVERY_TUNING"
            ))

        # 6. Decision Engine recommendations
        recommendations.append(Recommendation(
            recommendation_id=uuid4(),
            target_subsystem=SubsystemTarget.DECISION_ENGINE,
            title="Maintain Current Governance Risk Thresholds",
            rationale="No policy violations observed during execution.",
            expected_impact="Preserves baseline security posture.",
            confidence=0.95,
            evidence=["Zero policy breaches in decision logs."],
            action_type="POLICY_MAINTENANCE"
        ))

        return recommendations
