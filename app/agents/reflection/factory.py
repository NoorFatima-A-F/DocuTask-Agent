"""
Reflection Factory.
Provides dependency-injected factories for creating pre-configured ReflectionEngine,
ReflectionRuntime, and EvaluationPipeline instances.
"""

from app.agents.reflection.adaptation_engine import AdaptationEngine
from app.agents.reflection.cache import ReflectionCache
from app.agents.reflection.critique_engine import CritiqueEngine
from app.agents.reflection.engine import ReflectionEngine
from app.agents.reflection.evaluation_pipeline import EvaluationPipeline
from app.agents.reflection.feedback_generator import FeedbackGenerator
from app.agents.reflection.knowledge_extractor import KnowledgeExtractor
from app.agents.reflection.manager import ReflectionManager
from app.agents.reflection.metrics import ReflectionMetricsCollector
from app.agents.reflection.orchestrator import ReflectionOrchestrator
from app.agents.reflection.recommendation_engine import RecommendationEngine
from app.agents.reflection.repository import InMemoryReflectionRepository
from app.agents.reflection.runtime import ReflectionRuntime


class ReflectionFactory:
    """Factory creating fully wired reflection engines with default or customized dependencies."""

    @staticmethod
    def create_engine(
        cache_capacity: int = 1000,
        enable_metrics: bool = True
    ) -> ReflectionEngine:
        """Instantiates fully wired ReflectionEngine with all default analyzers and evaluators."""
        evaluation_pipeline = EvaluationPipeline()
        critique_engine = CritiqueEngine()
        knowledge_extractor = KnowledgeExtractor()
        recommendation_engine = RecommendationEngine()
        adaptation_engine = AdaptationEngine()
        feedback_generator = FeedbackGenerator()

        orchestrator = ReflectionOrchestrator(
            evaluation_pipeline=evaluation_pipeline,
            critique_engine=critique_engine,
            knowledge_extractor=knowledge_extractor,
            recommendation_engine=recommendation_engine,
            adaptation_engine=adaptation_engine,
            feedback_generator=feedback_generator
        )

        repository = InMemoryReflectionRepository()
        cache = ReflectionCache(capacity=cache_capacity)
        manager = ReflectionManager(repository=repository, cache=cache)
        metrics = ReflectionMetricsCollector() if enable_metrics else None

        return ReflectionEngine(
            orchestrator=orchestrator,
            manager=manager,
            metrics_collector=metrics
        )

    @staticmethod
    def create_runtime() -> ReflectionRuntime:
        """Instantiates production ReflectionRuntime container."""
        engine = ReflectionFactory.create_engine()
        return ReflectionRuntime(engine=engine)
