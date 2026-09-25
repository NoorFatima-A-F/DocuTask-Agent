"""
Phase 3I.12: Autonomous Reliability Engineering — Domain Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

from app.platform_verification.autonomous_reliability_engineering.domain.models import (
    AutonomousArchitectureReport,
    AnomalyIntelligenceReport,
    FailurePredictionReport,
    OptimizationRecommendationReport,
    CapacityIntelligenceReport,
    AutonomousScalingReport,
    SelfOptimizationReport,
    IncidentLearningReport,
    ReliabilityKnowledgeGraphReport,
    AutonomousSafetyReport,
    ContinuousReliabilityImprovementReport,
    AutonomousReliabilityCertificationReport,
)


class IAutonomousArchitectureVerifier(ABC):
    @abstractmethod
    def verify(self) -> AutonomousArchitectureReport:
        """Verify autonomous reliability architecture layers and control components."""
        pass


class IAnomalyIntelligenceVerifier(ABC):
    @abstractmethod
    def verify(self) -> AnomalyIntelligenceReport:
        """Verify multi-modal anomaly intelligence across metrics, logs, and distributed traces."""
        pass


class IFailurePredictionVerifier(ABC):
    @abstractmethod
    def verify(self) -> FailurePredictionReport:
        """Verify failure prediction across memory, queues, DB pools, and AI providers."""
        pass


class IOptimizationEngineVerifier(ABC):
    @abstractmethod
    def verify(self) -> OptimizationRecommendationReport:
        """Verify recommendations across performance, cost, allocation, and architecture."""
        pass


class ICapacityPlanningVerifier(ABC):
    @abstractmethod
    def verify(self) -> CapacityIntelligenceReport:
        """Verify multi-horizon capacity forecasting for workers, databases, and queues."""
        pass


class IAutonomousScalingVerifier(ABC):
    @abstractmethod
    def verify(self) -> AutonomousScalingReport:
        """Verify predictive scaling decisions, cooldown safety, and rollback guarantees."""
        pass


class ISelfOptimizationVerifier(ABC):
    @abstractmethod
    def verify(self) -> SelfOptimizationReport:
        """Verify closed-loop self-optimization across DB, queues, AI pipeline, and infrastructure."""
        pass


class IIncidentLearningVerifier(ABC):
    @abstractmethod
    def verify(self) -> IncidentLearningReport:
        """Verify RCA pattern extraction, operational learning, and recurrence prevention."""
        pass


class IKnowledgeGraphVerifier(ABC):
    @abstractmethod
    def verify(self) -> ReliabilityKnowledgeGraphReport:
        """Verify the operational reliability knowledge graph structure, nodes, and edges."""
        pass


class IDecisionSafetyVerifier(ABC):
    @abstractmethod
    def verify(self) -> AutonomousSafetyReport:
        """Verify Safe, Controlled, and Restricted autonomous action safety controls."""
        pass


class IContinuousImprovementLoopVerifier(ABC):
    @abstractmethod
    def verify(self) -> ContinuousReliabilityImprovementReport:
        """Verify the continuous Observe-Analyze-Improve-Measure-Learn reliability cycle."""
        pass


class IAutonomousReliabilityScorer(ABC):
    @abstractmethod
    def compute_certification(self, verification_results: Dict[str, Any]) -> AutonomousReliabilityCertificationReport:
        """Compute the 7-category weighted score and generate the certification report."""
        pass


class IAutonomousReliabilityExporter(ABC):
    @abstractmethod
    def export(self, verification_results: Dict[str, Any], certification_report: AutonomousReliabilityCertificationReport) -> Dict[str, str]:
        """Export all verification manifests and signed metadata.json."""
        pass
