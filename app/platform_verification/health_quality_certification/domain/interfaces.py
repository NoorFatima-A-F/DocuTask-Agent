"""
Phase 3H.5.11: Domain Interfaces for Health Quality Scoring & Certification Framework
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .models import (
    LivenessQualityMetrics,
    ReadinessQualityMetrics,
    DependencyHealthMetrics,
    FailureDetectionMetrics,
    RecoveryCapabilityMetrics,
    MonitoringIntegrationMetrics,
    SecurityComplianceMetrics,
    EvidenceQualityMetrics,
    SREReliabilityMetrics,
    RegressionReport,
    DeploymentGateReport,
    HealthQualityCertificationReport,
    HealthQualityScorecard,
    CategoryScoreItem,
)


class IHealthQualityEvaluator(ABC):
    @abstractmethod
    def evaluate_liveness(self) -> LivenessQualityMetrics:
        pass

    @abstractmethod
    def evaluate_readiness(self) -> ReadinessQualityMetrics:
        pass

    @abstractmethod
    def evaluate_dependencies(self) -> DependencyHealthMetrics:
        pass

    @abstractmethod
    def evaluate_failure_detection(self) -> FailureDetectionMetrics:
        pass

    @abstractmethod
    def evaluate_recovery(self) -> RecoveryCapabilityMetrics:
        pass

    @abstractmethod
    def evaluate_monitoring(self) -> MonitoringIntegrationMetrics:
        pass

    @abstractmethod
    def evaluate_security(self) -> SecurityComplianceMetrics:
        pass

    @abstractmethod
    def evaluate_evidence(self) -> EvidenceQualityMetrics:
        pass


class ISREReliabilityEngine(ABC):
    @abstractmethod
    def calculate_reliability_metrics(self) -> SREReliabilityMetrics:
        pass


class IRegressionDetector(ABC):
    @abstractmethod
    def detect_regression(self, current_scores: Dict[str, float], previous_scores: Dict[str, float] = None) -> RegressionReport:
        pass


class IDeploymentGatekeeper(ABC):
    @abstractmethod
    def evaluate_deployment_gate(
        self,
        overall_score: float,
        liveness_score: float,
        readiness_score: float,
        security_score: float,
        failure_detection_score: float,
        sre_metrics: SREReliabilityMetrics,
        regression_report: RegressionReport,
    ) -> DeploymentGateReport:
        pass


class IHealthQualityScorer(ABC):
    @abstractmethod
    def calculate_certification_scorecard(
        self,
        liveness: LivenessQualityMetrics,
        readiness: ReadinessQualityMetrics,
        dependencies: DependencyHealthMetrics,
        failure_detection: FailureDetectionMetrics,
        recovery: RecoveryCapabilityMetrics,
        monitoring: MonitoringIntegrationMetrics,
        security: SecurityComplianceMetrics,
        evidence: EvidenceQualityMetrics,
        sre_metrics: SREReliabilityMetrics,
        regression_report: RegressionReport,
        gate_report: DeploymentGateReport,
    ) -> HealthQualityScorecard:
        pass
