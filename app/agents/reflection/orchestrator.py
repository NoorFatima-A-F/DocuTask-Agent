"""
Reflection Orchestrator.
Coordinates the parallel and staged execution of evaluation pipelines, critique generation,
learning extraction, recommendations, and feedback formulation across reflection DAGs.
"""

from typing import Any, Dict, List, Optional
from app.agents.reflection.adaptation_engine import AdaptationEngine, AdaptationProposal
from app.agents.reflection.critique_engine import CritiqueEngine
from app.agents.reflection.evaluation import EvaluationReport
from app.agents.reflection.evaluation_pipeline import EvaluationPipeline
from app.agents.reflection.feedback_generator import FeedbackGenerator, SubsystemFeedbackBundle
from app.agents.reflection.knowledge_extractor import KnowledgeExtractor
from app.agents.reflection.learning_artifact import LearningArtifact
from app.agents.reflection.recommendation_engine import Recommendation, RecommendationEngine
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope
from app.agents.reflection.self_critique import SelfCritique


class ReflectionOrchestrator:
    """Orchestrates multi-stage reflection workflow."""

    def __init__(
        self,
        evaluation_pipeline: Optional[EvaluationPipeline] = None,
        critique_engine: Optional[CritiqueEngine] = None,
        knowledge_extractor: Optional[KnowledgeExtractor] = None,
        recommendation_engine: Optional[RecommendationEngine] = None,
        adaptation_engine: Optional[AdaptationEngine] = None,
        feedback_generator: Optional[FeedbackGenerator] = None,
    ):
        self.evaluation_pipeline = evaluation_pipeline or EvaluationPipeline()
        self.critique_engine = critique_engine or CritiqueEngine()
        self.knowledge_extractor = knowledge_extractor or KnowledgeExtractor()
        self.recommendation_engine = recommendation_engine or RecommendationEngine()
        self.adaptation_engine = adaptation_engine or AdaptationEngine()
        self.feedback_generator = feedback_generator or FeedbackGenerator()

    async def orchestrate_reflection(
        self,
        trace: ExecutionTraceEnvelope
    ) -> Dict[str, Any]:
        """Runs ordered reflection stages over completed execution trace."""
        # Stage 1: Multi-dimensional evaluation
        evaluation_report: EvaluationReport = self.evaluation_pipeline.run_pipeline(trace)

        # Stage 2: Introspective self-critique & logic validation
        critique: SelfCritique = self.critique_engine.generate_critique(trace, evaluation_report)

        # Stage 3: Distill immutable learning artifacts for Memory
        artifacts: List[LearningArtifact] = self.knowledge_extractor.extract_artifacts(trace, critique)

        # Stage 4: Synthesize cross-subsystem recommendations
        recommendations: List[Recommendation] = self.recommendation_engine.generate_recommendations(
            critique, artifacts
        )

        # Stage 5: Formulate adaptation proposals
        adaptation_proposals: List[AdaptationProposal] = self.adaptation_engine.generate_proposals(
            recommendations
        )

        # Stage 6: Produce typed feedback bundles for Planner, Execution, Memory, Tools
        feedback_bundle: SubsystemFeedbackBundle = self.feedback_generator.generate_feedback(
            critique, recommendations
        )

        return {
            "evaluation_report": evaluation_report,
            "critique": critique,
            "learning_artifacts": artifacts,
            "recommendations": recommendations,
            "adaptation_proposals": adaptation_proposals,
            "feedback_bundle": feedback_bundle
        }
