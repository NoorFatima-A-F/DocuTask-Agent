"""
Reflection Repository and Storage Layer.
Provides abstract and in-memory implementations for persisting reflections, evaluations,
recommendations, and learning artifacts. Cloud SQL/AlloyDB compatible.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from uuid import UUID
from app.agents.reflection.context import ReflectionResult
from app.agents.reflection.evaluation import EvaluationReport
from app.agents.reflection.interfaces import IReflectionRepository
from app.agents.reflection.learning_artifact import LearningArtifact
from app.agents.reflection.recommendation_engine import Recommendation
from app.agents.reflection.reflection import Reflection


class EvaluationRepository(ABC):
    """Persistence contract for evaluation reports."""

    @abstractmethod
    async def save_report(self, report: EvaluationReport) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_report_by_execution_id(self, execution_id: UUID) -> Optional[EvaluationReport]:
        raise NotImplementedError


class RecommendationRepository(ABC):
    """Persistence contract for actionable recommendations."""

    @abstractmethod
    async def save_recommendation(self, rec: Recommendation) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_subsystem(self, subsystem: str) -> List[Recommendation]:
        raise NotImplementedError


class LearningArtifactRepository(ABC):
    """Persistence contract for synthesized learning artifacts."""

    @abstractmethod
    async def save_artifact(self, artifact: LearningArtifact) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_artifacts(self) -> List[LearningArtifact]:
        raise NotImplementedError


class InMemoryReflectionRepository(IReflectionRepository):
    """Thread-safe in-memory repository for reflection aggregate roots."""

    def __init__(self):
        self._storage: Dict[UUID, Reflection] = {}

    async def save(self, reflection: Reflection) -> None:
        self._storage[reflection.identity.reflection_id] = reflection

    async def get_by_id(self, reflection_id: UUID) -> Optional[Reflection]:
        return self._storage.get(reflection_id)

    async def get_by_execution_id(self, execution_id: UUID) -> Optional[Reflection]:
        for ref in self._storage.values():
            if ref.identity.execution_id == execution_id:
                return ref
        return None

    async def list_all(self) -> List[Reflection]:
        return list(self._storage.values())


class InMemoryLearningArtifactRepository(LearningArtifactRepository):
    """In-memory storage for learning artifacts."""

    def __init__(self):
        self._artifacts: Dict[UUID, LearningArtifact] = {}

    async def save_artifact(self, artifact: LearningArtifact) -> None:
        self._artifacts[artifact.artifact_id] = artifact

    async def get_all_artifacts(self) -> List[LearningArtifact]:
        return list(self._artifacts.values())


class InMemoryRecommendationRepository(RecommendationRepository):
    """In-memory storage for recommendations."""

    def __init__(self):
        self._recommendations: Dict[UUID, Recommendation] = {}

    async def save_recommendation(self, rec: Recommendation) -> None:
        self._recommendations[rec.recommendation_id] = rec

    async def get_by_subsystem(self, subsystem: str) -> List[Recommendation]:
        return [
            r for r in self._recommendations.values()
            if r.target_subsystem.value == subsystem
        ]


class InMemoryEvaluationRepository(EvaluationRepository):
    """In-memory storage for evaluation reports."""

    def __init__(self):
        self._reports: Dict[UUID, EvaluationReport] = {}

    async def save_report(self, report: EvaluationReport) -> None:
        self._reports[report.execution_id] = report

    async def get_report_by_execution_id(self, execution_id: UUID) -> Optional[EvaluationReport]:
        return self._reports.get(execution_id)
